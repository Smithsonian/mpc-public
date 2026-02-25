"""Ground-truth evaluation tools for digest2 classification results.

This module lets you compare digest2 scores against known orbital
classifications so you can measure how well digest2 performs on a
labelled dataset.  Typical workflow:

1. Load ground-truth orbital elements and/or orbit-type labels.
2. Load a trksub-to-designation mapping (so tracklet IDs in digest2
   output can be linked to known objects).
3. Run digest2 on the observations.
4. Feed the results and ground truth into :class:`TruthEvaluator` to
   produce confusion matrices, per-class accuracy metrics, score
   distributions, and diagnostic plots.

File formats
------------
**Ground-truth CSV** — one row per object.  A header row is **required**
and is used to determine which columns are present.  The CSV must contain
``designation``, ``i``, ``H``, and at least two of ``a``, ``e``, ``q``
so that the missing one can be derived (``q = a * (1 - e)``).

Supported column combinations (plus ``designation``, ``i``, ``H``):

    (i)   ``q``, ``e``          — ``a`` is computed as ``q / (1 - e)``
    (ii)  ``a``, ``e``          — ``q`` is computed as ``a * (1 - e)``
    (iii) ``a``, ``q``          — ``e`` is computed as ``1 - q / a``
    (iv)  ``a``, ``q``, ``e``   — all three supplied, no derivation needed

N.B. Internally digest2 uses the (``q, e``) pair as the primary orbital elements,
so the ability to supply ``a`` is primarily for user convenience.
If only two of (``a``, ``e``, ``q``) are supplied, the third is derived automatically.

An optional ``orbit_type`` column can supply explicit class labels.

    ``orbit_type`` (optional):
        - if supplied, this label is used directly instead of being
          derived from the orbital elements.
        - Must be one of the digest2 class abbreviations
          (``NEO``, ``MB1``, etc.).

**Trksub mapping CSV** — one row per tracklet, with columns:

    trksub,designation

    ``trksub``:
        - the tracklet sub-ID used in the observation file.
    ``designation``:
        - the object name in the ground-truth file.
"""

import csv
import json
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union

from digest2.population import CLASS_ABBR, CLASS_TESTS
from digest2.result import ClassificationResult


# ── Orbit-type derivation ─────────────────────────────────────────────

# The "primary" class is the most specific non-composite class that an
# orbit satisfies.  We walk the class list in reverse so that narrow
# classes (Hilda, Trojan, …) take precedence over broad ones (Int).

# Indices 0-3 (Int, NEO, N22, N18) are composites / subsets of NEO.
# When deriving a *single* primary label for ground truth we skip Int
# and the H-filtered NEO variants and assign "NEO" for any q < 1.3.

_PRIMARY_PRIORITY: List[int] = [
    14,  # JFC
    13,  # JTr
    12,  # Hil
    11,  # MB3
    10,  # MB2
    9,   # Han
    8,   # Pal
    7,   # MB1
    6,   # Pho
    5,   # Hun
    4,   # MC
    1,   # NEO  (catches everything with q < 1.3)
]


def classify_orbit(q: float, e: float, i: float, H: float) -> str:
    """Return the primary digest2 class abbreviation for an orbit.

    Note the possible orbit categories are non-overlapping:
     - we do not consider categories such as `Int` or `N22` when assigning a single primary label.

    Uses the same boundary definitions as the C scoring engine (``population.CLASS_TESTS``).

    If no specific class matches, returns ``"Other"``.
    """
    for idx in _PRIMARY_PRIORITY:
        if CLASS_TESTS[idx](q, e, i, H):
            return CLASS_ABBR[idx]
    return "Other"


def classify_orbit_all(q: float, e: float, i: float, H: float) -> List[str]:
    """Return *all* digest2 class abbreviations that match an orbit.

    N.B. An orbit can belong to multiple overlapping classes
    (e.g. NEO and N22 and Int simultaneously).
    """
    return [CLASS_ABBR[c] for c in range(len(CLASS_TESTS))
            if CLASS_TESTS[c](q, e, i, H)]


# ── Data containers ───────────────────────────────────────────────────

@dataclass
class GroundTruthRecord:
    """Ground truth for a single object.

    Construct with any two of ``a``, ``e``, ``q``,
    plus ``i`` and ``H``;
    the missing element is derived automatically using ``q = a * (1 - e)``.

    Pass ``None`` for any of ``a``, ``e``, ``q`` that should be derived
    from the other two.

    Attributes:
        designation: Object name / provisional designation.
        a: Semi-major axis (AU).
        e: Eccentricity.
        q: Perihelion distance (AU).
        i: Inclination (degrees).
        H: Absolute magnitude.
        orbit_type: Primary digest2 class label (derived or explicit).
        all_classes: All matching digest2 classes.
    """
    designation: str
    i: float
    H: float
    a: Optional[float] = None
    e: Optional[float] = None
    q: Optional[float] = None
    orbit_type: str = ""
    all_classes: List[str] = field(default_factory=list)

    def __post_init__(self):
        # Derive whichever of a, e, q is missing from the other two.
        # None means "not supplied"; 0.0 is a valid value (e.g. e=0
        # for a circular orbit).
        has_a = self.a is not None
        has_e = self.e is not None
        has_q = self.q is not None
        n_supplied = sum([has_a, has_e, has_q])

        if n_supplied < 2:
            raise ValueError(
                f"GroundTruthRecord '{self.designation}': need at least two "
                f"of (a, e, q) to derive the third. "
                f"Got a={self.a}, e={self.e}, q={self.q}."
            )

        if has_a and has_e and not has_q:
            # Derive q from a and e.
            self.q = self.a * (1.0 - self.e)
        elif has_q and has_e and not has_a:
            # Derive a from q and e.
            if self.e < 1.0:
                self.a = self.q / (1.0 - self.e)
            else:
                self.a = float("inf")  # parabolic
        elif has_a and has_q and not has_e:
            # Derive e from a and q.
            self.e = 1.0 - self.q / self.a if self.a > 0 else 0.0

        # If all three were supplied, nothing to derive.

        if not self.orbit_type:
            self.orbit_type = classify_orbit(self.q, self.e, self.i, self.H)
        if not self.all_classes:
            self.all_classes = classify_orbit_all(
                self.q, self.e, self.i, self.H)


# ── File loaders ──────────────────────────────────────────────────────

def load_ground_truth(filepath: str) -> Dict[str, GroundTruthRecord]:
    """Load ground-truth orbital elements from a CSV file.

    The CSV must have a header row.  Required columns: ``designation``,
    ``i``, ``H``, and at least two of ``a``, ``e``, ``q``.
    Optional column: ``orbit_type``.

    Supported orbital-element column combinations:

    * ``q``, ``e``        — ``a`` is derived as ``q / (1 - e)``
    * ``a``, ``e``        — ``q`` is derived as ``a * (1 - e)``
    * ``a``, ``q``        — ``e`` is derived as ``1 - q / a``
    * ``a``, ``q``, ``e`` — all three supplied directly

    Returns:
        Dict mapping designation -> GroundTruthRecord.
    """
    records: Dict[str, GroundTruthRecord] = {}
    with open(filepath, "r", newline="") as f:
        reader = csv.DictReader(f)

        if reader.fieldnames is None:
            raise ValueError("CSV file appears to be empty")

        cols = set(reader.fieldnames)

        # Always required
        always_required = {"designation", "i", "H"}
        missing_always = always_required - cols
        if missing_always:
            raise ValueError(
                f"Ground-truth CSV missing required columns: {missing_always}"
            )

        # Check that at least two of a, e, q are present
        orbital_cols = {"a", "e", "q"} & cols
        if len(orbital_cols) < 2:
            raise ValueError(
                f"Ground-truth CSV must contain at least two of "
                f"'a', 'e', 'q' (found: {orbital_cols or 'none'}). "
                f"Header: {reader.fieldnames}"
            )

        has_a = "a" in cols
        has_e = "e" in cols
        has_q = "q" in cols
        has_orbit_type = "orbit_type" in cols

        for row in reader:
            desig = row["designation"].strip()
            inc = float(row["i"])
            H = float(row["H"])

            a_val = float(row["a"]) if has_a else None
            e_val = float(row["e"]) if has_e else None
            q_val = float(row["q"]) if has_q else None

            orbit_type = (
                row["orbit_type"].strip()
                if has_orbit_type and row.get("orbit_type")
                else ""
            )

            rec = GroundTruthRecord(
                designation=desig,
                i=inc,
                H=H,
                a=a_val,
                e=e_val,
                q=q_val,
                orbit_type=orbit_type,
            )
            records[desig] = rec

    return records


def load_trksub_mapping(filepath: str) -> Dict[str, str]:
    """Load a trksub-to-designation mapping from a CSV file.

    The CSV must have columns ``trksub`` and ``designation``.

    Returns:
        Dict mapping trksub -> designation.
    """
    mapping: Dict[str, str] = {}
    with open(filepath, "r", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise ValueError("CSV file appears to be empty")
        required = {"trksub", "designation"}
        missing = required - set(reader.fieldnames)
        if missing:
            raise ValueError(f"Trksub mapping CSV missing columns: {missing}")

        for row in reader:
            trksub = row["trksub"].strip()
            desig = row["designation"].strip()
            mapping[trksub] = desig

    return mapping


# ── Matched result container ──────────────────────────────────────────

@dataclass
class MatchedResult:
    """A digest2 result paired with its ground truth.

    Attributes:
        trksub: Tracklet sub-ID from digest2 output.
        designation: Object designation from ground truth.
        true_class: Primary true orbit class abbreviation.
        true_all_classes: All true orbit classes.
        predicted_class: Top predicted class from digest2 (highest noid score).
        result: The full ClassificationResult object.
        truth: The full GroundTruthRecord object.
    """
    trksub: str
    designation: str
    true_class: str
    true_all_classes: List[str]
    predicted_class: str
    result: ClassificationResult
    truth: GroundTruthRecord


# ── Core evaluator ────────────────────────────────────────────────────

class TruthEvaluator:
    """Compare digest2 classification results against ground truth.

    Example::

        evaluator = TruthEvaluator(
            results=d2_results,
            ground_truth=load_ground_truth("truth.csv"),
            trksub_mapping=load_trksub_mapping("mapping.csv"),
        )

        # Summary metrics
        print(evaluator.summary())

        # Confusion matrix
        cm = evaluator.confusion_matrix()

        # Score distributions for true NEOs vs true non-NEOs
        dist = evaluator.score_distributions("NEO")

        # Per-class accuracy table
        table = evaluator.per_class_accuracy()

    Parameters:
        results: List of ClassificationResult from digest2.
        ground_truth: Dict mapping designation -> GroundTruthRecord.
        trksub_mapping: Optional dict mapping trksub -> designation.
            If None, the result's ``designation`` field is matched directly
            against ground-truth keys.
        threshold: Score threshold for binary classification (default 65).
        score_type: Which score to use: ``"noid"`` (default) or ``"raw"``.
    """

    def __init__(
        self,
        results: List[ClassificationResult],
        ground_truth: Dict[str, GroundTruthRecord],
        trksub_mapping: Optional[Dict[str, str]] = None,
        threshold: float = 65.0,
        score_type: str = "noid",
    ):
        self.results = results
        self.ground_truth = ground_truth
        self.trksub_mapping = trksub_mapping or {}
        self.threshold = threshold
        self.score_type = score_type

        # Match results to ground truth
        self.matched: List[MatchedResult] = []
        self.unmatched_results: List[ClassificationResult] = []
        self._match()

    def _match(self):
        """Pair each digest2 result with its ground truth record."""
        for result in self.results:
            trksub = result.designation.strip()

            # Resolve trksub -> designation
            if trksub in self.trksub_mapping:
                desig = self.trksub_mapping[trksub]
            else:
                desig = trksub

            if desig in self.ground_truth:
                truth = self.ground_truth[desig]
                self.matched.append(MatchedResult(
                    trksub=trksub,
                    designation=desig,
                    true_class=truth.orbit_type,
                    true_all_classes=truth.all_classes,
                    predicted_class=result.top_class,
                    result=result,
                    truth=truth,
                ))
            else:
                self.unmatched_results.append(result)

    def _get_score(self, result: ClassificationResult, cls: str) -> float:
        """Get the score for a class using the configured score_type."""
        scores = result.noid if self.score_type == "noid" else result.raw
        return scores[cls]

    # ── Summary metrics ───────────────────────────────────────────────

    def summary(self) -> Dict[str, Any]:
        """Return overall summary statistics.

        Returns:
            Dict with keys: total_results, matched, unmatched,
            true_class_distribution, overall_accuracy,
            top_class_accuracy.
        """
        if not self.matched:
            return {
                "total_results": len(self.results),
                "matched": 0,
                "unmatched": len(self.unmatched_results),
                "true_class_distribution": {},
                "overall_accuracy": 0.0,
                "top_class_accuracy": 0.0,
            }

        true_dist = Counter(m.true_class for m in self.matched)

        # top_class accuracy: predicted top class matches true class
        correct = sum(1 for m in self.matched
                      if m.predicted_class == m.true_class)
        top_acc = correct / len(self.matched)

        # overall accuracy: predicted top class is in the set of all
        # true classes (more lenient; accounts for overlapping classes)
        correct_any = sum(1 for m in self.matched
                          if m.predicted_class in m.true_all_classes)
        overall_acc = correct_any / len(self.matched)

        return {
            "total_results": len(self.results),
            "matched": len(self.matched),
            "unmatched": len(self.unmatched_results),
            "true_class_distribution": dict(true_dist),
            "overall_accuracy": round(overall_acc, 4),
            "top_class_accuracy": round(top_acc, 4),
        }

    # ── Confusion matrix ──────────────────────────────────────────────

    def confusion_matrix(
        self,
        labels: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Build a confusion matrix of true class vs predicted class.

        Parameters:
            labels: List of class abbreviations to include.
                Defaults to all classes present in the matched data.

        Returns:
            Dict with keys:
            - ``labels``: ordered list of class labels.
            - ``matrix``: 2D list, ``matrix[i][j]`` = count where
              true=labels[i], predicted=labels[j].
            - ``label_to_index``: dict mapping label -> index.
        """
        if labels is None:
            all_labels = set()
            for m in self.matched:
                all_labels.add(m.true_class)
                all_labels.add(m.predicted_class)
            # Sort: put digest2 standard classes first, then extras
            standard_order = {a: i for i, a in enumerate(CLASS_ABBR)}
            labels = sorted(all_labels,
                            key=lambda x: standard_order.get(x, 999))

        n = len(labels)
        label_to_idx = {lab: i for i, lab in enumerate(labels)}
        matrix = [[0] * n for _ in range(n)]

        for m in self.matched:
            ti = label_to_idx.get(m.true_class)
            pi = label_to_idx.get(m.predicted_class)
            if ti is not None and pi is not None:
                matrix[ti][pi] += 1

        return {
            "labels": labels,
            "matrix": matrix,
            "label_to_index": label_to_idx,
        }

    # ── Binary detection metrics for a single class ───────────────────

    def binary_metrics(self, target_class: str) -> Dict[str, Any]:
        """Compute binary detection metrics for a target class.

        An object is *predicted positive* if its digest2 score for
        ``target_class`` meets or exceeds ``self.threshold``.
        An object is *actually positive* if ``target_class`` is in
        its true class set (``all_classes``).

        Returns:
            Dict with keys: tp, fp, tn, fn, precision, recall, f1,
            accuracy, n_positive, n_negative, threshold.
        """
        tp = fp = tn = fn = 0

        for m in self.matched:
            score = self._get_score(m.result, target_class)
            predicted_positive = score >= self.threshold
            actually_positive = target_class in m.true_all_classes

            if predicted_positive and actually_positive:
                tp += 1
            elif predicted_positive and not actually_positive:
                fp += 1
            elif not predicted_positive and actually_positive:
                fn += 1
            else:
                tn += 1

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = (2 * precision * recall / (precision + recall)
              if (precision + recall) > 0 else 0.0)
        accuracy = (tp + tn) / len(self.matched) if self.matched else 0.0

        return {
            "tp": tp, "fp": fp, "tn": tn, "fn": fn,
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1": round(f1, 4),
            "accuracy": round(accuracy, 4),
            "n_positive": tp + fn,
            "n_negative": tn + fp,
            "threshold": self.threshold,
        }

    # ── Per-class accuracy table ──────────────────────────────────────

    def per_class_accuracy(
        self,
        classes: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """Compute detection metrics for each orbit class.

        Parameters:
            classes: List of class abbreviations to evaluate.
                Defaults to all standard digest2 classes.

        Returns:
            List of dicts, one per class, each containing the class
            abbreviation and the metrics from :meth:`binary_metrics`.
        """
        if classes is None:
            classes = list(CLASS_ABBR)

        table = []
        for cls in classes:
            metrics = self.binary_metrics(cls)
            metrics["class"] = cls
            table.append(metrics)
        return table

    # ── Score distributions ───────────────────────────────────────────

    def score_distributions(
        self,
        target_class: str,
    ) -> Dict[str, List[float]]:
        """Get score distributions for a target class split by true label.

        Returns:
            Dict with keys:
            - ``true_positive_scores``: scores for objects truly in
              target_class.
            - ``true_negative_scores``: scores for objects NOT truly in
              target_class.
        """
        tp_scores: List[float] = []
        tn_scores: List[float] = []

        for m in self.matched:
            score = self._get_score(m.result, target_class)
            if target_class in m.true_all_classes:
                tp_scores.append(score)
            else:
                tn_scores.append(score)

        return {
            "true_positive_scores": tp_scores,
            "true_negative_scores": tn_scores,
        }

    # ── Threshold sweep ───────────────────────────────────────────────

    def threshold_sweep(
        self,
        target_class: str,
        thresholds: Optional[List[float]] = None,
    ) -> List[Dict[str, Any]]:
        """Evaluate binary metrics across a range of thresholds.

        Useful for finding the optimal threshold or plotting ROC-like
        curves.

        Parameters:
            target_class: Class abbreviation to evaluate.
            thresholds: List of threshold values. Defaults to 0..100
                in steps of 5.

        Returns:
            List of dicts, each with ``threshold`` and the metrics
            from :meth:`binary_metrics`.
        """
        if thresholds is None:
            thresholds = [float(t) for t in range(0, 101, 5)]

        original = self.threshold
        results = []
        for t in thresholds:
            self.threshold = t
            metrics = self.binary_metrics(target_class)
            results.append(metrics)
        self.threshold = original
        return results

    # ── Misclassification details ─────────────────────────────────────

    def misclassified(
        self,
        target_class: str,
        kind: str = "fn",
    ) -> List[MatchedResult]:
        """Return misclassified objects for a target class.

        Parameters:
            target_class: Class abbreviation.
            kind: ``"fn"`` for false negatives (missed detections) or
                ``"fp"`` for false positives (false alarms).

        Returns:
            List of MatchedResult objects.
        """
        out = []
        for m in self.matched:
            score = self._get_score(m.result, target_class)
            predicted_positive = score >= self.threshold
            actually_positive = target_class in m.true_all_classes

            if kind == "fn" and actually_positive and not predicted_positive:
                out.append(m)
            elif kind == "fp" and not actually_positive and predicted_positive:
                out.append(m)
        return out

    # ── Plotting helpers ──────────────────────────────────────────────

    def plot_confusion_matrix(
        self,
        labels: Optional[List[str]] = None,
        ax: Optional[Any] = None,
        cmap: str = "Blues",
        normalize: bool = False,
        title: str = "Confusion Matrix",
    ) -> Any:
        """Plot the confusion matrix as a heatmap.

        Requires matplotlib.

        Parameters:
            labels: Class labels to include.
            ax: Matplotlib axes object.  Created if None.
            cmap: Colormap name.
            normalize: If True, normalize rows to sum to 1.
            title: Plot title.

        Returns:
            The matplotlib axes object.
        """
        import matplotlib.pyplot as plt
        import numpy as np

        cm_data = self.confusion_matrix(labels=labels)
        labels_list = cm_data["labels"]
        matrix = np.array(cm_data["matrix"], dtype=float)

        if normalize and matrix.sum() > 0:
            row_sums = matrix.sum(axis=1, keepdims=True)
            row_sums[row_sums == 0] = 1
            matrix = matrix / row_sums

        if ax is None:
            fig, ax = plt.subplots(figsize=(8, 6))

        im = ax.imshow(matrix, interpolation="nearest", cmap=cmap)
        ax.figure.colorbar(im, ax=ax)

        ax.set(
            xticks=range(len(labels_list)),
            yticks=range(len(labels_list)),
            xticklabels=labels_list,
            yticklabels=labels_list,
            ylabel="True class",
            xlabel="Predicted class",
            title=title,
        )
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
                 rotation_mode="anchor")

        fmt = ".2f" if normalize else "d"
        thresh = matrix.max() / 2.0
        for row_i in range(len(labels_list)):
            for col_j in range(len(labels_list)):
                val = matrix[row_i, col_j]
                ax.text(
                    col_j, row_i,
                    format(int(val), "d") if not normalize else format(val, ".2f"),
                    ha="center", va="center",
                    color="white" if val > thresh else "black",
                )

        ax.figure.tight_layout()
        return ax

    def plot_score_distribution(
        self,
        target_class: str,
        ax: Optional[Any] = None,
        bins: int = 20,
        title: Optional[str] = None,
    ) -> Any:
        """Plot score distributions for true positives vs true negatives.

        Requires matplotlib.

        Parameters:
            target_class: Class abbreviation.
            ax: Matplotlib axes object.  Created if None.
            bins: Number of histogram bins.
            title: Plot title (auto-generated if None).

        Returns:
            The matplotlib axes object.
        """
        import matplotlib.pyplot as plt

        dist = self.score_distributions(target_class)
        tp = dist["true_positive_scores"]
        tn = dist["true_negative_scores"]

        if ax is None:
            fig, ax = plt.subplots(figsize=(8, 5))

        if tp:
            ax.hist(tp, bins=bins, alpha=0.6, label=f"True {target_class}",
                    color="tab:red", edgecolor="black")
        if tn:
            ax.hist(tn, bins=bins, alpha=0.6, label=f"Not {target_class}",
                    color="tab:blue", edgecolor="black")

        ax.axvline(self.threshold, color="black", linestyle="--",
                   linewidth=1.5, label=f"Threshold ({self.threshold})")
        ax.set_xlabel(f"{target_class} {self.score_type} score")
        ax.set_ylabel("Count")
        ax.set_title(title or f"Score Distribution: {target_class}")
        ax.legend()
        ax.figure.tight_layout()
        return ax

    def plot_threshold_sweep(
        self,
        target_class: str,
        ax: Optional[Any] = None,
        title: Optional[str] = None,
    ) -> Any:
        """Plot precision, recall, and F1 across thresholds.

        Requires matplotlib.

        Parameters:
            target_class: Class abbreviation.
            ax: Matplotlib axes object.  Created if None.
            title: Plot title (auto-generated if None).

        Returns:
            The matplotlib axes object.
        """
        import matplotlib.pyplot as plt

        sweep = self.threshold_sweep(target_class)
        thresholds = [s["threshold"] for s in sweep]
        precisions = [s["precision"] for s in sweep]
        recalls = [s["recall"] for s in sweep]
        f1s = [s["f1"] for s in sweep]

        if ax is None:
            fig, ax = plt.subplots(figsize=(8, 5))

        ax.plot(thresholds, precisions, "o-", label="Precision", color="tab:blue")
        ax.plot(thresholds, recalls, "s-", label="Recall", color="tab:orange")
        ax.plot(thresholds, f1s, "^-", label="F1", color="tab:green")

        ax.axvline(self.threshold, color="black", linestyle="--",
                   linewidth=1.5, alpha=0.5,
                   label=f"Current threshold ({self.threshold})")
        ax.set_xlabel("Threshold")
        ax.set_ylabel("Score")
        ax.set_ylim(-0.05, 1.05)
        ax.set_title(title or f"Threshold Sweep: {target_class}")
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.figure.tight_layout()
        return ax

    def plot_per_class_f1(
        self,
        classes: Optional[List[str]] = None,
        ax: Optional[Any] = None,
        title: str = "Per-Class F1 Score",
    ) -> Any:
        """Bar chart of F1 scores for each orbit class.

        Requires matplotlib.

        Parameters:
            classes: Class abbreviations to include.
            ax: Matplotlib axes object.  Created if None.
            title: Plot title.

        Returns:
            The matplotlib axes object.
        """
        import matplotlib.pyplot as plt

        table = self.per_class_accuracy(classes=classes)
        # Filter to classes that have at least one true positive object
        table = [row for row in table if row["n_positive"] > 0]
        if not table:
            if ax is None:
                fig, ax = plt.subplots()
            ax.text(0.5, 0.5, "No classes with positive examples",
                    ha="center", va="center", transform=ax.transAxes)
            return ax

        labels = [row["class"] for row in table]
        f1s = [row["f1"] for row in table]

        if ax is None:
            fig, ax = plt.subplots(figsize=(10, 5))

        bars = ax.bar(labels, f1s, color="tab:green", edgecolor="black")
        ax.set_ylabel("F1 Score")
        ax.set_xlabel("Orbit Class")
        ax.set_title(title)
        ax.set_ylim(0, 1.1)

        for bar, val in zip(bars, f1s):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.02,
                    f"{val:.2f}", ha="center", va="bottom", fontsize=9)

        ax.figure.tight_layout()
        return ax

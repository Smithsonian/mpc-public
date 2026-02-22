"""Tests for the ground-truth evaluation module (digest2.truth)."""

import json
from pathlib import Path

import pytest

from digest2.population import CLASS_ABBR
from digest2.result import ClassificationResult, Scores
from digest2.truth import (
    GroundTruthRecord,
    MatchedResult,
    TruthEvaluator,
    classify_orbit,
    classify_orbit_all,
    load_ground_truth,
    load_trksub_mapping,
)


# ── Fixtures ──────────────────────────────────────────────────────────

# Representative orbital elements for each class.
# These are approximate values that should trigger each class test.
SAMPLE_ORBITS = {
    "neo":  {"q": 0.9,  "e": 0.4,  "i": 10.0, "H": 20.0},
    "mc":   {"q": 1.4,  "e": 0.35, "i": 10.0, "H": 18.0},
    "hun":  {"q": 1.55, "e": 0.15, "i": 22.0, "H": 16.0},
    "pho":  {"q": 1.7,  "e": 0.24, "i": 23.0, "H": 15.0},
    "mb1":  {"q": 1.8,  "e": 0.18, "i": 5.0,  "H": 17.0},
    "pal":  {"q": 1.8,  "e": 0.30, "i": 30.0, "H": 14.0},
    "han":  {"q": 2.0,  "e": 0.22, "i": 21.5, "H": 14.0},
    "mb2":  {"q": 2.0,  "e": 0.25, "i": 8.0,  "H": 15.0},
    "mb3":  {"q": 2.0,  "e": 0.35, "i": 10.0, "H": 13.0},
    "hil":  {"q": 2.5,  "e": 0.35, "i": 10.0, "H": 12.0},
    "jtr":  {"q": 4.2,  "e": 0.15, "i": 15.0, "H": 10.0},
    "jfc":  {"q": 1.5,  "e": 0.60, "i": 12.0, "H": 15.0},
}


@pytest.fixture
def ground_truth_csv(tmp_path):
    """Create a sample ground-truth CSV file."""
    csv_path = tmp_path / "truth.csv"
    lines = [
        "designation,q,e,i,H",
        "2024 AA,0.9,0.4,10.0,20.0",       # NEO
        "2024 BB,1.8,0.18,5.0,17.0",        # MB1
        "2024 CC,2.0,0.25,8.0,15.0",        # MB2
        "2024 DD,0.8,0.5,15.0,22.5",        # NEO
        "2024 EE,1.4,0.35,10.0,18.0",       # MC
    ]
    csv_path.write_text("\n".join(lines) + "\n")
    return str(csv_path)


@pytest.fixture
def ground_truth_with_type_csv(tmp_path):
    """Create a ground-truth CSV with explicit orbit_type column."""
    csv_path = tmp_path / "truth_typed.csv"
    lines = [
        "designation,q,e,i,H,orbit_type",
        "2024 AA,0.9,0.4,10.0,20.0,NEO",
        "2024 BB,1.8,0.18,5.0,17.0,MB1",
        "2024 CC,2.0,0.25,8.0,15.0,MB2",
    ]
    csv_path.write_text("\n".join(lines) + "\n")
    return str(csv_path)


@pytest.fixture
def trksub_mapping_csv(tmp_path):
    """Create a sample trksub mapping CSV."""
    csv_path = tmp_path / "mapping.csv"
    lines = [
        "trksub,designation",
        "T001,2024 AA",
        "T002,2024 BB",
        "T003,2024 CC",
        "T004,2024 DD",
        "T005,2024 EE",
    ]
    csv_path.write_text("\n".join(lines) + "\n")
    return str(csv_path)


def _make_result(designation: str, neo: float, mb1: float, mb2: float,
                 mc: float = 0.0) -> ClassificationResult:
    """Create a ClassificationResult with specified scores."""
    return ClassificationResult(
        raw=Scores(NEO=neo, MB1=mb1, MB2=mb2, MC=mc),
        noid=Scores(NEO=neo, MB1=mb1, MB2=mb2, MC=mc),
        rms=0.5,
        rms_prime=0.0,
        designation=designation,
    )


@pytest.fixture
def sample_results():
    """Create sample digest2 classification results."""
    return [
        _make_result("T001", neo=85, mb1=2, mb2=1),     # True NEO, predicted NEO
        _make_result("T002", neo=5, mb1=80, mb2=10),     # True MB1, predicted MB1
        _make_result("T003", neo=3, mb1=10, mb2=75),     # True MB2, predicted MB2
        _make_result("T004", neo=90, mb1=1, mb2=0),      # True NEO, predicted NEO
        _make_result("T005", neo=10, mb1=5, mb2=3, mc=70),  # True MC, predicted MC
    ]


@pytest.fixture
def misclassified_results():
    """Results where some classifications are wrong."""
    return [
        _make_result("T001", neo=85, mb1=2, mb2=1),     # True NEO, predicted NEO (correct)
        _make_result("T002", neo=70, mb1=20, mb2=5),     # True MB1, predicted NEO (wrong!)
        _make_result("T003", neo=3, mb1=10, mb2=75),     # True MB2, predicted MB2 (correct)
        _make_result("T004", neo=30, mb1=5, mb2=0),      # True NEO, predicted NEO (below threshold! fn)
        _make_result("T005", neo=10, mb1=5, mb2=3, mc=70),  # True MC, predicted MC (correct)
    ]


# ── Tests: classify_orbit ─────────────────────────────────────────────

class TestClassifyOrbit:
    """Test orbit classification from orbital elements."""

    def test_neo(self):
        assert classify_orbit(0.9, 0.4, 10.0, 20.0) == "NEO"

    def test_mars_crosser(self):
        assert classify_orbit(1.4, 0.35, 10.0, 18.0) == "MC"

    def test_mb1(self):
        assert classify_orbit(1.8, 0.18, 5.0, 17.0) == "MB1"

    def test_mb2(self):
        assert classify_orbit(2.0, 0.25, 8.0, 15.0) == "MB2"

    def test_mb3(self):
        result = classify_orbit(3.0, 0.05, 5.0, 13.0)
        assert result == "MB3"

    def test_jfc(self):
        result = classify_orbit(1.5, 0.60, 12.0, 15.0)
        assert result == "JFC"

    def test_other_fallback(self):
        # Very extreme orbit that doesn't match any specific class
        result = classify_orbit(50.0, 0.99, 170.0, 25.0)
        assert result == "Other"

    def test_classify_orbit_all_neo(self):
        """NEO orbit should match NEO, N22, and Int at minimum."""
        classes = classify_orbit_all(0.9, 0.4, 10.0, 20.0)
        assert "NEO" in classes
        assert "N22" in classes
        assert "Int" in classes

    def test_classify_orbit_all_mb1(self):
        """MB1 orbit should match MB1 and possibly Int."""
        classes = classify_orbit_all(1.8, 0.18, 5.0, 17.0)
        assert "MB1" in classes


# ── Tests: GroundTruthRecord ──────────────────────────────────────────

class TestGroundTruthRecord:
    """Test GroundTruthRecord dataclass."""

    def test_auto_classify(self):
        rec = GroundTruthRecord(
            designation="test", q=0.9, e=0.4, i=10.0, H=20.0
        )
        assert rec.orbit_type == "NEO"
        assert "NEO" in rec.all_classes
        assert "Int" in rec.all_classes

    def test_explicit_type(self):
        rec = GroundTruthRecord(
            designation="test", q=0.9, e=0.4, i=10.0, H=20.0,
            orbit_type="NEO"
        )
        assert rec.orbit_type == "NEO"

    def test_all_classes_populated(self):
        rec = GroundTruthRecord(
            designation="test", q=0.9, e=0.4, i=10.0, H=20.0
        )
        assert isinstance(rec.all_classes, list)
        assert len(rec.all_classes) > 0


# ── Tests: File loading ───────────────────────────────────────────────

class TestLoadGroundTruth:
    """Test ground truth CSV loading."""

    def test_load_basic(self, ground_truth_csv):
        records = load_ground_truth(ground_truth_csv)
        assert len(records) == 5
        assert "2024 AA" in records
        assert records["2024 AA"].orbit_type == "NEO"
        assert records["2024 BB"].orbit_type == "MB1"

    def test_load_with_orbit_type(self, ground_truth_with_type_csv):
        records = load_ground_truth(ground_truth_with_type_csv)
        assert records["2024 AA"].orbit_type == "NEO"
        assert records["2024 BB"].orbit_type == "MB1"

    def test_load_orbital_elements(self, ground_truth_csv):
        records = load_ground_truth(ground_truth_csv)
        rec = records["2024 AA"]
        assert rec.q == 0.9
        assert rec.e == 0.4
        assert rec.i == 10.0
        assert rec.H == 20.0

    def test_missing_column(self, tmp_path):
        bad_csv = tmp_path / "bad.csv"
        bad_csv.write_text("designation,q,e\ntest,0.9,0.4\n")
        with pytest.raises(ValueError, match="missing columns"):
            load_ground_truth(str(bad_csv))

    def test_empty_file(self, tmp_path):
        empty_csv = tmp_path / "empty.csv"
        empty_csv.write_text("")
        with pytest.raises(ValueError, match="empty"):
            load_ground_truth(str(empty_csv))


class TestLoadTrksubMapping:
    """Test trksub mapping CSV loading."""

    def test_load(self, trksub_mapping_csv):
        mapping = load_trksub_mapping(trksub_mapping_csv)
        assert mapping["T001"] == "2024 AA"
        assert mapping["T005"] == "2024 EE"
        assert len(mapping) == 5

    def test_missing_column(self, tmp_path):
        bad_csv = tmp_path / "bad.csv"
        bad_csv.write_text("trksub,name\nT001,test\n")
        with pytest.raises(ValueError, match="missing columns"):
            load_trksub_mapping(str(bad_csv))


# ── Tests: TruthEvaluator ────────────────────────────────────────────

class TestTruthEvaluator:
    """Test the main evaluator class."""

    @pytest.fixture
    def evaluator(self, sample_results, ground_truth_csv, trksub_mapping_csv):
        gt = load_ground_truth(ground_truth_csv)
        mapping = load_trksub_mapping(trksub_mapping_csv)
        return TruthEvaluator(
            results=sample_results,
            ground_truth=gt,
            trksub_mapping=mapping,
        )

    @pytest.fixture
    def evaluator_misclassified(self, misclassified_results,
                                 ground_truth_csv, trksub_mapping_csv):
        gt = load_ground_truth(ground_truth_csv)
        mapping = load_trksub_mapping(trksub_mapping_csv)
        return TruthEvaluator(
            results=misclassified_results,
            ground_truth=gt,
            trksub_mapping=mapping,
        )

    # ── Matching ──────────────────────────────────────────────────────

    def test_matching(self, evaluator):
        assert len(evaluator.matched) == 5
        assert len(evaluator.unmatched_results) == 0

    def test_unmatched(self, ground_truth_csv, trksub_mapping_csv):
        """Results with no ground truth match go to unmatched."""
        results = [_make_result("UNKNOWN", neo=50, mb1=30, mb2=20)]
        gt = load_ground_truth(ground_truth_csv)
        mapping = load_trksub_mapping(trksub_mapping_csv)
        ev = TruthEvaluator(results=results, ground_truth=gt,
                            trksub_mapping=mapping)
        assert len(ev.matched) == 0
        assert len(ev.unmatched_results) == 1

    def test_direct_designation_match(self, ground_truth_csv):
        """When no trksub mapping, match directly on designation."""
        results = [_make_result("2024 AA", neo=85, mb1=2, mb2=1)]
        gt = load_ground_truth(ground_truth_csv)
        ev = TruthEvaluator(results=results, ground_truth=gt)
        assert len(ev.matched) == 1
        assert ev.matched[0].designation == "2024 AA"

    # ── Summary ───────────────────────────────────────────────────────

    def test_summary(self, evaluator):
        s = evaluator.summary()
        assert s["total_results"] == 5
        assert s["matched"] == 5
        assert s["unmatched"] == 0
        assert "NEO" in s["true_class_distribution"]
        assert s["overall_accuracy"] > 0
        assert s["top_class_accuracy"] > 0

    def test_summary_perfect(self, evaluator):
        """With perfect predictions, accuracy should be 1.0."""
        s = evaluator.summary()
        assert s["top_class_accuracy"] == 1.0

    def test_summary_empty(self):
        ev = TruthEvaluator(results=[], ground_truth={})
        s = ev.summary()
        assert s["matched"] == 0
        assert s["overall_accuracy"] == 0.0

    # ── Confusion matrix ──────────────────────────────────────────────

    def test_confusion_matrix(self, evaluator):
        cm = evaluator.confusion_matrix()
        assert "labels" in cm
        assert "matrix" in cm
        assert len(cm["labels"]) > 0
        # Matrix is square
        n = len(cm["labels"])
        assert len(cm["matrix"]) == n
        for row in cm["matrix"]:
            assert len(row) == n

    def test_confusion_matrix_sums(self, evaluator):
        cm = evaluator.confusion_matrix()
        total = sum(sum(row) for row in cm["matrix"])
        assert total == len(evaluator.matched)

    def test_confusion_matrix_with_labels(self, evaluator):
        cm = evaluator.confusion_matrix(labels=["NEO", "MB1", "MB2"])
        assert cm["labels"] == ["NEO", "MB1", "MB2"]
        assert len(cm["matrix"]) == 3

    # ── Binary metrics ────────────────────────────────────────────────

    def test_binary_metrics_neo(self, evaluator):
        m = evaluator.binary_metrics("NEO")
        assert m["tp"] == 2  # 2024 AA and 2024 DD are NEOs, predicted NEO >= 65
        assert m["fn"] == 0  # All NEOs detected
        assert m["precision"] > 0
        assert m["recall"] > 0

    def test_binary_metrics_with_misclassification(self, evaluator_misclassified):
        m = evaluator_misclassified.binary_metrics("NEO")
        # T001 (true NEO, score 85) -> TP
        # T004 (true NEO, score 30) -> FN (below threshold 65)
        # T002 (true MB1, score 70) -> FP
        assert m["tp"] == 1
        assert m["fn"] == 1
        assert m["fp"] == 1

    def test_binary_metrics_mb1(self, evaluator):
        m = evaluator.binary_metrics("MB1")
        assert m["tp"] == 1  # 2024 BB
        assert m["recall"] == 1.0

    # ── Per-class accuracy ────────────────────────────────────────────

    def test_per_class_accuracy(self, evaluator):
        table = evaluator.per_class_accuracy()
        assert len(table) == len(CLASS_ABBR)
        assert all("class" in row for row in table)
        assert all("precision" in row for row in table)
        assert all("recall" in row for row in table)

    def test_per_class_accuracy_subset(self, evaluator):
        table = evaluator.per_class_accuracy(classes=["NEO", "MB1"])
        assert len(table) == 2
        assert table[0]["class"] == "NEO"
        assert table[1]["class"] == "MB1"

    # ── Score distributions ───────────────────────────────────────────

    def test_score_distributions(self, evaluator):
        dist = evaluator.score_distributions("NEO")
        assert "true_positive_scores" in dist
        assert "true_negative_scores" in dist
        # 2 true NEOs
        assert len(dist["true_positive_scores"]) == 2
        # 3 non-NEOs
        assert len(dist["true_negative_scores"]) == 3

    def test_score_values(self, evaluator):
        dist = evaluator.score_distributions("NEO")
        # True NEO scores should be high
        for score in dist["true_positive_scores"]:
            assert score >= 65
        # Non-NEO scores should be low
        for score in dist["true_negative_scores"]:
            assert score < 65

    # ── Threshold sweep ───────────────────────────────────────────────

    def test_threshold_sweep(self, evaluator):
        sweep = evaluator.threshold_sweep("NEO")
        assert len(sweep) > 0
        assert all("threshold" in s for s in sweep)
        assert all("precision" in s for s in sweep)
        # At threshold 0, recall should be 1.0 (everything is positive)
        zero_thresh = [s for s in sweep if s["threshold"] == 0][0]
        assert zero_thresh["recall"] == 1.0

    def test_threshold_sweep_custom(self, evaluator):
        sweep = evaluator.threshold_sweep("NEO", thresholds=[50.0, 65.0, 80.0])
        assert len(sweep) == 3

    def test_threshold_sweep_preserves_original(self, evaluator):
        original = evaluator.threshold
        evaluator.threshold_sweep("NEO")
        assert evaluator.threshold == original

    # ── Misclassified ─────────────────────────────────────────────────

    def test_misclassified_fn(self, evaluator_misclassified):
        fn = evaluator_misclassified.misclassified("NEO", kind="fn")
        # T004 has true NEO but score 30 < 65
        assert len(fn) == 1
        assert fn[0].trksub == "T004"

    def test_misclassified_fp(self, evaluator_misclassified):
        fp = evaluator_misclassified.misclassified("NEO", kind="fp")
        # T002 has true MB1 but NEO score 70 >= 65
        assert len(fp) == 1
        assert fp[0].trksub == "T002"

    def test_misclassified_none(self, evaluator):
        fn = evaluator.misclassified("NEO", kind="fn")
        assert len(fn) == 0


# ── Tests: Plotting (smoke tests) ────────────────────────────────────

class TestPlotting:
    """Smoke tests for plotting functions — just ensure they don't crash."""

    @pytest.fixture
    def evaluator(self, sample_results, ground_truth_csv, trksub_mapping_csv):
        gt = load_ground_truth(ground_truth_csv)
        mapping = load_trksub_mapping(trksub_mapping_csv)
        return TruthEvaluator(
            results=sample_results,
            ground_truth=gt,
            trksub_mapping=mapping,
        )

    @pytest.fixture(autouse=True)
    def _use_agg_backend(self):
        """Use non-interactive backend for CI/testing."""
        import matplotlib
        matplotlib.use("Agg")

    def test_plot_confusion_matrix(self, evaluator):
        import matplotlib.pyplot as plt
        ax = evaluator.plot_confusion_matrix()
        assert ax is not None
        plt.close("all")

    def test_plot_confusion_matrix_normalized(self, evaluator):
        import matplotlib.pyplot as plt
        ax = evaluator.plot_confusion_matrix(normalize=True)
        assert ax is not None
        plt.close("all")

    def test_plot_score_distribution(self, evaluator):
        import matplotlib.pyplot as plt
        ax = evaluator.plot_score_distribution("NEO")
        assert ax is not None
        plt.close("all")

    def test_plot_threshold_sweep(self, evaluator):
        import matplotlib.pyplot as plt
        ax = evaluator.plot_threshold_sweep("NEO")
        assert ax is not None
        plt.close("all")

    def test_plot_per_class_f1(self, evaluator):
        import matplotlib.pyplot as plt
        ax = evaluator.plot_per_class_f1()
        assert ax is not None
        plt.close("all")

    def test_plot_per_class_f1_with_subset(self, evaluator):
        import matplotlib.pyplot as plt
        ax = evaluator.plot_per_class_f1(classes=["NEO", "MB1", "MB2"])
        assert ax is not None
        plt.close("all")


# ── Tests: Edge cases ─────────────────────────────────────────────────

class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_raw_score_type(self, sample_results, ground_truth_csv,
                            trksub_mapping_csv):
        gt = load_ground_truth(ground_truth_csv)
        mapping = load_trksub_mapping(trksub_mapping_csv)
        ev = TruthEvaluator(
            results=sample_results,
            ground_truth=gt,
            trksub_mapping=mapping,
            score_type="raw",
        )
        m = ev.binary_metrics("NEO")
        assert "tp" in m

    def test_custom_threshold(self, sample_results, ground_truth_csv,
                              trksub_mapping_csv):
        gt = load_ground_truth(ground_truth_csv)
        mapping = load_trksub_mapping(trksub_mapping_csv)
        ev = TruthEvaluator(
            results=sample_results,
            ground_truth=gt,
            trksub_mapping=mapping,
            threshold=50.0,
        )
        m = ev.binary_metrics("NEO")
        assert m["threshold"] == 50.0

    def test_no_positive_examples(self, ground_truth_csv, trksub_mapping_csv):
        """Binary metrics for a class with no true positives."""
        results = [_make_result("T002", neo=5, mb1=80, mb2=10)]
        gt = load_ground_truth(ground_truth_csv)
        mapping = load_trksub_mapping(trksub_mapping_csv)
        ev = TruthEvaluator(results=results, ground_truth=gt,
                            trksub_mapping=mapping)
        m = ev.binary_metrics("JTr")
        assert m["tp"] == 0
        assert m["fn"] == 0
        assert m["recall"] == 0.0

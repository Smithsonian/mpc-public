"""
population.py — Python frontend for digest2 population model creation.

This module provides a pure-Python implementation of the pipeline that builds
the digest2 population model file (digest2.model.csv).  The pipeline is:

    S3M synthetic orbit files  -->  s3m.dat  -->  digest2.model.csv
         (via build_s3m)           (via build_model + astorb.dat)

This replaces the C programs s3mbin.c and muk.c with equivalent Python code,
so users can regenerate or update the population model without a C compiler.

Public domain.
"""

import math
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple

import numpy as np

# ---------------------------------------------------------------------------
# Constants (from d2model.h / d2model.c)
# ---------------------------------------------------------------------------

D2CLASSES = 15
QX = 29
EX = 8
IX = 11
HX = 18

QPART = np.array([
    0.4, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5,
    1.67, 1.8, 2.0, 2.2, 2.4, 2.6, 2.8, 3.0, 3.2, 3.5,
    4.0, 4.5, 5.0, 5.5, 10.0, 20.0, 30.0, 40.0, 100.0,
])

EPART = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.7, 0.9, 1.1])

IPART = np.array([2.0, 5.0, 10.0, 15.0, 20.0, 25.0, 30.0, 40.0,
                   60.0, 90.0, 180.0])

HPART = np.array([6.0, 8.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0,
                   17.0, 18.0, 19.0, 20.0, 21.0, 22.0, 23.0, 24.0, 25.5])

CLASS_HEADING = [
    "MPC interest.",
    "NEO(q < 1.3)",
    "NEO(H <= 22)",
    "NEO(H <= 18)",
    "Mars Crosser",
    "Hungaria gr.",
    "Phocaea group",
    "Inner MB",
    "Pallas group",
    "Hansa group",
    "Middle MB",
    "Outer MB",
    "Hilda group",
    "Jupiter tr.",
    "Jupiter Comet",
]

CLASS_ABBR = [
    "Int", "NEO", "N22", "N18", "MC",
    "Hun", "Pho", "MB1", "Pal", "Han",
    "MB2", "MB3", "Hil", "JTr", "JFC",
]

# ---------------------------------------------------------------------------
# Orbit class test functions (from d2model.c)
# ---------------------------------------------------------------------------

def is_mpcint(q: float, e: float, i: float, h: float) -> bool:
    """MPC interesting: q<1.3 OR e>=0.5 OR i>=40 OR Q>10."""
    if e >= 1.0:
        return True  # parabolic/hyperbolic — always interesting
    return q < 1.3 or e >= 0.5 or i >= 40.0 or q * (1.0 + e) / (1.0 - e) > 10.0


def is_neo(q: float, e: float, i: float, h: float) -> bool:
    """NEO: q < 1.3 AU."""
    return q < 1.3


def is_h22neo(q: float, e: float, i: float, h: float) -> bool:
    """NEO with H <= 22 (rounded)."""
    return q < 1.3 and h < 22.5


def is_h18neo(q: float, e: float, i: float, h: float) -> bool:
    """NEO with H <= 18 (rounded)."""
    return q < 1.3 and h < 18.5


def is_mars_crosser(q: float, e: float, i: float, h: float) -> bool:
    """Mars Crosser: 1.3 <= q < 1.67, Q > 1.58."""
    if e >= 1.0:
        return False
    return q < 1.67 and q >= 1.3 and q * (1 + e) / (1 - e) > 1.58


def is_hungaria(q: float, e: float, i: float, h: float) -> bool:
    """Hungaria group: 1.78 < a < 2.0, e < 0.18, 16 < i < 34."""
    if e > 0.18 or i < 16 or i > 34:
        return False
    if e >= 1.0:
        return False
    a = q / (1 - e)
    return 1.78 < a < 2.0


def is_phocaea(q: float, e: float, i: float, h: float) -> bool:
    """Phocaea group: q > 1.5, 2.2 < a < 2.45, 20 < i < 27."""
    if q < 1.5 or i < 20 or i > 27:
        return False
    if e >= 1.0:
        return False
    a = q / (1 - e)
    return 2.2 < a < 2.45


def is_inner_mb(q: float, e: float, i: float, h: float) -> bool:
    """Inner Main Belt: q > 1.67, 2.1 < a < 2.5, i limit varies."""
    if q < 1.67:
        return False
    if e >= 1.0:
        return False
    a = q / (1 - e)
    return 2.1 < a < 2.5 and i < ((a - 2.1) / 0.4) * 10 + 7


def is_pallas(q: float, e: float, i: float, h: float) -> bool:
    """Pallas group: 2.5 < a < 2.8, e < 0.35, 24 < i < 37."""
    if e > 0.35 or i < 24 or i > 37:
        return False
    if e >= 1.0:
        return False
    a = q / (1 - e)
    return 2.5 < a < 2.8


def is_hansa(q: float, e: float, i: float, h: float) -> bool:
    """Hansa group: 2.55 < a < 2.72, e < 0.25, 20 < i < 23.5."""
    if e > 0.25 or i < 20 or i > 23.5:
        return False
    if e >= 1.0:
        return False
    a = q / (1 - e)
    return 2.55 < a < 2.72


def is_mid_mb(q: float, e: float, i: float, h: float) -> bool:
    """Middle Main Belt: 2.5 < a < 2.8, e < 0.45, i < 20."""
    if e > 0.45 or i > 20:
        return False
    if e >= 1.0:
        return False
    a = q / (1 - e)
    return 2.5 < a < 2.8


def is_outer_mb(q: float, e: float, i: float, h: float) -> bool:
    """Outer Main Belt: 2.8 < a < 3.25, e < 0.4, i limit varies."""
    if e > 0.4:
        return False
    if e >= 1.0:
        return False
    a = q / (1 - e)
    return 2.8 < a < 3.25 and i < ((a - 2.8) / 0.45) * 16 + 20


def is_hilda(q: float, e: float, i: float, h: float) -> bool:
    """Hilda group: 3.9 < a < 4.02, e < 0.4, i < 18."""
    if i > 18 or e > 0.4:
        return False
    if e >= 1.0:
        return False
    a = q / (1 - e)
    return 3.9 < a < 4.02


def is_trojan(q: float, e: float, i: float, h: float) -> bool:
    """Jupiter Trojan: 5.05 < a < 5.35, e < 0.22, i < 38."""
    if e > 0.22 or i > 38:
        return False
    if e >= 1.0:
        return False
    a = q / (1 - e)
    return 5.05 < a < 5.35


def is_jfc(q: float, e: float, i: float, h: float) -> bool:
    """Jupiter Family Comet: 2 < Tj < 3, q >= 1.3."""
    if q < 1.3:
        return False
    if e >= 1.0:
        return False
    t = (5.2 * (1 - e) / q
         + 2 * math.sqrt(q * (1 + e) / 5.2) * math.cos(math.radians(i)))
    return 2 < t < 3


# Ordered list of class test functions — matches C isClass[] array
CLASS_TESTS: List[Callable[[float, float, float, float], bool]] = [
    is_mpcint, is_neo, is_h22neo, is_h18neo, is_mars_crosser,
    is_hungaria, is_phocaea, is_inner_mb, is_pallas, is_hansa,
    is_mid_mb, is_outer_mb, is_hilda, is_trojan, is_jfc,
]

# ---------------------------------------------------------------------------
# Binning functions (from d2model.c)
# ---------------------------------------------------------------------------

def h_to_bin(h: float) -> int:
    """Convert H magnitude to bin index (always returns a valid index)."""
    for ih in range(HX - 1):
        if h < HPART[ih]:
            return ih
    return HX - 1


def qei_to_bin(q: float, e: float, i: float) -> Optional[Tuple[int, int, int]]:
    """Convert (q, e, i) to bin indices.  Returns None if out of model."""
    iq = 0
    while q >= QPART[iq]:
        iq += 1
        if iq == QX:
            return None
    ie = 0
    while e >= EPART[ie]:
        ie += 1
        if ie == EX:
            return None
    ii = 0
    while i >= IPART[ii]:
        ii += 1
        if ii == IX:
            return None
    return (iq, ie, ii)


def qeih_to_bin(q: float, e: float, i: float,
                h: float) -> Optional[Tuple[int, int, int, int]]:
    """Convert (q, e, i, H) to 4-D bin indices.  Returns None if out of model."""
    result = qei_to_bin(q, e, i)
    if result is None:
        return None
    return (*result, h_to_bin(h))

# ---------------------------------------------------------------------------
# S3M file processing (equivalent to s3mbin.c)
# ---------------------------------------------------------------------------

def bin_s3m(filepath: str, clip_neo: bool = False) -> Tuple[np.ndarray, np.ndarray]:
    """Bin a single S3M synthetic orbit file.

    Parameters
    ----------
    filepath : str
        Path to an S3M .s3m file.
    clip_neo : bool
        If True, skip orbits with q < 1.3 (used for non-NEO S3M files
        to avoid double-counting NEOs).

    Returns
    -------
    all_ss : ndarray, shape (QX, EX, IX, HX)
        Binned count for solar-system-wide histogram.
    all_class : ndarray, shape (D2CLASSES, QX, EX, IX, HX)
        Binned count per orbit class.
    """
    all_ss = np.zeros((QX, EX, IX, HX))
    all_class = np.zeros((D2CLASSES, QX, EX, IX, HX))

    with open(filepath, "r") as f:
        for line in f:
            # Skip S3M comment lines
            if line.startswith("!!"):
                continue

            parts = line.split()
            # S3M format: id subid q e i node peri epoch H
            if len(parts) < 9:
                continue
            try:
                q = float(parts[2])
                e = float(parts[3])
                i = float(parts[4])
                h = float(parts[8])
            except (ValueError, IndexError):
                continue

            if q <= 0.0 or e < 0.0 or e > 1.1 or i < 0.0 or i >= 180.0:
                continue

            if clip_neo and q < 1.3:
                continue

            b = qeih_to_bin(q, e, i, h)
            if b is None:
                continue

            iq, ie, ii, ih = b
            all_ss[iq, ie, ii, ih] += 1

            for c in range(D2CLASSES):
                if CLASS_TESTS[c](q, e, i, h):
                    all_class[c, iq, ie, ii, ih] += 1

    return all_ss, all_class


def build_s3m(s3m_files: List[Tuple[str, bool]],
              output_path: str = "s3m.dat") -> Dict:
    """Process multiple S3M files and write s3m.dat.

    Parameters
    ----------
    s3m_files : list of (filepath, clip_neo) tuples
        Each entry is (path_to_s3m_file, clip_neo_flag).
    output_path : str
        Where to write the output s3m.dat file.

    Returns
    -------
    dict with keys 'total_orbits', 'class_counts'.
    """
    total_ss = np.zeros((QX, EX, IX, HX))
    total_class = np.zeros((D2CLASSES, QX, EX, IX, HX))

    for filepath, clip_neo in s3m_files:
        ss, cls = bin_s3m(filepath, clip_neo)
        total_ss += ss
        total_class += cls

    _write_s3m(output_path, total_ss, total_class)

    return {
        "total_orbits": int(total_ss.sum()),
        "class_counts": {CLASS_ABBR[c]: int(total_class[c].sum())
                         for c in range(D2CLASSES)},
    }


def _write_s3m(filepath: str, all_ss: np.ndarray,
               all_class: np.ndarray) -> None:
    """Write binned S3M data to s3m.dat format."""
    with open(filepath, "w") as f:
        f.write("S3M binned\n")

        f.write("q")
        for v in QPART:
            f.write(f" {v:g}")
        f.write("\ne")
        for v in EPART:
            f.write(f" {v:g}")
        f.write("\ni")
        for v in IPART:
            f.write(f" {v:g}")
        f.write("\nh")
        for v in HPART:
            f.write(f" {v:g}")
        f.write("\n")

        for iq in range(QX):
            for ie in range(EX):
                for ii in range(IX):
                    vals = " ".join(f"{all_ss[iq, ie, ii, ih]:g}"
                                    for ih in range(HX))
                    f.write(vals + " \n")

        for c in range(D2CLASSES):
            f.write(f"{CLASS_HEADING[c]}\n")
            for iq in range(QX):
                for ie in range(EX):
                    for ii in range(IX):
                        vals = " ".join(
                            f"{all_class[c, iq, ie, ii, ih]:g}"
                            for ih in range(HX))
                        f.write(vals + " \n")

# ---------------------------------------------------------------------------
# Reading s3m.dat (equivalent to the reading portion of muk.c)
# ---------------------------------------------------------------------------

def read_s3m(filepath: str) -> Tuple[np.ndarray, np.ndarray]:
    """Read a previously-built s3m.dat file.

    Returns
    -------
    all_ss : ndarray, shape (QX, EX, IX, HX)
    all_class : ndarray, shape (D2CLASSES, QX, EX, IX, HX)
    """
    with open(filepath, "r") as f:
        # Line 1: "S3M binned"
        header = f.readline().strip()
        if header != "S3M binned":
            raise ValueError(f"Unexpected s3m.dat header: {header!r}")

        # Lines 2-5: partition arrays (q, e, i, h) — validate but don't need
        for name, expected in [("q", QPART), ("e", EPART),
                                ("i", IPART), ("h", HPART)]:
            line = f.readline().strip()
            parts = line.split()
            if parts[0] != name:
                raise ValueError(
                    f"Expected partition '{name}', got '{parts[0]}'")

        # Read all_ss: QX*EX*IX rows, each with HX values
        all_ss = np.zeros((QX, EX, IX, HX))
        for iq in range(QX):
            for ie in range(EX):
                for ii in range(IX):
                    vals = []
                    while len(vals) < HX:
                        line = f.readline()
                        vals.extend(float(x) for x in line.split())
                    all_ss[iq, ie, ii, :] = vals[:HX]

        # Read per-class arrays
        all_class = np.zeros((D2CLASSES, QX, EX, IX, HX))
        for c in range(D2CLASSES):
            # Class heading line — may need to consume blank line first
            heading_line = f.readline().strip()
            # The C code does two fgets after all_ss data before checking heading;
            # the first may consume trailing whitespace from the numeric data.
            if not heading_line:
                heading_line = f.readline().strip()

            for iq in range(QX):
                for ie in range(EX):
                    for ii in range(IX):
                        vals = []
                        while len(vals) < HX:
                            line = f.readline()
                            vals.extend(float(x) for x in line.split())
                        all_class[c, iq, ie, ii, :] = vals[:HX]

    return all_ss, all_class

# ---------------------------------------------------------------------------
# Reading astorb.dat catalog (equivalent to catalog reading in muk.c)
# ---------------------------------------------------------------------------

def read_astorb(filepath: str) -> Tuple[np.ndarray, np.ndarray, Dict]:
    """Read an astorb.dat catalog and bin known objects.

    Parameters
    ----------
    filepath : str
        Path to the astorb.dat file.

    Returns
    -------
    known_ss : ndarray, shape (QX, EX, IX, HX)
    known_class : ndarray, shape (D2CLASSES, QX, EX, IX, HX)
    stats : dict with keys 'lines', 'parse_fails', 'out_of_model', 'usable'
    """
    known_ss = np.zeros((QX, EX, IX, HX))
    known_class = np.zeros((D2CLASSES, QX, EX, IX, HX))

    lines = 0
    parse_fails = 0
    out_of_model = 0
    usable = 0

    with open(filepath, "r") as f:
        for line in f:
            lines += 1

            # Fixed-format column extraction (matching muk.c exactly):
            #   H:    columns 42-46  (0-indexed, line[42:47])
            #   i:    columns 147-156 (line[147:157])
            #   e:    columns 158-167 (line[158:168])
            #   a:    columns 169-180 (line[169:181])
            try:
                h = float(line[42:47])
                i = float(line[147:157])
                e = float(line[158:168])
                a = float(line[169:181])
            except (ValueError, IndexError):
                parse_fails += 1
                continue

            q = a * (1 - e)
            b = qeih_to_bin(q, e, i, h)
            if b is None:
                out_of_model += 1
                continue

            usable += 1
            iq, ie, ii, ih = b
            known_ss[iq, ie, ii, ih] += 1

            for c in range(D2CLASSES):
                if CLASS_TESTS[c](q, e, i, h):
                    known_class[c, iq, ie, ii, ih] += 1

    return known_ss, known_class, {
        "lines": lines,
        "parse_fails": parse_fails,
        "out_of_model": out_of_model,
        "usable": usable,
    }

# ---------------------------------------------------------------------------
# Volume scaling + model assembly (equivalent to muk.c main)
# ---------------------------------------------------------------------------

def _volume_scale(all_ss: np.ndarray, known_ss: np.ndarray,
                  all_class: np.ndarray, known_class: np.ndarray):
    """Apply volume scaling and compute unk = (all - known) * isqv.

    Modifies arrays *in place* and returns (unk_ss, unk_class).
    After this call, all_ss and all_class have been scaled too.
    """
    unk_ss = np.zeros_like(all_ss)
    unk_class = np.zeros_like(all_class)

    q0 = 0.0
    for iq in range(QX):
        q1 = QPART[iq]
        dq = q1 - q0
        q0 = q1
        e0 = 0.0
        d1 = 1.0
        for ie in range(EX):
            e1 = EPART[ie]
            d0 = d1
            d1 = 1.0 - e1 if e1 < 1.0 else 0.0
            dae = dq * (e1 - e0) / (d0 + d1)
            e0 = e1
            i0 = 0.0
            for ii in range(IX):
                i1 = IPART[ii]
                daei = dae * (i1 - i0)
                i0 = i1
                h0 = 0.0
                for ih in range(HX):
                    h1 = HPART[ih]
                    isqv = 1.0 / math.sqrt(daei * (h1 - h0))
                    h0 = h1

                    unk_ss[iq, ie, ii, ih] = (
                        (all_ss[iq, ie, ii, ih]
                         - known_ss[iq, ie, ii, ih]) * isqv)
                    all_ss[iq, ie, ii, ih] *= isqv

                    for c in range(D2CLASSES):
                        unk_class[c, iq, ie, ii, ih] = (
                            (all_class[c, iq, ie, ii, ih]
                             - known_class[c, iq, ie, ii, ih]) * isqv)
                        all_class[c, iq, ie, ii, ih] *= isqv

    return unk_ss, unk_class

# ---------------------------------------------------------------------------
# CSV output (equivalent to mputclass / mheader in muk.c)
# ---------------------------------------------------------------------------

def write_model_csv(output_path: str,
                    all_ss: np.ndarray, unk_ss: np.ndarray,
                    all_class: np.ndarray, unk_class: np.ndarray) -> None:
    """Write the digest2.model.csv file.

    Parameters
    ----------
    output_path : str
        Destination CSV path.
    all_ss, unk_ss : ndarray, shape (QX, EX, IX, HX)
    all_class, unk_class : ndarray, shape (D2CLASSES, QX, EX, IX, HX)
    """
    with open(output_path, "w") as f:
        # Header
        hdr = "Model,Class,Q,e,i"
        for ih in range(HX):
            hdr += f",H{HPART[ih]:g}"
        f.write(hdr + "\n")

        def _write_section(mod: str, cls_label: str,
                           pop: np.ndarray) -> None:
            for iq in range(QX):
                for ie in range(EX):
                    for ii in range(IX):
                        line = (f"{mod},{cls_label},"
                                f"{QPART[iq]:g},{EPART[ie]:g},{IPART[ii]:g}")
                        for ih in range(HX):
                            v = pop[iq, ie, ii, ih]
                            if v == 0:
                                line += ","
                            else:
                                line += f",{v:.15g}"
                        f.write(line + "\n")

        _write_section("All", "SS", all_ss)
        _write_section("Unk", "SS", unk_ss)
        for c in range(D2CLASSES):
            _write_section("All", CLASS_ABBR[c], all_class[c])
            _write_section("Unk", CLASS_ABBR[c], unk_class[c])

# ---------------------------------------------------------------------------
# CSV reading (equivalent to readCSVClass in d2modelio.c)
# ---------------------------------------------------------------------------

def read_model_csv(filepath: str) -> Dict:
    """Read a digest2.model.csv file.

    Returns
    -------
    dict with keys:
        'all_ss', 'unk_ss' : ndarray (QX, EX, IX, HX)
        'all_class', 'unk_class' : ndarray (D2CLASSES, QX, EX, IX, HX)
    """
    all_ss = np.zeros((QX, EX, IX, HX))
    unk_ss = np.zeros((QX, EX, IX, HX))
    all_class = np.zeros((D2CLASSES, QX, EX, IX, HX))
    unk_class = np.zeros((D2CLASSES, QX, EX, IX, HX))

    # Build lookup for class abbreviation -> index
    abbr_to_idx = {a: i for i, a in enumerate(CLASS_ABBR)}

    with open(filepath, "r") as f:
        header = f.readline()  # skip header

        for line in f:
            parts = line.rstrip("\n").split(",")
            mod = parts[0]   # "All" or "Unk"
            cls = parts[1]   # "SS" or class abbreviation
            q_val = float(parts[2])
            e_val = float(parts[3])
            i_val = float(parts[4])

            # Find bin indices from partition values
            iq = _find_partition_index(QPART, q_val)
            ie = _find_partition_index(EPART, e_val)
            ii = _find_partition_index(IPART, i_val)

            h_vals = np.zeros(HX)
            for ih in range(HX):
                field = parts[5 + ih] if 5 + ih < len(parts) else ""
                h_vals[ih] = float(field) if field else 0.0

            if cls == "SS":
                if mod == "All":
                    all_ss[iq, ie, ii, :] = h_vals
                else:
                    unk_ss[iq, ie, ii, :] = h_vals
            else:
                c = abbr_to_idx[cls]
                if mod == "All":
                    all_class[c, iq, ie, ii, :] = h_vals
                else:
                    unk_class[c, iq, ie, ii, :] = h_vals

    return {
        "all_ss": all_ss,
        "unk_ss": unk_ss,
        "all_class": all_class,
        "unk_class": unk_class,
    }


def _find_partition_index(part: np.ndarray, value: float) -> int:
    """Find the index in a partition array matching a value (within tolerance)."""
    for idx in range(len(part)):
        if abs(part[idx] - value) < 1e-9:
            return idx
    raise ValueError(f"Value {value} not found in partition array")

# ---------------------------------------------------------------------------
# Main entry point: build_model (equivalent to muk.c main)
# ---------------------------------------------------------------------------

def build_model(s3m_path: str,
                catalog_path: str,
                output_path: str = "digest2.model.csv",
                catalog_format: str = "astorb") -> Dict:
    """Build digest2.model.csv from s3m.dat and an orbit catalog.

    This is the Python equivalent of muk.c.

    Parameters
    ----------
    s3m_path : str
        Path to s3m.dat (output of build_s3m or the C s3mbin program).
    catalog_path : str
        Path to the known-object catalog (e.g. astorb.dat).
    output_path : str
        Where to write the output CSV model file.
    catalog_format : str
        Format of the catalog.  Currently only "astorb" is supported.

    Returns
    -------
    dict with statistics: s3m_total, catalog_stats, output_path
    """
    # Step 1: read s3m.dat
    all_ss, all_class = read_s3m(s3m_path)
    s3m_total = int(all_ss.sum())

    # Step 2: read orbit catalog
    if catalog_format == "astorb":
        known_ss, known_class, cat_stats = read_astorb(catalog_path)
    else:
        raise ValueError(f"Unsupported catalog format: {catalog_format!r}")

    # Step 3: fix up — where known > all, set all = known
    mask = known_ss > all_ss
    all_ss[mask] = known_ss[mask]
    for c in range(D2CLASSES):
        mask_c = known_class[c] > all_class[c]
        all_class[c][mask_c] = known_class[c][mask_c]

    # Step 4: volume scaling
    unk_ss, unk_class = _volume_scale(all_ss, known_ss, all_class, known_class)

    # Step 5: write output
    write_model_csv(output_path, all_ss, unk_ss, all_class, unk_class)

    return {
        "s3m_total": s3m_total,
        "catalog_stats": cat_stats,
        "output_path": str(output_path),
    }

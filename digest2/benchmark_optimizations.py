#!/usr/bin/env python3
"""
Benchmark digest2 scoring performance: before vs after optimizations.

Uses git worktrees to build the pre-optimization code alongside the
current working-tree code, then times both on the same tracklets
using the Python API with sequential scoring (max_workers=1) to
isolate C-level performance differences.

Usage:
    python benchmark_optimizations.py [--baseline-ref origin/main] [--iterations 5]
"""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile


def build_extension(directory):
    """Build the C extension in the given digest2 directory."""
    build_dir = os.path.join(directory, "build")
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)

    # Remove old .so files
    src_dir = os.path.join(directory, "src", "digest2")
    for f in os.listdir(src_dir):
        if f.startswith("_extension") and f.endswith(".so"):
            os.remove(os.path.join(src_dir, f))

    result = subprocess.run(
        [sys.executable, "setup.py", "build_ext", "--inplace"],
        cwd=directory,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"Build failed in {directory}:")
        print(result.stderr)
        return False
    return True


def time_scoring(digest2_src_dir, obs_file, iterations, label, obscodes_path=None):
    """Import digest2 from a specific directory and time sequential scoring.

    Forces max_workers=1 if the API supports it to ensure an apples-to-apples
    comparison of C-level performance (not thread parallelism).
    Also prints per-tracklet scores so we can verify real work was done.
    """
    obscodes_init = (
        f"obscodes_path = {obscodes_path!r}" if obscodes_path
        else "obscodes_path = None"
    )

    script = f"""
import sys
import os
import time
import inspect

sys.path.insert(0, os.path.join({digest2_src_dir!r}, "src"))

for key in list(sys.modules.keys()):
    if key.startswith("digest2"):
        del sys.modules[key]

from digest2 import Digest2

obs_file = {obs_file!r}
iterations = {iterations!r}
{obscodes_init}

# Determine if classify_file accepts max_workers (not present in older code)
sig = inspect.signature(Digest2.classify_file)
has_max_workers = "max_workers" in sig.parameters
classify_kwargs = {{"max_workers": 1}} if has_max_workers else {{}}

# Warm-up run
with Digest2(obscodes_path=obscodes_path) as d2:
    _ = d2.classify_file(obs_file, **classify_kwargs)

# Timed runs
times = []
results = None
for _ in range(iterations):
    with Digest2(obscodes_path=obscodes_path) as d2:
        t0 = time.perf_counter()
        results = d2.classify_file(obs_file, **classify_kwargs)
        t1 = time.perf_counter()
        times.append(t1 - t0)

n_tracklets = len(results)
mean_t = sum(times) / len(times)
min_t = min(times)
max_t = max(times)
per_tracklet = mean_t / n_tracklets * 1000

print(f"RESULTS:{{n_tracklets}}:{{mean_t}}:{{min_t}}:{{max_t}}:{{per_tracklet}}")
print(f"MODE:{{'sequential (max_workers=1)' if has_max_workers else 'sequential (no parallel API)'}}")
for r in results:
    print(f"SCORE:{{r.designation}}:{{r.noid.NEO:.1f}}:{{r.noid.MB1:.1f}}")
"""
    result = subprocess.run(
        [sys.executable, "-c", script],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"Scoring failed for {label}:")
        print(result.stderr)
        return None

    parsed = {"scores": []}
    for line in result.stdout.strip().split("\n"):
        if line.startswith("RESULTS:"):
            parts = line.split(":")
            parsed["n_tracklets"] = int(parts[1])
            parsed["mean"] = float(parts[2])
            parsed["min"] = float(parts[3])
            parsed["max"] = float(parts[4])
            parsed["per_tracklet_ms"] = float(parts[5])
        elif line.startswith("MODE:"):
            parsed["mode"] = line[5:]
        elif line.startswith("SCORE:"):
            parts = line.split(":")
            parsed["scores"].append({
                "desig": parts[1],
                "NEO": float(parts[2]),
                "MB1": float(parts[3]),
            })

    if "n_tracklets" not in parsed:
        print(f"Scoring failed for {label}: no RESULTS line in output")
        print(result.stdout)
        return None

    return parsed


def main():
    parser = argparse.ArgumentParser(
        description="Benchmark digest2 C scoring optimizations (sequential only)"
    )
    parser.add_argument(
        "--baseline-ref",
        default="origin/main",
        help="Git ref for baseline (pre-optimization) code (default: origin/main)",
    )
    parser.add_argument(
        "--iterations",
        type=int,
        default=5,
        help="Number of timing iterations (default: 5)",
    )
    parser.add_argument(
        "--obs-file",
        default=None,
        help="Observation file to benchmark (default: three-hr-tracklets.obs)",
    )
    args = parser.parse_args()

    repo_root = os.path.dirname(os.path.abspath(__file__))
    digest2_dir = repo_root

    if args.obs_file:
        obs_file = os.path.abspath(args.obs_file)
    else:
        obs_file = os.path.join(digest2_dir, "digest2", "three-hr-tracklets.obs")

    if not os.path.exists(obs_file):
        print(f"Observation file not found: {obs_file}")
        sys.exit(1)

    obscodes_path = os.path.join(digest2_dir, "digest2", "digest2.obscodes")
    if not os.path.exists(obscodes_path):
        obscodes_path = None

    print("Benchmark: digest2 C scoring optimization comparison")
    print("  NOTE: All scoring is sequential (max_workers=1) to isolate")
    print("        C-level performance from thread parallelism.")
    print(f"  Baseline ref:  {args.baseline_ref}")
    print(f"  Obs file:      {obs_file}")
    print(f"  Iterations:    {args.iterations}")
    print()

    # --- Benchmark current (optimized) code ---
    print("Building CURRENT (optimized) code...")
    if not build_extension(digest2_dir):
        sys.exit(1)

    print("Timing CURRENT code...")
    current = time_scoring(digest2_dir, obs_file, args.iterations, "current",
                           obscodes_path=obscodes_path)
    if not current:
        sys.exit(1)

    print(
        f"  {current['n_tracklets']} tracklets, "
        f"mean={current['mean']:.3f}s, "
        f"per-tracklet={current['per_tracklet_ms']:.1f}ms "
        f"({current['mode']})"
    )
    print()

    # --- Build baseline in a temporary worktree ---
    repo_root_abs = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=digest2_dir,
        capture_output=True,
        text=True,
    ).stdout.strip()

    worktree_dir = tempfile.mkdtemp(prefix="d2bench_")
    worktree_path = os.path.join(worktree_dir, "mpc-public")

    print(f"Creating worktree for baseline ({args.baseline_ref})...")
    result = subprocess.run(
        ["git", "worktree", "add", "--detach", worktree_path, args.baseline_ref],
        cwd=repo_root_abs,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"Failed to create worktree: {result.stderr}")
        shutil.rmtree(worktree_dir, ignore_errors=True)
        sys.exit(1)

    baseline_digest2 = os.path.join(worktree_path, "digest2")

    try:
        print("Building BASELINE code...")
        if not build_extension(baseline_digest2):
            sys.exit(1)

        print("Timing BASELINE code...")
        baseline = time_scoring(
            baseline_digest2, obs_file, args.iterations, "baseline",
            obscodes_path=obscodes_path,
        )
        if not baseline:
            sys.exit(1)

        print(
            f"  {baseline['n_tracklets']} tracklets, "
            f"mean={baseline['mean']:.3f}s, "
            f"per-tracklet={baseline['per_tracklet_ms']:.1f}ms "
            f"({baseline['mode']})"
        )
        print()

        # --- Report ---
        speedup = baseline["mean"] / current["mean"]
        pct_faster = (1 - current["mean"] / baseline["mean"]) * 100

        print("=" * 60)
        print("RESULTS")
        print("=" * 60)
        print(f"  Baseline ({args.baseline_ref}):")
        print(f"    Total:        {baseline['mean']:.3f}s  (min={baseline['min']:.3f}s, max={baseline['max']:.3f}s)")
        print(f"    Per-tracklet: {baseline['per_tracklet_ms']:.1f}ms")
        print()
        print(f"  Current (optimized):")
        print(f"    Total:        {current['mean']:.3f}s  (min={current['min']:.3f}s, max={current['max']:.3f}s)")
        print(f"    Per-tracklet: {current['per_tracklet_ms']:.1f}ms")
        print()
        print(f"  Speedup: {speedup:.2f}x ({pct_faster:.1f}% faster)")
        print()

        # Score comparison
        print("  Score comparison (NEO / MB1):")
        max_diff = 0.0
        for b, c in zip(baseline["scores"], current["scores"]):
            neo_diff = abs(b["NEO"] - c["NEO"])
            mb1_diff = abs(b["MB1"] - c["MB1"])
            max_diff = max(max_diff, neo_diff, mb1_diff)
            flag = " *" if neo_diff > 0.5 or mb1_diff > 0.5 else ""
            print(
                f"    {b['desig']:15s}  "
                f"NEO: {b['NEO']:5.1f} -> {c['NEO']:5.1f} ({neo_diff:+.1f})  "
                f"MB1: {b['MB1']:5.1f} -> {c['MB1']:5.1f} ({mb1_diff:+.1f}){flag}"
            )
        print(f"  Max score difference: {max_diff:.1f}")
        print("=" * 60)

    finally:
        subprocess.run(
            ["git", "worktree", "remove", "--force", worktree_path],
            cwd=repo_root_abs,
            capture_output=True,
        )
        shutil.rmtree(worktree_dir, ignore_errors=True)


if __name__ == "__main__":
    main()

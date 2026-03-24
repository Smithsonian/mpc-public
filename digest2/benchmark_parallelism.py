#!/usr/bin/env python3
"""
Benchmark digest2 parallel scaling on the current branch.

Tests Python API at max_workers=1, 2, 4, and all cores, then
tests the C CLI at -u 1 and default (all cores) for comparison.

Usage:
    python benchmark_parallelism.py [--obs-file path] [--iterations N]
"""

import argparse
import os
import subprocess
import sys
import time


def find_obs_file(digest2_dir, obs_file_arg):
    if obs_file_arg:
        return os.path.abspath(obs_file_arg)
    default = os.path.join(digest2_dir, "digest2", "three-hr-tracklets.obs")
    if os.path.exists(default):
        return default
    sys.exit(f"Observation file not found: {default}")


def find_model_path(digest2_dir):
    bin_model = os.path.join(digest2_dir, "digest2", "digest2.model")
    if os.path.exists(bin_model):
        return bin_model
    csv_model = os.path.join(digest2_dir, "digest2", "digest2.model.csv")
    if os.path.exists(csv_model):
        return csv_model
    return None


def find_obscodes_path(digest2_dir):
    p = os.path.join(digest2_dir, "digest2", "digest2.obscodes")
    return p if os.path.exists(p) else None


def time_python_api(digest2_src_dir, obs_file, max_workers, iterations,
                    obscodes_path=None, model_path=None):
    """Time Python API at a given max_workers level via subprocess."""
    obscodes_init = (
        f"obscodes_path = {obscodes_path!r}" if obscodes_path else "obscodes_path = None"
    )
    model_init = (
        f"model_path = {model_path!r}" if model_path else "model_path = None"
    )
    script = f"""
import sys
import os
import time

sys.path.insert(0, os.path.join({digest2_src_dir!r}, "src"))
for key in list(sys.modules.keys()):
    if key.startswith("digest2"):
        del sys.modules[key]

from digest2 import Digest2

obs_file = {obs_file!r}
iterations = {iterations!r}
max_workers = {max_workers!r}
{obscodes_init}
{model_init}

init_kwargs = {{}}
if obscodes_path:
    init_kwargs["obscodes_path"] = obscodes_path
if model_path:
    init_kwargs["model_path"] = model_path

# Warm-up run
with Digest2(**init_kwargs) as d2:
    _ = d2.classify_file(obs_file, max_workers=max_workers)

# Timed runs
times = []
results = None
for _ in range(iterations):
    with Digest2(**init_kwargs) as d2:
        t0 = time.perf_counter()
        results = d2.classify_file(obs_file, max_workers=max_workers)
        t1 = time.perf_counter()
        times.append(t1 - t0)

n_tracklets = len(results)
mean_t = sum(times) / len(times)
min_t = min(times)
per_tracklet_ms = mean_t / n_tracklets * 1000

print(f"RESULTS:{{n_tracklets}}:{{mean_t:.4f}}:{{min_t:.4f}}:{{per_tracklet_ms:.3f}}")
"""
    result = subprocess.run(
        [sys.executable, "-c", script],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"  ERROR timing max_workers={max_workers}: {result.stderr[:200]}")
        return None

    for line in result.stdout.strip().split("\n"):
        if line.startswith("RESULTS:"):
            parts = line.split(":")
            return {
                "n_tracklets": int(parts[1]),
                "mean": float(parts[2]),
                "min": float(parts[3]),
                "per_tracklet_ms": float(parts[4]),
            }
    return None


def time_c_cli(binary, obs_file, n_threads):
    """Time the C CLI binary with the given number of threads.

    Must run from the binary's directory so digest2.model is found.
    """
    if not os.path.exists(binary):
        return None

    binary_dir = os.path.dirname(os.path.abspath(binary))
    binary_name = os.path.basename(binary)

    args = [f"./{binary_name}"]
    if n_threads is not None:
        args += ["-u", str(n_threads)]
    args.append(obs_file)

    # Warm-up
    subprocess.run(args, capture_output=True, cwd=binary_dir)

    times = []
    for _ in range(3):
        t0 = time.perf_counter()
        r = subprocess.run(args, capture_output=True, cwd=binary_dir)
        t1 = time.perf_counter()
        if r.returncode != 0:
            return None
        times.append(t1 - t0)

    mean_t = sum(times) / len(times)
    min_t = min(times)
    return {"mean": mean_t, "min": min_t}


def main():
    parser = argparse.ArgumentParser(
        description="Benchmark digest2 parallel scaling (Python API + C CLI)"
    )
    parser.add_argument("--obs-file", default=None,
                        help="Observation file (default: three-hr-tracklets.obs)")
    parser.add_argument("--iterations", type=int, default=3,
                        help="Python API timing iterations (default: 3)")
    args = parser.parse_args()

    repo_root = os.path.dirname(os.path.abspath(__file__))
    digest2_dir = repo_root

    obs_file = find_obs_file(digest2_dir, args.obs_file)
    model_path = find_model_path(digest2_dir)
    obscodes_path = find_obscodes_path(digest2_dir)
    c_binary = os.path.join(digest2_dir, "digest2", "digest2")

    try:
        import os as _os
        cpu_count = _os.cpu_count() or 4
    except Exception:
        cpu_count = 4

    worker_levels = sorted(set([1, 2, 4, cpu_count]))

    print("=" * 65)
    print("digest2 Parallel Scaling Benchmark")
    print("=" * 65)
    print(f"  Obs file:     {obs_file}")
    print(f"  CPU cores:    {cpu_count}")
    print(f"  Iterations:   {args.iterations} per worker level")
    print(f"  Model:        {model_path or '(bundled)'}")
    print()

    # ----------------------------------------------------------------
    # Python API benchmark
    # ----------------------------------------------------------------
    print("--- Python API (ThreadPoolExecutor, GIL-released C scoring) ---")
    print()

    py_results = {}
    for w in worker_levels:
        label = f"max_workers={w}"
        if w == cpu_count:
            label += f" (all cores)"
        print(f"  Timing {label}...", flush=True)
        r = time_python_api(
            digest2_dir, obs_file, w, args.iterations,
            obscodes_path=obscodes_path, model_path=model_path,
        )
        if r is None:
            print(f"  FAILED for max_workers={w}")
            continue
        py_results[w] = r
        print(f"    n_tracklets={r['n_tracklets']}, mean={r['mean']:.3f}s, "
              f"per-tracklet={r['per_tracklet_ms']:.1f}ms")

    if py_results:
        print()
        print(f"  {'workers':>8}  {'total(s)':>10}  {'ms/tracklet':>12}  {'speedup':>8}  {'efficiency':>10}")
        print(f"  {'-'*8}  {'-'*10}  {'-'*12}  {'-'*8}  {'-'*10}")

        baseline_mean = py_results.get(1, {}).get("mean")
        for w in worker_levels:
            if w not in py_results:
                continue
            r = py_results[w]
            if baseline_mean and baseline_mean > 0:
                speedup = baseline_mean / r["mean"]
                efficiency = speedup / w * 100
                speedup_str = f"{speedup:.2f}x"
                eff_str = f"{efficiency:.0f}%"
            else:
                speedup_str = "n/a"
                eff_str = "n/a"
            print(f"  {w:>8}  {r['mean']:>10.3f}  {r['per_tracklet_ms']:>12.1f}  "
                  f"{speedup_str:>8}  {eff_str:>10}")

        if 1 in py_results and cpu_count in py_results:
            best_speedup = py_results[1]["mean"] / py_results[cpu_count]["mean"]
            print()
            threshold = 4.0
            status = "PASS" if best_speedup >= threshold else "FAIL"
            print(f"  Max speedup ({cpu_count} workers vs 1): {best_speedup:.2f}x  [{status} — threshold >= {threshold}x]")

    # ----------------------------------------------------------------
    # C CLI benchmark
    # ----------------------------------------------------------------
    print()
    print("--- C CLI Binary ---")

    if not os.path.exists(c_binary):
        print(f"  C binary not found: {c_binary}")
        print("  Build with: cd digest2/digest2 && make")
    else:
        print()
        cli_results = {}

        print("  Timing -u 1 (single-threaded)...", flush=True)
        r1 = time_c_cli(c_binary, obs_file, 1)
        if r1:
            cli_results[1] = r1
            print(f"    mean={r1['mean']:.3f}s, min={r1['min']:.3f}s")

        print(f"  Timing default (all {cpu_count} cores)...", flush=True)
        rN = time_c_cli(c_binary, obs_file, None)
        if rN:
            cli_results["all"] = rN
            print(f"    mean={rN['mean']:.3f}s, min={rN['min']:.3f}s")

        if 1 in cli_results and "all" in cli_results:
            cli_speedup = cli_results[1]["mean"] / cli_results["all"]["mean"]
            threshold = 4.0
            status = "PASS" if cli_speedup >= threshold else "FAIL"
            print()
            print(f"  Speedup (all cores vs -u 1): {cli_speedup:.2f}x  [{status} — threshold >= {threshold}x]")

    print()
    print("=" * 65)


if __name__ == "__main__":
    main()

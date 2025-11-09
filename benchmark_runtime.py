#!/usr/bin/env python3
import argparse
import importlib
import random
import statistics
import time
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

import sys
sys.setrecursionlimit(300_000)

def gen_values(n, low=1, high=100000, seed=42):
    rnd = random.Random(seed)
    return [rnd.randint(low, high) for _ in range(n)]

def time_once(func, n, k, values):
    t0 = time.perf_counter()
    total, indices = func(n, k, values)
    t1 = time.perf_counter()
    return t1 - t0, total, indices

def time_trials(func, n, k, trials, seed_base=100):
    times = []
    for t in range(trials):
        values = gen_values(n, seed=seed_base + t)
        dt, total, _ = time_once(func, n, k, values)
        times.append(dt)
    return statistics.mean(times), (statistics.pstdev(times) if len(times) > 1 else 0.0)

def safe_import(module_name, func_name):
    mod = importlib.import_module(module_name)
    return getattr(mod, func_name)

def save_plot(x, y, title, xlabel, ylabel, outpath):
    plt.figure()
    plt.plot(x, y, marker='o')              # no explicit colors/styles
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    plt.savefig(outpath)
    plt.close()

def main():
    p = argparse.ArgumentParser(description="Benchmark Programs 3, 4A, 4B, 5 and generate plots.")
    p.add_argument("--trials", type=int, default=3)
    p.add_argument("--overlay_small_ns", nargs="+", type=int,
                   default=[10, 12, 14, 16, 18, 20, 22, 24])  # keep small for Program 3
    p.add_argument("--prog4_ns", nargs="+", type=int,
                   default=[5000, 10000, 20000, 30000, 40000, 50000])
    p.add_argument("--prog5_ns", nargs="+", type=int,
                   default=[10000, 20000, 50000, 80000, 100000])
    p.add_argument("--fixed_k", type=int, default=2)
    p.add_argument("--results_dir", default="results")
    p.add_argument("--plots_dir", default="plots")
    args = p.parse_args()

    results_dir = Path(args.results_dir); results_dir.mkdir(parents=True, exist_ok=True)
    plots_dir = Path(args.plots_dir); plots_dir.mkdir(parents=True, exist_ok=True)

    # Import your functions — must match filenames & function names in this folder
    program3  = safe_import("program3",  "program3")
    program4A = safe_import("program4A", "program4A")
    program4B = safe_import("program4B", "program4B")
    program5  = safe_import("program5",  "program5")

    # -------- Plot 3: Program 3 vs n (fixed k) --------
    import pandas as pd
    rows = []
    for n in args.overlay_small_ns:
        mean_t, std_t = time_trials(program3, n, args.fixed_k, trials=args.trials)
        rows.append({"n": n, "k": args.fixed_k, "mean_time_s": mean_t, "std_time_s": std_t})
    df = pd.DataFrame(rows)
    df.to_csv(results_dir / "plot3_program3_vs_n.csv", index=False)
    save_plot(df["n"], df["mean_time_s"],
              f"Plot 3: Program 3 Runtime vs n (k={args.fixed_k})", "n", "time (s)",
              plots_dir / "plot3_program3.png")

    # -------- Plot 4: Program 4A vs n (fixed k) --------
    rows = []
    for n in args.prog4_ns:
        mean_t, std_t = time_trials(program4A, n, args.fixed_k, trials=args.trials)
        rows.append({"n": n, "k": args.fixed_k, "mean_time_s": mean_t, "std_time_s": std_t})
    df = pd.DataFrame(rows)
    df.to_csv(results_dir / "plot4_program4A_vs_n.csv", index=False)
    save_plot(df["n"], df["mean_time_s"],
              f"Plot 4: Program 4A Runtime vs n (k={args.fixed_k})", "n", "time (s)",
              plots_dir / "plot4_program4A.png")

    # -------- Plot 5: Program 4B vs n (fixed k) --------
    rows = []
    for n in args.prog4_ns:
        mean_t, std_t = time_trials(program4B, n, args.fixed_k, trials=args.trials)
        rows.append({"n": n, "k": args.fixed_k, "mean_time_s": mean_t, "std_time_s": std_t})
    df = pd.DataFrame(rows)
    df.to_csv(results_dir / "plot5_program4B_vs_n.csv", index=False)
    save_plot(df["n"], df["mean_time_s"],
              f"Plot 5: Program 4B Runtime vs n (k={args.fixed_k})", "n", "time (s)",
              plots_dir / "plot5_program4B.png")

    # -------- Plot 6: Program 5 vs n (fixed k) --------
    rows = []
    for n in args.prog5_ns:
        mean_t, std_t = time_trials(program5, n, args.fixed_k, trials=args.trials)
        rows.append({"n": n, "k": args.fixed_k, "mean_time_s": mean_t, "std_time_s": std_t})
    df = pd.DataFrame(rows)
    df.to_csv(results_dir / "plot6_program5_vs_n.csv", index=False)
    save_plot(df["n"], df["mean_time_s"],
              f"Plot 6: Program 5 Runtime vs n (k={args.fixed_k})", "n", "time (s)",
              plots_dir / "plot6_program5.png")

    # -------- Plot 7: Overlay (Programs 3, 4A, 4B, 5) on small n --------
    rows = []
    def bench_series(fn, label, ns):
        xs, ys = [], []
        for n in ns:
            mean_t, std_t = time_trials(fn, n, args.fixed_k, trials=args.trials)
            xs.append(n); ys.append(mean_t)
            rows.append({"program": label, "n": n, "k": args.fixed_k,
                         "mean_time_s": mean_t, "std_time_s": std_t})
        return xs, ys
    xs3, ys3 = bench_series(program3,  "Program 3",  args.overlay_small_ns)
    xs4a, ys4a = bench_series(program4A, "Program 4A", args.overlay_small_ns)
    xs4b, ys4b = bench_series(program4B, "Program 4B", args.overlay_small_ns)
    xs5, ys5 = bench_series(program5,  "Program 5",  args.overlay_small_ns)
    pd.DataFrame(rows).to_csv(results_dir / "plot7_overlay_p3_p4a_p4b_p5.csv", index=False)

    plt.figure()
    plt.plot(xs3, ys3, marker='o', label="Program 3")
    plt.plot(xs4a, ys4a, marker='o', label="Program 4A")
    plt.plot(xs4b, ys4b, marker='o', label="Program 4B")
    plt.plot(xs5, ys5, marker='o', label="Program 5")
    plt.title(f"Plot 7: Overlay (k={args.fixed_k})")
    plt.xlabel("n"); plt.ylabel("time (s)")
    plt.legend()
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    plt.savefig(Path(args.plots_dir) / "plot7_overlay.png")
    plt.close()

    # -------- Plot 8: Overlay 4A vs 4B on bigger n --------
    rows = []
    xs4a2, ys4a2 = [], []
    for n in args.prog4_ns:
        mean_t, std_t = time_trials(program4A, n, args.fixed_k, trials=args.trials)
        xs4a2.append(n); ys4a2.append(mean_t)
        rows.append({"program":"Program 4A","n":n,"k":args.fixed_k,"mean_time_s":mean_t,"std_time_s":std_t})
    xs4b2, ys4b2 = [], []
    for n in args.prog4_ns:
        mean_t, std_t = time_trials(program4B, n, args.fixed_k, trials=args.trials)
        xs4b2.append(n); ys4b2.append(mean_t)
        rows.append({"program":"Program 4B","n":n,"k":args.fixed_k,"mean_time_s":mean_t,"std_time_s":std_t})
    pd.DataFrame(rows).to_csv(results_dir / "plot8_overlay_p4a_p4b.csv", index=False)

    plt.figure()
    plt.plot(xs4a2, ys4a2, marker='o', label="Program 4A")
    plt.plot(xs4b2, ys4b2, marker='o', label="Program 4B")
    plt.title(f"Plot 8: Overlay 4A vs 4B (k={args.fixed_k})")
    plt.xlabel("n"); plt.ylabel("time (s)")
    plt.legend()
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    plt.savefig(Path(args.plots_dir) / "plot8_overlay_4a_4b.png")
    plt.close()

    print("Done. CSVs in:", Path(args.results_dir).resolve())
    print("Plots in:", Path(args.plots_dir).resolve())

if __name__ == "__main__":
    main()

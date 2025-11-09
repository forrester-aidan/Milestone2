# plot9_quality.py
import random
from pathlib import Path
import statistics
import pandas as pd
import matplotlib.pyplot as plt

from program1 import program1      # Greedy (hg)
from program5 import program5      # Optimal (ho) for this plot

def gen_values(n, low=1, high=100000, seed=None):
    rnd = random.Random(seed)
    return [rnd.randint(low, high) for _ in range(n)]

def main():
    # --- CONFIG ---
    k = 2
    ns = [500, 1000, 1500, 2000, 2500]   # adjust if desired
    trials = 20
    base_seed = 4242
    # --------------

    # Folders
    results_dir = Path("results"); results_dir.mkdir(exist_ok=True)
    plots_dir   = Path("plots");   plots_dir.mkdir(exist_ok=True)

    rows = []
    print(f"[Plot9] k={k}, ns={ns}, trials={trials}")
    for n in ns:
        print(f"[Plot9] n={n} ...", flush=True)
        for t in range(trials):
            values = gen_values(n, seed=base_seed + n*31 + t)
            hg, _ = program1(n, k, values)   # greedy total
            ho, _ = program5(n, k, values)   # optimal total
            if ho == 0:
                ratio = 0.0
            else:
                ratio = (hg - ho) / ho       # can be negative if greedy < optimal
            rows.append({"n": n, "k": k, "trial": t, "hg": hg, "ho": ho, "ratio": ratio})

    # Save raw + summary CSVs
    df = pd.DataFrame(rows)
    df.to_csv(results_dir / "plot9_quality_raw.csv", index=False)
    summary = df.groupby("n", as_index=False).agg(
        mean_ratio=("ratio", "mean"),
        std_ratio=("ratio", "std")
    )
    summary.to_csv(results_dir / "plot9_quality.csv", index=False)

    # Plot mean ratio vs n (no blocking GUI)
    plt.figure(figsize=(7.5,4.5))
    plt.plot(summary["n"], summary["mean_ratio"], marker="o")
    plt.axhline(0, linestyle="--", linewidth=0.8)
    plt.title("Plot 9: Quality (hg − ho)/ho vs n (k=2)")
    plt.xlabel("n")
    plt.ylabel("(hg − ho)/ho")
    plt.grid(True, linestyle="--", linewidth=0.5, alpha=0.7)
    plt.tight_layout()
    out_png = plots_dir / "plot9_quality.png"
    plt.savefig(out_png, dpi=200)
    plt.close()

    print("Saved:", out_png)
    print("CSV:", results_dir / "plot9_quality.csv")

if __name__ == "__main__":
    main()

import random
import matplotlib.pyplot as plt
from program1 import program1
from program3 import program3
from program4A import program4A
from program4B import program4B
from program5 import program5
random.seed(42)


def compare_algorithms(ns, k=2, trials=5):
    rel_errors = {"3": [], "4A": [], "4B": [], "5": []}

    for n in ns:
        for _ in range(trials):
            values = [random.randint(1, 100) for _ in range(n)]

            # Baseline (optimal)
            opt_val, _ = program1(n, k, values)
            if opt_val == 0:
                continue

            # Compare other algorithms
            for label, func in [("3", program3), ("4A", program4A),
                                ("4B", program4B), ("5", program5)]:
                hg, _ = func(n, k, values)
                rel_err = abs(hg - opt_val) / opt_val
                rel_errors[label].append(rel_err)

    # Average across trials
    for key in rel_errors:
        rel_errors[key] = sum(rel_errors[key]) / len(rel_errors[key])

    return rel_errors

def plot_quality(rel_errors):
    labels = list(rel_errors.keys())
    errors = [rel_errors[k] for k in labels]

    plt.figure(figsize=(8,5))
    plt.bar(labels, errors, color=['skyblue', 'lightgreen', 'orange', 'salmon'])
    plt.title("Algorithm Output Quality Comparison")
    plt.ylabel("Average Relative Error ( (hg - ho) / ho )")
    plt.xlabel("Algorithm")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig("plot9_output_quality.png", dpi=300)
    plt.show()

if __name__ == "__main__":
    ns = [20, 40, 60, 80, 100]   # larger array sizes
    rel_errors = compare_algorithms(ns, k=2, trials=20)
    print("Average relative errors:", rel_errors)
    plot_quality(rel_errors)


import matplotlib.pyplot as plt
from sweep import WIDTHS, HEIGHTS, LENGTHS, FLOWS, run_sweep, filter_valid, find_pareto_front, best_under_constraint


def plot_pareto(all_valid, pareto_points, best_design=None):
    fig, ax = plt.subplots(figsize=(8, 6))

    ax.scatter(
        [p["dP_kPa"] for p in all_valid],
        [p["h_conv"] for p in all_valid],
        color="lightgray", s=10, label="All valid designs"
    )

    ax.scatter(
        [p["dP_kPa"] for p in pareto_points],
        [p["h_conv"] for p in pareto_points],
        color="steelblue", s=25, label="Pareto front"
    )

    if best_design is not None:
        ax.scatter(
            best_design["dP_kPa"], best_design["h_conv"],
            color="red", s=120, marker="*", label="Chosen design", zorder=5
        )

    ax.set_xlabel("Pressure drop (kPa)")
    ax.set_ylabel("h_conv (W/m^2*K)")
    ax.set_title("Cold plate design space: h_conv vs. pressure drop")
    ax.legend()
    plt.tight_layout()
    plt.show()


"""
if __name__ == "__main__":
    all_results = run_sweep(WIDTHS, HEIGHTS, LENGTHS, FLOWS)
    valid = filter_valid(all_results)
    pareto = find_pareto_front(valid)
    best = best_under_constraint(pareto, max_dP_kPa=50)  # placeholder, use your real pump budget

    plot_pareto(valid, pareto, best)
"""
import matplotlib.pyplot as plt
from sweep import WIDTHS, HEIGHTS, FLOWS, run_sweep, filter_valid, find_pareto_front, best_designs_under_constraint


def plot_pareto(all_valid, pareto_points, best_design=None):
    fig, (ax, list_ax) = plt.subplots(
        1, 2, figsize=(13, 6), gridspec_kw={"width_ratios": [3, 2]}
    )

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

    if best_design:
        for rank, design in enumerate(best_design, start=1):
            ax.plot(
                design["dP_kPa"], design["h_conv"],
                color="red", marker="*", markersize=16,
                linestyle="None", label="Top designs" if rank == 1 else None,
                zorder=5
            )
            ax.annotate(
                str(rank),
                (design["dP_kPa"], design["h_conv"]),
                xytext=(6, 6), textcoords="offset points",
                color="darkred", fontweight="bold"
            )

        list_ax.set_title("Starred designs", loc="left")
        list_ax.axis("off")
        list_ax.text(
            0, 0.96,
            "Rank   dP (kPa)   h_conv\n",
            transform=list_ax.transAxes,
            va="top", fontweight="bold", family="monospace"
        )
        for rank, design in enumerate(best_design, start=1):
            list_ax.text(
                0, 0.91 - (rank - 1) * 0.15,
                f"{rank:>4}   {design['dP_kPa']:>8.2f}   "
                f"{design['h_conv']:>8.0f}\n"
                f"      {design['width']} x {design['height']} mm, "
                f"{design['flow']} L/min",
                transform=list_ax.transAxes,
                va="top", family="monospace"
            )
    else:
        list_ax.axis("off")

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
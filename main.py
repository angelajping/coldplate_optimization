from sweep import WIDTHS, HEIGHTS, FLOWS, run_sweep, filter_valid, find_pareto_front, best_designs_under_constraint
from plot_results import plot_pareto

MAX_PUMP_PRESSURE_KPA = 50  # placeholder, replace with your actual pump's spec

def main():
    all_results = run_sweep(WIDTHS, HEIGHTS, FLOWS)
    valid = filter_valid(all_results)
    pareto = find_pareto_front(valid)
    best = best_designs_under_constraint(pareto, MAX_PUMP_PRESSURE_KPA)

    print(f"Total combinations: {len(all_results)}")
    print(f"Valid designs (Re >= 3000): {len(valid)}")
    print(f"Pareto-optimal designs: {len(pareto)}")

    if best:
        print("\nBest designs under pump constraint:")
        for rank, design in enumerate(best, start=1):
            print(f"\n  #{rank}")
            for key, value in design.items():
                print(f"    {key}: {value}")
    else:
        print("\nNo design satisfies the pressure constraint — loosen it or revisit your ranges.")

    plot_pareto(valid, pareto, best)

if __name__ == "__main__":
    main()
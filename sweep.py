import itertools
import numpy as np
from cold_plate_model import compute

WIDTHS = np.linspace(2, 40, 0.5)      # mm
HEIGHTS = np.linspace(2, 100, 0.5)     # mm
LENGTHS = np.linspace(100, 5000, 5)  # mm
FLOWS = np.linspace(1, 20, 1)       # L/min

def run_sweep(widths, heights, lengths, flows):
    results = []
    for w, h, L, flow in itertools.product(widths, heights, lengths, flows):
        r = compute(width_mm=w, height_mm=h, length_mm=L, flow_Lmin=flow)
        r["width"] = w
        r["height"] = h
        r["length"] = L
        r["flow"] = flow
        results.append(r)
    return results

def filter_valid(results):
    return [r for r in results if r["valid"]]

def find_pareto_front(results):
    pareto = []
    for point in results:
        dominated = False
        for other in results:
            if other["h_conv"] >= point["h_conv"] and other["dP_kPa"] <= point["dP_kPa"] \
               and (other["h_conv"] > point["h_conv"] or other["dP_kPa"] < point["dP_kPa"]):
                dominated = True
                break
        if not dominated:
            pareto.append(point)
    return pareto

def best_under_constraint(pareto_points, max_dP_kPa):
    feasible = [p for p in pareto_points if p["dP_kPa"] <= max_dP_kPa]
    if not feasible:
        return None
    return max(feasible, key=lambda p: p["h_conv"])

if __name__ == "__main__":
    all_results = run_sweep(WIDTHS, HEIGHTS, LENGTHS, FLOWS)
    valid = filter_valid(all_results)
    pareto = find_pareto_front(valid)

    print(f"Total combinations: {len(all_results)}")
    print(f"Valid (Re >= 3000): {len(valid)}")
    print(f"Pareto-optimal points: {len(pareto)}")

    best = best_under_constraint(pareto, max_dP_kPa=50)  # placeholder, use your real pump budget
    print("Best design under constraint:", best)
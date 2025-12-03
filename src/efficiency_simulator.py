"""Efficiency Simulator

Generates a simple grid of (O, T_visible, S) values and computes E_index.

Use this for:
    - quick intuition building
    - toy experiments on how entropy (S) affects efficiency

Example:
    python efficiency_simulator.py --output 10 --tmin 1 --tmax 10 --smin 1 --smax 5 --steps 20
"""

import argparse
import numpy as np
import csv
from pathlib import Path


def efficiency_index(o: float, t_visible: float, s: float) -> float:
    if t_visible <= 0 or s <= 0:
        return 0.0
    return o / (t_visible * s)


def main() -> None:
    parser = argparse.ArgumentParser(description="Simulate E_index over a grid of T_visible and S.")
    parser.add_argument("--output", type=float, default=10.0, help="Fixed output O for the simulation")
    parser.add_argument("--tmin", type=float, default=1.0, help="Minimum visible time")
    parser.add_argument("--tmax", type=float, default=10.0, help="Maximum visible time")
    parser.add_argument("--smin", type=float, default=1.0, help="Minimum entropy index")
    parser.add_argument("--smax", type=float, default=5.0, help="Maximum entropy index")
    parser.add_argument("--steps", type=int, default=25, help="Number of steps per axis")
    parser.add_argument("--out", type=str, default="data/simulated_grid.csv", help="Output CSV path")
    args = parser.parse_args()

    t_vals = np.linspace(args.tmin, args.tmax, args.steps)
    s_vals = np.linspace(args.smin, args.smax, args.steps)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with out_path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["O", "T_visible", "S", "E_index"])
        for t in t_vals:
            for s in s_vals:
                e_idx = efficiency_index(args.output, t, s)
                writer.writerow([args.output, t, s, e_idx])

    print(f"Saved simulated grid to {out_path.resolve()}")


if __name__ == "__main__":
    main()

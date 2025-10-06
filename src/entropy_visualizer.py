
"""Entropy Visualizer
Plots how E_true changes as entropy S and visible time T_visible vary.
Usage:
    python entropy_visualizer.py --output 10 --tmin 0.2 --tmax 5 --smin 0.2 --smax 5
This will save a PNG at diagrams/energy_vs_output_curve.png
"""
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

def compute_e_true(O, T, S):
    return O / (T * S)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=float, default=10.0, help='Output yield (O)')
    ap.add_argument('--tmin', type=float, default=0.5, help='Min T_visible')
    ap.add_argument('--tmax', type=float, default=5.0, help='Max T_visible')
    ap.add_argument('--smin', type=float, default=0.5, help='Min entropy S')
    ap.add_argument('--smax', type=float, default=5.0, help='Max entropy S')
    ap.add_argument('--steps', type=int, default=100, help='Steps per axis')
    ap.add_argument('--out', type=str, default='../diagrams/energy_vs_output_curve.png', help='Output PNG path')
    args = ap.parse_args()

    T = np.linspace(args.tmin, args.tmax, args.steps)
    S = np.linspace(args.smin, args.smax, args.steps)
    T_grid, S_grid = np.meshgrid(T, S)
    Z = compute_e_true(args.output, T_grid, S_grid)

    # 2D line slice at median S to keep a single plot (no subplots) and simple visualization
    s_mid_idx = args.steps // 2
    S_mid = S[s_mid_idx]
    E_slice = compute_e_true(args.output, T, S_mid)

    plt.figure()
    plt.plot(T, E_slice)
    plt.title(f"Efficiency vs Visible Time (S fixed at {S_mid:.2f}, O={args.output})")
    plt.xlabel("Visible Time (T_visible)")
    plt.ylabel("E_true")
    out_path = Path(__file__).parent / args.out
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, dpi=160, bbox_inches='tight')
    print(f"Saved plot to {out_path.resolve()}")

if __name__ == '__main__':
    main()

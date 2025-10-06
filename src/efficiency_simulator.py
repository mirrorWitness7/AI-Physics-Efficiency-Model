
"""Efficiency Simulator
Compute E_true = O / (T_visible * S) for single or batch inputs.
Usage:
    python efficiency_simulator.py --output 12 --time 3.0 --entropy 0.5
    python efficiency_simulator.py --csv data/sample_operator_cycles.csv
"""
import argparse
import sys
import pandas as pd
import numpy as np

def efficiency(o, t_visible, s):
    o = np.asarray(o, dtype=float)
    t_visible = np.asarray(t_visible, dtype=float)
    s = np.asarray(s, dtype=float)
    if np.any(t_visible <= 0) or np.any(s <= 0):
        raise ValueError("T_visible and S must be > 0 to avoid division by zero.")
    return o / (t_visible * s)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=float, help='Output yield (O)')
    ap.add_argument('--time', type=float, help='Visible time (T_visible)')
    ap.add_argument('--entropy', type=float, help='Entropy / scatter (S)')
    ap.add_argument('--csv', type=str, help='CSV with columns: cycle_id,phase,entropy,output,time(optional)')
    ap.add_argument('--time-default', type=float, default=1.0, help='Default T_visible if missing in CSV')
    args = ap.parse_args()

    if args.csv:
        df = pd.read_csv(args.csv)
        if 'time' not in df.columns:
            df['time'] = args.time_default
        # Validate columns
        for col in ['output','time','entropy']:
            if col not in df.columns:
                print(f"CSV is missing required column: {col}", file=sys.stderr)
                sys.exit(1)
        df['E_true'] = efficiency(df['output'], df['time'], df['entropy'])
        print(df.to_string(index=False))
        return

    if args.output is None or args.time is None or args.entropy is None:
        ap.print_help()
        sys.exit(0)

    e = efficiency(args.output, args.time, args.entropy)
    print(f"E_true = {e:.6f}")

if __name__ == '__main__':
    main()

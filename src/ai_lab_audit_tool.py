
"""AI Lab Audit Tool (Minimal)
Computes an audit score from simple inputs and emits a governance flag.
Usage:
    python ai_lab_audit_tool.py --output 12 --time 1.5 --entropy 0.8 --safety 0.9 --proportionality 0.85
Score formula (example):
    base = E_true = O / (T_visible * S)
    guard = (safety + proportionality) / 2
    score = base * guard
"""
import argparse

def efficiency(o, t_visible, s):
    if t_visible <= 0 or s <= 0:
        raise ValueError("T_visible and S must be > 0.")
    return o / (t_visible * s)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=float, required=True, help='Output yield (O)')
    ap.add_argument('--time', type=float, required=True, help='Visible time (T_visible)')
    ap.add_argument('--entropy', type=float, required=True, help='Entropy / scatter (S)')
    ap.add_argument('--safety', type=float, default=0.9, help='Safety coefficient [0..1]')
    ap.add_argument('--proportionality', type=float, default=0.9, help='Proportionality / guardrail fit [0..1]')
    args = ap.parse_args()

    e_true = efficiency(args.output, args.time, args.entropy)
    guard = (max(0.0, min(1.0, args.safety)) + max(0.0, min(1.0, args.proportionality))) / 2.0
    score = e_true * guard

    flag = "OK"
    if guard < 0.7:
        flag = "REVIEW-GUARDRAILS"
    if e_true < 1.0:
        flag = "LOW-EFFICIENCY" if flag == "OK" else flag + ";LOW-EFFICIENCY"

    print(f"E_true={e_true:.4f}  Guard={guard:.2f}  Score={score:.4f}  Flag={flag}")

if __name__ == '__main__':
    main()

## 2️⃣ `ai_lab_audit_tool.py`

```python
"""AI Lab Audit Tool (Minimal)

Computes a simple efficiency index from inputs and emits a soft governance flag.

Usage (example):
    python ai_lab_audit_tool.py \
        --output 12 --time 1.5 --entropy 2.0 \
        --safety 0.9 --proportionality 0.85 --mode execute

Model:
    E_index = O / (T_visible * S)
    guard   = (safety + proportionality) / 2
    score   = E_index * guard

Notes:
    - This is a heuristic dashboard metric, not a scientific law.
    - In EXPLORE mode, low E_index is not automatically “bad”.
"""

import argparse


def efficiency_index(o: float, t_visible: float, s: float) -> float:
    """Compute efficiency index E_index = O / (T_visible * S)."""
    if t_visible <= 0 or s <= 0:
        raise ValueError("T_visible and S must be > 0.")
    return o / (t_visible * s)


def audit_flag(score: float, mode: str) -> str:
    """
    Return a human-readable audit message.

    mode:
        - 'explore' : tolerate lower scores, focus on learning.
        - 'execute' : expect higher scores, focus on stability & delivery.
    """
    if mode not in {"explore", "execute"}:
        mode = "execute"

    if mode == "explore":
        # In exploration, we care more about *chronic* low scores.
        if score < 0.05:
            return "⚠️ Very low exploratory yield — check if questions are well-posed."
        elif score < 0.15:
            return "ℹ️ Normal for early exploration. Focus on clarity of hypotheses."
        else:
            return "✅ Strong exploratory yield — capture learnings and consolidate."
    else:  # execute
        if score < 0.05:
            return "🚨 Execution breakdown — high effort & scatter for little output."
        elif score < 0.15:
            return "⚠️ Inefficient execution — inspect meetings, priorities, and rework."
        elif score < 0.30:
            return "ℹ️ Acceptable but improvable — look for entropy sources to cut."
        else:
            return "✅ Efficient execution — protect current patterns and guardrails."


def main() -> None:
    parser = argparse.ArgumentParser(description="Minimal AI Lab Efficiency Audit Tool")
    parser.add_argument("--output", type=float, required=True, help="Output units (O)")
    parser.add_argument("--time", type=float, required=True, help="Visible time T_visible (hours, days, etc.)")
    parser.add_argument("--entropy", type=float, required=True, help="Entropy / scatter index S (1–5)")
    parser.add_argument("--safety", type=float, default=1.0, help="Safety score 0–1 (alignment, review, governance)")
    parser.add_argument("--proportionality", type=float, default=1.0,
                        help="Proportionality score 0–1 (risk vs. reward sanity)")
    parser.add_argument("--mode", type=str, default="execute",
                        help="Mode: 'explore' or 'execute' (defaults to 'execute')")
    args = parser.parse_args()

    e_idx = efficiency_index(args.output, args.time, args.entropy)
    guard = max(0.0, min(1.0, (args.safety + args.proportionality) / 2.0))
    score = e_idx * guard

    print(f"O = {args.output}")
    print(f"T_visible = {args.time}")
    print(f"S (entropy) = {args.entropy}")
    print(f"E_index = {e_idx:.4f}")
    print(f"Guardrail factor = {guard:.2f}")
    print(f"Composite score = {score:.4f}")
    print(audit_flag(score, args.mode))


if __name__ == "__main__":
    main()

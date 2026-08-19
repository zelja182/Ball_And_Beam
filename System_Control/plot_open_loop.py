"""Plot open-loop ball position: no servo, grey-box, black-box (nonlinear + linearized)."""

from __future__ import annotations

import os

import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams.update(
    {
        "font.family": "serif",
        "font.serif": ["Times New Roman", "DejaVu Serif"],
        "axes.unicode_minus": False,
    }
)

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data")

SERIES = [
    # (
    #     "ball_position_no_servo.csv",
    #     "nonlinear",
    #     "Нелинеарни модел; без серво мотора",
    #     "tab:blue",
    #     "-",
    # ),
    # (
    #     "ball_position_no_servo.csv",
    #     "linearized",
    #     "Линеаризовани модел; без серво мотора",
    #     "tab:orange",
    #     "-",
    # ),
    # (
    #     "servo_position_grey_box.csv",
    #     "nonlinear",
    #     "Нелинеарни модел",
    #     "tab:green",
    #     "-",
    # ),
    # (
    #     "servo_position_grey_box.csv",
    #     "linearized",
    #     "Линеаризовани модел",
    #     "tab:red",
    #     "-",
    # ),
    (
        "servo_position_black_box.csv",
        "nonlinear",
        "Нелинеарни модел",
        "tab:purple",
        "-",
    ),
    (
        "servo_position_black_box.csv",
        "linearized",
        "Линеаризовани модел",
        "tab:brown",
        "-",
    ),
]


def main() -> int:
    fig, ax = plt.subplots(figsize=(10, 5.5))

    for filename, column, label, color, style in SERIES:
        df = pd.read_csv(os.path.join(DATA_DIR, filename))
        ax.plot(df["time_s"], df[column], color=color, linestyle=style, label=label)

    ax.set_title("Промена угла серво мотора одређеног методом црне кутије")
    ax.set_xlabel("време [s]")
    ax.set_ylabel("угао серво мотора [°]")
    ax.set_xlim(0, 15)
    ax.set_ylim(-47, 47)
    ax.set_xticks(range(0, 16))
    ax.grid(True, alpha=0.35)
    ax.legend(loc="upper right", fontsize=8)

    out_path = os.path.join(DATA_DIR, "upravljanje_black_box_servo.png")
    fig.tight_layout()
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    print(f"Saved {out_path}")
    plt.show()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

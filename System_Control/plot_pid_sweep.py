"""Plot a MATLAB PID parameter sweep CSV: grey-box and black-box loops."""

from __future__ import annotations

import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

plt.rcParams.update(
    {
        "font.family": "serif",
        "font.serif": ["Times New Roman", "DejaVu Serif"],
        "axes.unicode_minus": False,
    }
)

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data")
FIG_DIR = os.path.join(DATA_DIR, "Slike")
CSV_PATH = os.path.join(DATA_DIR, "pid_sweep_r_0.csv")
SETPOINT_MM = 250.0
SWEEP_COLS = ("Kp", "Ki", "Kd", "r_0")

# Thesis figures: keep only representative sweep values (None = plot all).
SELECTED_VALUES = {
    "Kd": [-0.05, -0.1, -0.5, -1.5, -5.0],
    "Kp": [-0.05, -0.5, -2, -3, -5],
    "Ki": [-0.001, -0.01, -0.1, -0.4, -2],
}


def detect_sweep_param(df: pd.DataFrame) -> str:
    for name in SWEEP_COLS:
        if name in df.columns and df[name].nunique() > 1:
            return name
    return "Kd"


def ask_use_filter(sweep_param: str) -> bool:
    selected = SELECTED_VALUES.get(sweep_param)
    if not selected:
        print(f"No preset filter for {sweep_param}; plotting all values.")
        return False

    values_txt = ", ".join(f"{v:g}" for v in selected)
    while True:
        answer = input(
            f"Filter {sweep_param} to [{values_txt}]? [y/n]: "
        ).strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("Please answer y or n.")


def filter_selected(df: pd.DataFrame, sweep_param: str) -> pd.DataFrame:
    selected = SELECTED_VALUES.get(sweep_param)
    if not selected:
        return df
    mask = pd.Series(False, index=df.index)
    for value in selected:
        mask |= np.isclose(df[sweep_param], value)
    filtered = df.loc[mask].copy()
    if filtered.empty:
        raise ValueError(f"No rows matched SELECTED_VALUES[{sweep_param!r}] = {selected}")
    return filtered


def plot_sweep(df: pd.DataFrame, out_path: str, use_filter: bool = False) -> None:
    sweep_param = detect_sweep_param(df)
    selected = SELECTED_VALUES.get(sweep_param) if use_filter else None
    if use_filter and selected:
        df = filter_selected(df, sweep_param)
        values = list(selected)
    else:
        values = df[sweep_param].drop_duplicates().tolist()
    colors = plt.cm.tab10.colors

    fig, axes = plt.subplots(2, 2, sharex=True, figsize=(11, 7))
    (ax_pos_g, ax_pos_b), (ax_ang_g, ax_ang_b) = axes

    for ax in (ax_pos_g, ax_pos_b):
        ax.axhline(SETPOINT_MM, color="k", linestyle="--", linewidth=0.9)

    for i, value in enumerate(values):
        run = df[np.isclose(df[sweep_param], value)]
        if run.empty:
            continue
        color = colors[i % len(colors)]
        label = f"{sweep_param} = {value:g}"
        ax_pos_g.plot(run["time_s"], run["ball_grey"], color=color, label=label)
        ax_ang_g.plot(run["time_s"], run["servo_grey"], color=color, label=label)
        ax_pos_b.plot(run["time_s"], run["ball_black"], color=color, label=label)
        ax_ang_b.plot(run["time_s"], run["servo_black"], color=color, label=label)

    ax_pos_g.set_title("Сива кутија")
    ax_pos_b.set_title("Црна кутија")
    ax_pos_g.set_ylabel("позиција лопте [mm]")
    ax_pos_b.set_ylabel("позиција лопте [mm]")
    ax_ang_g.set_ylabel("угао мотора [°]")
    ax_ang_b.set_ylabel("угао мотора [°]")
    ax_ang_g.set_xlabel("време [s]")
    ax_ang_b.set_xlabel("време [s]")

    for ax in (ax_pos_g, ax_pos_b):
        ax.set_ylim(0, 450)
        ax.grid(True, alpha=0.35)
    for ax in (ax_ang_g, ax_ang_b):
        ax.set_ylim(-50, 50)
        ax.grid(True, alpha=0.35)
        ax.set_xlim(0, df["time_s"].max())

    ax_pos_g.legend(loc="best", fontsize=8)

    fixed = [name for name in ("Kp", "Ki", "Kd") if name in df.columns and name != sweep_param]
    fixed_txt = ", ".join(f"{name} = {df[name].iloc[0]:g}" for name in fixed)
    if sweep_param == "r_0":
        title = f"Симулација PID, промена почетног положаја $r_0$ ({fixed_txt})"
    else:
        title = f"Симулација PID, промена {sweep_param} ({fixed_txt})"
    fig.suptitle(title)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    print(f"Saved {out_path}")
    if os.environ.get("MPLBACKEND", "").lower() != "agg":
        plt.show()
    plt.close(fig)


def main() -> int:
    path = sys.argv[1] if len(sys.argv) > 1 else CSV_PATH
    df = pd.read_csv(path)
    sweep_param = detect_sweep_param(df)
    use_filter = ask_use_filter(sweep_param)
    os.makedirs(FIG_DIR, exist_ok=True)
    out_name = os.path.splitext(os.path.basename(path))[0] + ".png"
    plot_sweep(df, os.path.join(FIG_DIR, out_name), use_filter=use_filter)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

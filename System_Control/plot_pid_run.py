"""Plot a PID serial log: ball position and beam angle vs time."""

from __future__ import annotations

import os
import sys

import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams.update(
    {
        "font.family": "serif",
        "font.serif": ["Times New Roman", "DejaVu Serif"],
        "axes.unicode_minus": False,
    }
)

CSV_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "Data",
    "pid_run_20260819_204505.csv",
)


def load_run(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df = df.sort_index()
    df["time_s"] = df["time_ms"] / 1000.0
    # Drop wrap / leftover samples after a reset (time jumps backward).
    dt = df["time_s"].diff()
    cut = dt[dt < 0].index.min()
    if pd.notna(cut):
        df = df.loc[: cut - 1]
    df["time_s"] = df["time_s"] - df["time_s"].iloc[0]
    return df


def plot_run(df: pd.DataFrame, out_path: str) -> None:
    fig, (ax_pos, ax_ang) = plt.subplots(2, 1, sharex=True, figsize=(10, 6))

    ax_pos.plot(df["time_s"], df["distance_mm"], color="tab:blue")
    ax_pos.set_ylabel("позиција лопте [mm]")
    ax_pos.set_ylim(0, 450)
    ax_pos.grid(True, alpha=0.35)

    ax_ang.plot(df["time_s"], df["beam_deg"], color="tab:orange")
    ax_ang.set_xlabel("време [s]")
    ax_ang.set_ylabel("угао мотора [°]")
    ax_ang.set_ylim(-50, 50)
    ax_ang.grid(True, alpha=0.35)
    ax_ang.set_xlim(0, df["time_s"].iloc[-1])

    fig.suptitle("Стварни одзив система")
    fig.tight_layout()
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    print(f"Saved {out_path}")
    plt.show()


def main() -> int:
    path = sys.argv[1] if len(sys.argv) > 1 else CSV_PATH
    df = load_run(path)
    out_path = os.path.splitext(path)[0] + ".png"
    plot_run(df, out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

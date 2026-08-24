"""Compare the Simulink responses with the measured response of the real rig.

Produces the figures used in the model-verification chapter and prints the
metrics quoted in the text.
"""

from __future__ import annotations

import glob
import os

import matplotlib

matplotlib.use("Agg")
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

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "Data")
FIG = os.path.join(DATA, "Slike")

SETPOINT_MM = 250.0
TOLERANCE_MM = 5.0

BEST_RUN = os.path.join(DATA, "Data_experiment_1", "pid_run_20260822_130913.csv")
EXP1_DIR = os.path.join(DATA, "Data_experiment_1")
EXP2_DIR = os.path.join(DATA, "Data_experiment_2")
GREY_CSV = os.path.join(DATA, "grey_box_data_final.csv")
BLACK_CSV = os.path.join(DATA, "black_box_data_final.csv")
SWEEP_CSV = os.path.join(DATA, "pid_sweep_r_0.csv")

# Four paired comparisons: r_0 matches the measured initial ball position.
PAIRS = [
    (380, "pid_run_20260822_130913.csv"),
    (379, "pid_run_20260822_131000.csv"),
    (71, "pid_run_20260822_131243.csv"),
    (70, "pid_run_20260822_131159.csv"),
]


def load_run(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["time_s"] = df["time_ms"] / 1000.0
    dt = df["time_s"].diff()
    cut = dt[dt < 0].index.min()
    if pd.notna(cut):
        df = df.loc[: cut - 1]
    df["time_s"] = df["time_s"] - df["time_s"].iloc[0]

    # Inside the dead zone the sketch commands 0 deg but logs the previous
    # angle, so the recorded command is reconstructed here.
    inside = (df["distance_mm"] - SETPOINT_MM).abs() <= TOLERANCE_MM
    df.loc[inside, "beam_deg"] = 0.0
    return df


def load_sim(path: str) -> pd.DataFrame:
    # The Simulink logger keeps the sweep column names; the first signal is the
    # beam angle and the second the ball position.
    df = pd.read_csv(path)
    return df.rename(columns={df.columns[1]: "beam_deg", df.columns[2]: "distance_mm"})


def band_entry(t: np.ndarray, y: np.ndarray, band: float, hold: float = 1.0) -> float:
    """First time the ball enters the band and stays inside it for `hold` s."""
    inside = np.abs(y - SETPOINT_MM) <= band
    for i in range(len(t)):
        if inside[i] and np.all(inside[i : np.searchsorted(t, t[i] + hold)]):
            return t[i]
    return np.nan


def command_period(t: np.ndarray, u: np.ndarray, threshold: float = 20.0) -> float:
    """Mean time between excursions of the command beyond +-threshold."""
    starts = np.where(np.diff((np.abs(u) > threshold).astype(int)) == 1)[0]
    return np.mean(np.diff(t[starts])) if len(starts) > 2 else np.nan


def metrics(t: np.ndarray, y: np.ndarray, u: np.ndarray) -> dict:
    from_above = y[0] > SETPOINT_MM
    crossed = np.where((y < SETPOINT_MM) if from_above else (y > SETPOINT_MM))[0]
    crossed = crossed[t[crossed] > 0.3]
    t_cross = t[crossed[0]] if len(crossed) else np.nan

    if len(crossed):
        win = (t >= t_cross) & (t <= t_cross + 2.0)
        peak = np.min(y[win]) if from_above else np.max(y[win])
        overshoot = abs(peak - SETPOINT_MM)
    else:
        overshoot = np.nan

    ss = t >= 8.0
    return {
        "t_cross": t_cross,
        "t20": band_entry(t, y, 20.0),
        "t10": band_entry(t, y, 10.0),
        "t5": band_entry(t, y, 5.0),
        "overshoot": overshoot,
        "y_ss": y[ss].mean(),
        "bias": y[ss].mean() - SETPOINT_MM,
        "ripple": y[ss].std(),
        "u_std": u.std(),
        "sat": 100.0 * np.mean(np.abs(u) >= 44.5),
        "period": command_period(t, u),
        "iae": np.trapezoid(np.abs(SETPOINT_MM - y), t),
    }


def figure_comparison() -> None:
    run = load_run(BEST_RUN)
    grey = load_sim(GREY_CSV)
    black = load_sim(BLACK_CSV)

    fig, (ax_pos, ax_ang) = plt.subplots(2, 1, sharex=True, figsize=(10, 6))

    for df, label, style in (
        (run, "експеримент", dict(color="tab:blue", lw=1.4)),
        (grey, "симулација (сива кутија)", dict(color="tab:red", lw=1.4, ls="--")),
        (black, "симулација (црна кутија)", dict(color="tab:green", lw=1.4, ls="-.")),
    ):
        ax_pos.plot(df["time_s"], df["distance_mm"], label=label, **style)
        ax_ang.plot(df["time_s"], df["beam_deg"], **style)

    ax_pos.axhline(SETPOINT_MM, color="k", ls=":", lw=1)
    ax_pos.axhspan(
        SETPOINT_MM - TOLERANCE_MM, SETPOINT_MM + TOLERANCE_MM, color="k", alpha=0.08
    )
    ax_pos.set_ylabel("позиција лопте [mm]")
    ax_pos.set_ylim(0, 450)
    ax_pos.grid(True, alpha=0.35)
    ax_pos.legend(loc="upper right", fontsize=9)

    ax_ang.set_ylabel("угао мотора [°]")
    ax_ang.set_xlabel("време [s]")
    ax_ang.set_ylim(-50, 50)
    ax_ang.grid(True, alpha=0.35)
    ax_ang.set_xlim(0, 15)

    fig.suptitle("Поређење симулације и одзива реалног система")
    fig.tight_layout()
    out = os.path.join(FIG, "poredjenje_simulacija_eksperiment.png")
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("saved", out)

    print("\n--- poredjenje ---")
    head = (
        f"{'':<12}{'t20':>6}{'t10':>6}{'t5':>6}{'preskok':>9}{'y_ss':>8}{'oscil.':>10}"
        f"{'u std':>7}{'zasic.':>8}{'perioda':>9}{'IAE':>6}"
    )
    print(head)
    for name, df in (
        ("eksperiment", run),
        ("siva kutija", grey),
        ("crna kutija", black),
    ):
        m = metrics(
            df["time_s"].values, df["distance_mm"].values, df["beam_deg"].values
        )
        print(
            f"{name:<12}{m['t20']:>6.2f}{m['t10']:>6.2f}{m['t5']:>6.2f}{m['overshoot']:>9.1f}"
            f"{m['y_ss']:>8.1f}{m['ripple']:>10.2f}{m['u_std']:>7.1f}{m['sat']:>8.1f}"
            f"{m['period']:>9.2f}{m['iae']:>6.0f}"
        )


def figure_simulations() -> None:
    """Simulated ball position only, both models."""
    grey = load_sim(GREY_CSV)
    black = load_sim(BLACK_CSV)

    fig, ax = plt.subplots(figsize=(10, 4.2))
    ax.plot(grey["time_s"], grey["distance_mm"], color="tab:red", lw=1.4, label="сива кутија")
    ax.plot(
        black["time_s"],
        black["distance_mm"],
        color="tab:green",
        lw=1.4,
        ls="--",
        label="црна кутија",
    )
    ax.axhline(SETPOINT_MM, color="k", ls=":", lw=1)
    ax.axhspan(
        SETPOINT_MM - TOLERANCE_MM, SETPOINT_MM + TOLERANCE_MM, color="k", alpha=0.08
    )
    ax.set_ylabel("позиција лопте [mm]")
    ax.set_xlabel("време [s]")
    ax.set_ylim(200, 400)
    ax.set_xlim(0, 15)
    ax.grid(True, alpha=0.35)
    ax.legend(loc="upper right", fontsize=9)

    fig.suptitle("Симулирани одзив система са изабраним параметрима регулатора")
    fig.tight_layout()
    out = os.path.join(FIG, "odziv_simulacija.png")
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("saved", out)


def figure_repeatability() -> None:
    files = sorted(glob.glob(os.path.join(EXP1_DIR, "*.csv")))
    fig, ax_pos = plt.subplots(figsize=(10, 4.2))

    stats = []
    for path in files:
        df = load_run(path)
        ax_pos.plot(df["time_s"], df["distance_mm"], lw=0.9, alpha=0.85)
        ss = df["time_s"] >= 6.0
        stats.append(
            (
                df.loc[ss, "distance_mm"].mean() - SETPOINT_MM,
                df.loc[ss, "distance_mm"].std(),
                100.0 * (df.loc[ss, "distance_mm"].sub(SETPOINT_MM).abs() <= 5).mean(),
            )
        )

    ax_pos.axhline(SETPOINT_MM, color="k", ls=":", lw=1)
    ax_pos.axhspan(
        SETPOINT_MM - TOLERANCE_MM, SETPOINT_MM + TOLERANCE_MM, color="k", alpha=0.08
    )
    ax_pos.set_ylabel("позиција лопте [mm]")
    ax_pos.set_xlabel("време [s]")
    ax_pos.set_ylim(0, 450)
    ax_pos.set_xlim(0, 15)
    ax_pos.grid(True, alpha=0.35)

    fig.suptitle("Понављивост: десет узастопних експеримената")
    fig.tight_layout()
    out = os.path.join(FIG, "ponovljivost_eksperimenata.png")
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("saved", out)

    arr = np.array(stats)
    print("\n--- ponovljivost (10 eksperimenata, t > 6 s) ---")
    print(f"odstupanje srednje vrednosti : {arr[:,0].mean():+5.1f} mm (od {arr[:,0].min():+.1f} do {arr[:,0].max():+.1f})")
    print(f"oscilovanje (std)            : {arr[:,1].mean():5.1f} mm")
    print(f"vreme u zoni +-5 mm          : {arr[:,2].mean():5.1f} %")


def disturbance_events(t: np.ndarray, y: np.ndarray) -> list[tuple[float, float, float]]:
    """Return (t_peak, peak deviation, recovery time) for each large excursion."""
    e = np.abs(y - SETPOINT_MM)
    events, i = [], 0
    while i < len(t):
        if e[i] <= 80:
            i += 1
            continue
        j = i
        while j < len(t) and e[j] > 20:
            j += 1
        seg = slice(i, j)
        k = i + int(np.argmax(e[seg]))
        if j < len(t):
            events.append((t[k], e[k], t[j] - t[k]))
        i = j + 1
    return events


def figure_disturbance() -> None:
    files = sorted(glob.glob(os.path.join(EXP2_DIR, "*.csv")))
    ref = load_run(files[0])

    fig, (ax_pos, ax_ang) = plt.subplots(2, 1, sharex=True, figsize=(10, 6))
    ax_pos.plot(ref["time_s"], ref["distance_mm"], color="tab:blue", lw=1.3)
    ax_pos.axhline(SETPOINT_MM, color="k", ls=":", lw=1)
    ax_pos.axhspan(
        SETPOINT_MM - TOLERANCE_MM, SETPOINT_MM + TOLERANCE_MM, color="k", alpha=0.08
    )
    ax_pos.set_ylabel("позиција лопте [mm]")
    ax_pos.set_ylim(0, 450)
    ax_pos.grid(True, alpha=0.35)

    ax_ang.plot(ref["time_s"], ref["beam_deg"], color="tab:orange", lw=0.9)
    ax_ang.set_ylabel("угао мотора [°]")
    ax_ang.set_xlabel("време [s]")
    ax_ang.set_ylim(-50, 50)
    ax_ang.grid(True, alpha=0.35)
    ax_ang.set_xlim(0, ref["time_s"].iloc[-1])

    fig.suptitle("Одзив система на спољашњи поремећај")
    fig.tight_layout()
    out = os.path.join(FIG, "odziv_na_poremecaj.png")
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("saved", out)

    print("\n--- spoljasnji poremecaj (Data_experiment_2) ---")
    peaks, recov, n = [], [], 0
    for path in files:
        df = load_run(path)
        ev = disturbance_events(df["time_s"].values, df["distance_mm"].values)
        n += len(ev)
        peaks += [e[1] for e in ev]
        recov += [e[2] for e in ev]
        print(
            f"{os.path.basename(path)[8:-4]}: {len(ev)} poremecaja, "
            f"max odstupanje {max([e[1] for e in ev], default=float('nan')):.0f} mm, "
            f"oporavak {np.mean([e[2] for e in ev]) if ev else float('nan'):.1f} s"
        )
    print(
        f"ukupno {n} poremecaja: odstupanje {np.mean(peaks):.0f} +- {np.std(peaks):.0f} mm, "
        f"vreme oporavka {np.mean(recov):.1f} +- {np.std(recov):.1f} s"
    )


def mse(y_ref: np.ndarray, y_model: np.ndarray) -> float:
    """Mean squared error, same definition as MATLAB immse()."""
    return float(np.mean((y_ref - y_model) ** 2))


def resample_to(t_src: np.ndarray, y_src: np.ndarray, t_dst: np.ndarray) -> np.ndarray:
    return np.interp(t_dst, t_src, y_src)


def load_sweep_run(path: str, r0: float) -> tuple[pd.DataFrame, pd.DataFrame]:
    df = pd.read_csv(path)
    run = df[np.isclose(df["r_0"], r0)].copy()
    if run.empty:
        raise ValueError(f"No sweep rows for r_0 = {r0}")
    grey = run[["time_s", "servo_grey", "ball_grey"]].rename(
        columns={"servo_grey": "beam_deg", "ball_grey": "distance_mm"}
    )
    black = run[["time_s", "servo_black", "ball_black"]].rename(
        columns={"servo_black": "beam_deg", "ball_black": "distance_mm"}
    )
    return grey.reset_index(drop=True), black.reset_index(drop=True)


def figure_paired_comparison() -> None:
    """One thesis figure: 2x2 panels, each experiment vs both simulations."""
    fig, axes = plt.subplots(2, 2, sharex=True, sharey=True, figsize=(11, 7))
    axes = axes.ravel()

    print("\n--- poredjenje 4 para (eksperiment vs simulacija) ---")
    print(
        f"{'r0':>5} {'exp':>8} {'MSE_siva':>10} {'MSE_crna':>10} "
        f"{'MSE_s0-4':>10} {'MSE_c0-4':>10} "
        f"{'t10_e':>6} {'t10_s':>6} {'t10_c':>6}"
    )

    for ax, (r0, exp_name) in zip(axes, PAIRS):
        exp = load_run(os.path.join(EXP1_DIR, exp_name))
        grey, black = load_sweep_run(SWEEP_CSV, r0)

        ax.plot(
            exp["time_s"],
            exp["distance_mm"],
            color="tab:blue",
            lw=1.4,
            label="експеримент",
        )
        ax.plot(
            grey["time_s"],
            grey["distance_mm"],
            color="tab:red",
            lw=1.3,
            label="сива кутија",
        )
        ax.plot(
            black["time_s"],
            black["distance_mm"],
            color="tab:green",
            lw=1.3,
            ls="--",
            label="црна кутија",
        )
        ax.axhline(SETPOINT_MM, color="k", ls=":", lw=0.9)
        ax.axhspan(
            SETPOINT_MM - TOLERANCE_MM,
            SETPOINT_MM + TOLERANCE_MM,
            color="k",
            alpha=0.07,
        )
        ax.set_title(f"$r_0 = {r0:g}\\,\\mathrm{{mm}}$")
        ax.grid(True, alpha=0.35)
        ax.set_xlim(0, 15)
        ax.set_ylim(0, 450)

        t_e = exp["time_s"].values
        y_e = exp["distance_mm"].values
        y_g = resample_to(grey["time_s"].values, grey["distance_mm"].values, t_e)
        y_b = resample_to(black["time_s"].values, black["distance_mm"].values, t_e)
        m = t_e <= 4.0
        mse_g = mse(y_e, y_g)
        mse_b = mse(y_e, y_b)
        mse_g4 = mse(y_e[m], y_g[m])
        mse_b4 = mse(y_e[m], y_b[m])
        t10_e = band_entry(t_e, y_e, 10)
        t10_g = band_entry(grey["time_s"].values, grey["distance_mm"].values, 10)
        t10_b = band_entry(black["time_s"].values, black["distance_mm"].values, 10)
        print(
            f"{r0:5.0f} {exp_name[17:-4]:>8} {mse_g:10.1f} {mse_b:10.1f} "
            f"{mse_g4:10.1f} {mse_b4:10.1f} "
            f"{t10_e:6.2f} {t10_g:6.2f} {t10_b:6.2f}"
        )

    axes[0].legend(loc="upper right", fontsize=8)
    axes[0].set_ylabel("позиција лопте [mm]")
    axes[2].set_ylabel("позиција лопте [mm]")
    axes[2].set_xlabel("време [s]")
    axes[3].set_xlabel("време [s]")

    fig.suptitle("Поређење симулације и експеримента за четири почетна услова")
    fig.tight_layout()
    out = os.path.join(FIG, "poredjenje_4_pocetna.png")
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("saved", out)


def main() -> int:
    os.makedirs(FIG, exist_ok=True)
    figure_paired_comparison()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

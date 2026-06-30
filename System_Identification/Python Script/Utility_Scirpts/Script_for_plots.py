from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from thesis_plot_style import (
    ANGLE_LABEL,
    TEXT_WIDTH_IN,
    TIME_LABEL,
    apply_style,
    row_height,
    save_figure,
)

# --- configuration ---
TESTS_PER_GROUP = 5
GROUP_INDICES = None
ROWS_PER_PAGE = 4  # 4 angle groups per A4 landscape page

SAVE_FIGURES = True
OUTPUT_DIR = Path(__file__).resolve().parent / "figures" / "test_1"
SHOW_PLOT = True

DATA_DIR = (
    Path(__file__).resolve().parent.parent.parent
    / "Data"
    / "Encoder_data"
    / "Test_1"
    / "Processed"
)


def discover_groups(data_dir: Path) -> list[tuple[int, int, int]]:
    """Return (start, end, pwm) for each group of repeated runs at one setpoint."""
    files = sorted(
        data_dir.glob("Test_*.csv"),
        key=lambda path: int(path.stem.split("_")[1]),
    )
    groups = []
    for start in range(0, len(files), TESTS_PER_GROUP):
        end = min(start + TESTS_PER_GROUP, len(files))
        pwm = int(pd.read_csv(files[start])["PWM"].iloc[0])
        groups.append((start, end, pwm))
    return groups


def merge(start: int, end: int) -> pd.DataFrame:
    merged = pd.DataFrame()
    for i in range(start, end):
        df = pd.read_csv(DATA_DIR / f"Test_{i}.csv")
        col = i % TESTS_PER_GROUP
        merged[f"Angles_{col}"] = df["Angles"]
        merged[f"Time_{col}"] = df["Time_s"]
        merged[f"PWM_{col}"] = df["PWM"]
    return merged


def plot_group(ax_row, df: pd.DataFrame, *, show_x: bool, show_y_left: bool) -> None:
    for col in range(TESTS_PER_GROUP):
        ax = ax_row[col]
        time = df[f"Time_{col}"]
        ax.plot(time, df[f"Angles_{col}"], time, df[f"PWM_{col}"])
        ax.grid(True)
        if show_x:
            ax.set_xlabel(TIME_LABEL)
        if show_y_left and col == 0:
            ax.set_ylabel(ANGLE_LABEL)


def plot_page(groups: list[tuple[int, int, int]], page_idx: int) -> plt.Figure:
    datasets = [merge(start, end) for start, end, _pwm in groups]
    n_rows = len(datasets)

    # Landscape A4: wider figure for 5 columns of subplots.
    fig, axs = plt.subplots(
        n_rows,
        TESTS_PER_GROUP,
        squeeze=False,
        figsize=(TEXT_WIDTH_IN * 1.45, row_height(n_rows) * n_rows),
    )

    for row_idx, df in enumerate(datasets):
        plot_group(
            axs[row_idx],
            df,
            show_x=row_idx == n_rows - 1,
            show_y_left=True,
        )

    fig.tight_layout()

    if SAVE_FIGURES:
        save_figure(fig, OUTPUT_DIR / f"test_1_page_{page_idx + 1}")

    return fig


def main() -> None:
    apply_style()

    groups = discover_groups(DATA_DIR)
    if GROUP_INDICES is not None:
        groups = [groups[i] for i in GROUP_INDICES]

    pages = [
        groups[i : i + ROWS_PER_PAGE]
        for i in range(0, len(groups), ROWS_PER_PAGE)
    ]

    for page_idx, page_groups in enumerate(pages):
        plot_page(page_groups, page_idx)

    if SHOW_PLOT:
        plt.show()


if __name__ == "__main__":
    main()

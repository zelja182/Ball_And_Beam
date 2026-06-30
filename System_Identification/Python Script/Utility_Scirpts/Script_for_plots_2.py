from pathlib import Path

import matplotlib.gridspec as gridspec
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
N_COLS = 2
PLOTS_PER_PAGE = 8  # 4 rows × 2 cols — fits one A4 portrait page
DATA_SUBDIR = "Test_30"
FILE_INDICES = None

SAVE_FIGURES = True
OUTPUT_DIR = Path(__file__).resolve().parent / "figures" / "test_2"
SHOW_PLOT = True

DATA_DIR = (
    Path(__file__).resolve().parent.parent.parent
    / "Data"
    / "Encoder_data"
    / "Test_2"
    / DATA_SUBDIR
    / "Processed"
)


def discover_files(data_dir: Path) -> list[Path]:
    return sorted(
        data_dir.glob("Test_*.csv"),
        key=lambda path: int(path.stem.split("_")[1]),
    )


def plot_test(ax, csv_path: Path) -> None:
    df = pd.read_csv(csv_path)
    ax.plot(df["Time_s"], df["Angles"], df["Time_s"], df["PWM"])
    ax.grid(True)


def set_axis_labels(
    ax,
    *,
    show_x: bool,
    show_y: bool,
) -> None:
    if show_x:
        ax.set_xlabel(TIME_LABEL)
    if show_y:
        ax.set_ylabel(ANGLE_LABEL)


def plot_page(files: list[Path], page_idx: int) -> plt.Figure:
    n_files = len(files)
    n_rows = (n_files + N_COLS - 1) // N_COLS
    height = row_height(n_rows)

    fig = plt.figure(figsize=(TEXT_WIDTH_IN, height * n_rows))
    gs = gridspec.GridSpec(n_rows, N_COLS, figure=fig)

    for i, csv_path in enumerate(files):
        if n_files % N_COLS != 0 and i == n_files - 1:
            ax = fig.add_subplot(gs[n_rows - 1, :])
            show_x = True
            show_y = True
        else:
            row, col = divmod(i, N_COLS)
            ax = fig.add_subplot(gs[row, col])
            show_x = row == n_rows - 1
            show_y = col == 0

        plot_test(ax, csv_path)
        set_axis_labels(ax, show_x=show_x, show_y=show_y)

    fig.tight_layout()

    if SAVE_FIGURES:
        save_figure(fig, OUTPUT_DIR / f"{DATA_SUBDIR}_page_{page_idx + 1}")

    return fig


def main() -> None:
    apply_style()

    files = discover_files(DATA_DIR)
    if FILE_INDICES is not None:
        files = [files[i] for i in FILE_INDICES]

    pages = [
        files[i : i + PLOTS_PER_PAGE]
        for i in range(0, len(files), PLOTS_PER_PAGE)
    ]

    for page_idx, page_files in enumerate(pages):
        plot_page(page_files, page_idx)

    if SHOW_PLOT:
        plt.show()


if __name__ == "__main__":
    main()

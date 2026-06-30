"""Matplotlib settings for A4 thesis figures (Word or LaTeX)."""

from pathlib import Path

import matplotlib.pyplot as plt

# Typical printable width inside A4 margins (~16 cm).
TEXT_WIDTH_IN = 6.3
# Usable height on A4 portrait with margins (~24 cm).
MAX_PAGE_HEIGHT_IN = 9.4
SAVE_DPI = 300

ANGLE_LABEL = "Ugao [°]"
TIME_LABEL = "Vreme [s]"


def apply_style() -> None:
    plt.rcParams.update(
        {
            "font.family": "serif",
            "font.size": 9,
            "axes.labelsize": 9,
            "xtick.labelsize": 8,
            "ytick.labelsize": 8,
            "legend.fontsize": 8,
            "lines.linewidth": 1.0,
            "axes.linewidth": 0.6,
            "grid.linewidth": 0.4,
            "grid.alpha": 0.35,
            "savefig.dpi": SAVE_DPI,
            "savefig.pad_inches": 0.03,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        }
    )


def row_height(n_rows: int) -> float:
    return max(1.0, MAX_PAGE_HEIGHT_IN / n_rows)


def save_figure(fig, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(output_path.with_suffix(".png"), dpi=SAVE_DPI, bbox_inches="tight")

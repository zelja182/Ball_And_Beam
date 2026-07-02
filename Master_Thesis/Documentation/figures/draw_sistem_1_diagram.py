"""Redraw Servo closed-loop block diagram (Model 1) for thesis."""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch

OUTPUT_DIR = Path(__file__).resolve().parent
LW = 2.8
FS = 11
BOX_PAD = 0.15


def block(ax, xy, text, width=1.1, height=0.75, fontsize=FS):
    x, y = xy
    patch = FancyBboxPatch(
        (x - width / 2, y - height / 2),
        width,
        height,
        boxstyle="square,pad=0.02",
        linewidth=LW,
        edgecolor="black",
        facecolor="white",
    )
    ax.add_patch(patch)
    ax.text(x, y, text, ha="center", va="center", fontsize=fontsize)
    return patch


def summing(ax, xy, r=0.22):
    x, y = xy
    circle = Circle((x, y), r, fill=False, linewidth=LW, edgecolor="black")
    ax.add_patch(circle)
    return circle


def arrow(ax, start, end):
    ax.annotate(
        "",
        xy=end,
        xytext=start,
        arrowprops=dict(arrowstyle="-|>", lw=LW, color="black", shrinkA=0, shrinkB=0),
    )


def line(ax, start, end):
    ax.plot([start[0], end[0]], [start[1], end[1]], color="black", linewidth=LW, solid_capstyle="round")


def main() -> None:
    fig, ax = plt.subplots(figsize=(11, 3.6))
    ax.set_xlim(-0.2, 13.2)
    ax.set_ylim(0.3, 4.2)
    ax.axis("off")

    y_main = 2.6
    y_fb_inner = 1.15
    y_fb_outer = 0.55

    # Block centers (left to right)
    x_in = 0.9
    x_s1 = 2.2
    x_kp = 3.5
    x_s2 = 4.8
    x_plant = 6.6
    x_int = 8.4
    x_out = 10.2
    x_end = 11.6

    block(ax, (x_in, y_main), r"$X_{\mathrm{ulaz}}(s)$", width=1.35)
    summing(ax, (x_s1, y_main))
    block(ax, (x_kp, y_main), r"$K_p$", width=0.75)
    summing(ax, (x_s2, y_main))
    block(ax, (x_plant, y_main), r"$\dfrac{b_0}{s+a_0}$", width=1.55, height=0.9)
    block(ax, (x_int, y_main), r"$\dfrac{1}{s}$", width=0.75)
    block(ax, (x_out, y_main), r"$\theta_l(s)$", width=1.05)
    block(ax, (x_plant, y_fb_inner), r"$K_d s$", width=0.95, height=0.75, fontsize=10)

    # Forward path
    arrow(ax, (x_in + 0.7, y_main), (x_s1 - 0.22, y_main))
    arrow(ax, (x_s1 + 0.22, y_main), (x_kp - 0.38, y_main))
    arrow(ax, (x_kp + 0.38, y_main), (x_s2 - 0.22, y_main))
    arrow(ax, (x_s2 + 0.22, y_main), (x_plant - 0.78, y_main))
    arrow(ax, (x_plant + 0.78, y_main), (x_int - 0.38, y_main))
    arrow(ax, (x_int + 0.38, y_main), (x_out - 0.53, y_main))
    arrow(ax, (x_out + 0.53, y_main), (x_end, y_main))

    # Inner feedback (derivative): plant output -> Kd*s -> sum2
    tap_x = x_plant + 0.78
    line(ax, (tap_x, y_main), (tap_x, y_fb_inner + 0.38))
    line(ax, (tap_x, y_fb_inner + 0.38), (x_plant + 0.48, y_fb_inner + 0.38))
    line(ax, (x_plant + 0.48, y_fb_inner + 0.38), (x_plant + 0.48, y_fb_inner))
    arrow(ax, (x_plant - 0.48, y_fb_inner), (x_s2, y_fb_inner))
    line(ax, (x_s2, y_fb_inner), (x_s2, y_main - 0.22))

    # Outer feedback: output -> sum1
    line(ax, (x_end, y_main), (x_end, y_fb_outer))
    line(ax, (x_end, y_fb_outer), (x_s1, y_fb_outer))
    line(ax, (x_s1, y_fb_outer), (x_s1, y_main - 0.22))

    # Summing junction signs
    ax.text(x_s1 - 0.38, y_main + 0.12, "+", fontsize=10, ha="center")
    ax.text(x_s1, y_main - 0.42, "−", fontsize=12, ha="center")
    ax.text(x_s2 - 0.38, y_main + 0.12, "+", fontsize=10, ha="center")
    ax.text(x_s2, y_main - 0.42, "−", fontsize=12, ha="center")

    fig.tight_layout(pad=0.2)
    for ext in (".pdf", ".png"):
        fig.savefig(OUTPUT_DIR / f"Sistem_1_model{ext}", dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Saved to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()

"""Drawing helpers for the tutorial's diagrams: labelled boxes, arrows, and shaded panels.

The diagrams in tutorials.py and in the research figure modules use these helpers,
so every diagram draws its boxes and arrows the same way.
"""

from functools import partial

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


def box(ax, x, y, text, color, width=1.65, size=11):
    """A rounded box of height 0.72 with its lower left corner at (x, y), and centred text."""
    ax.add_patch(FancyBboxPatch((x, y), width, .72, boxstyle="round,pad=0.05,rounding_size=0.06",
                               facecolor=color, edgecolor="#64748b", linewidth=1))
    ax.text(x+width/2, y+.36, text, ha="center", va="center", fontsize=size)


def arrow(ax, a, b, color="#475569", **kw):
    """An arrow from point a to point b."""
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="->", mutation_scale=13, color=color, **kw))


def panel(ax, x, y, width, height, label, color, ink):
    """A shaded background panel, with its label to the left of its top edge."""
    ax.add_patch(FancyBboxPatch((x, y), width, height, boxstyle="round,pad=0,rounding_size=0.12",
                               facecolor=color, edgecolor="none", zorder=0))
    ax.text(x-.15, y+height-.25, label, ha="right", va="top", fontsize=11, color=ink)


def bound_helpers(ax):
    """box, arrow, and panel, each bound to one axes."""
    return partial(box, ax), partial(arrow, ax), partial(panel, ax)


def diagram(size, xlim, ylim):
    """A figure of the given size in inches, with one frameless axes, and the helpers bound to it."""
    fig, ax = plt.subplots(figsize=size)
    ax.set(xlim=xlim, ylim=ylim); ax.axis("off")
    return (fig, ax, *bound_helpers(ax))


def finish(fig):
    """Fit the layout and close the figure, so it renders once where it is placed."""
    fig.tight_layout(); plt.close(fig)
    return fig

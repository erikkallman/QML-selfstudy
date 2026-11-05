"""Figures for the Structured generation chapter: the training steps, the isolation graph, and the Lab.

The computation is in research_generation.py. Colours: pink marks the selected
qubit, teal its neighbors and the training steps.
"""

import matplotlib.pyplot as plt
import numpy as np

from figure_style import diagram, finish
import research_generation as gen


def training_picture():
    """The training rule as steps: select the isolating pairs, average one bit, invert, repeat per qubit."""
    # One column, top to bottom: data, one qubit's estimate, repeated per qubit, then generation.
    fig, ax, box, arrow, _ = diagram((4.6, 5.4), (0, 6.6), (1.1, 8.8))
    rows=[(7.85, "Training pairs $(x,y)$\nfrom the target circuit", "#f1f5f9"),
          (6.55, "Select the pairs whose\ninput isolates qubit $j$", "#ccfbf1"),
          (5.25, "Mean $\\bar y_j$ of\nqubit $j$'s output bit", "#ccfbf1"),
          (3.95, "Angle $\\hat\\beta_j=\\frac{1}{2}\\arccos(1-2\\bar y_j)$", "#ccfbf1"),
          (2.45, "Fitted circuit\ngenerates new bitstrings", "#f1f5f9")]
    for i,(y,label,color) in enumerate(rows):
        box(.6, y, label, color, 4.2)
        if i < len(rows)-1: arrow((2.7, y), (2.7, rows[i+1][0]+.72))
    arrow((4.8, 4.31), (4.8, 6.91), connectionstyle="arc,angleA=0,angleB=0,armA=22,armB=22,rad=8")
    ax.text(6.05, 5.61, "Repeat for\neach qubit", ha="center", va="center", fontsize=10, color="#475569")
    ax.text(2.85, 3.56, "all six angles", ha="left", va="center", fontsize=10, color="#475569")
    ax.text(2.7, 1.65, "No loss function and no gradients", ha="center", va="center", fontsize=10, color="#475569")
    return finish(fig)


def graph_picture(wire):
    """The 2-by-3 grid with the selected qubit and its neighbors, and the inputs that isolate it."""
    fig, ax = plt.subplots(figsize=(9, 3.3))
    positions = {j: (j % 3, 1-j//3) for j in gen.WIRES}
    for u, v in gen.EDGES:
        ax.plot([positions[u][0],positions[v][0]], [positions[u][1],positions[v][1]], color="#737373", zorder=0)
    for j, (x, y) in positions.items():
        color = "#be185d" if j == wire else "#0f766e" if j in gen.NEIGHBORS[wire] else "#737373"
        ax.scatter([x], [y], s=650, color=color)
        ax.text(x, y, str(j), ha="center", va="center", color="white", fontsize=14)
        state = (r"$x_j=1:\ |0\rangle$" if j in gen.NEIGHBORS[wire]
                 else r"$x_j=0:\ |+\rangle$" if j == wire else "any input")
        ax.text(x, y-.27, state, ha="center", fontsize=12)
    ax.set(xlim=(-.6,2.6),ylim=(-.6,1.5)); ax.axis("off")
    ax.set_title(rf"Isolate qubit {wire}: its neighbors get input 1 and remain in $|0\rangle$", fontsize=13)
    fig.tight_layout(); plt.close(fig)
    return fig


def distribution_picture(target_p, learned_p, empirical, generated):
    """Left: the probability of each bitstring, target against fitted, with sample frequencies. Right: 32 samples."""
    fig, axes = plt.subplots(1, 2, figsize=(11, 3.5))
    axes[0].plot(target_p, color="#171717", label="Target circuit")
    axes[0].plot(learned_p, label="Fitted circuit")
    axes[0].scatter(np.arange(64), empirical, s=8, alpha=.6, label="New samples")
    axes[0].set(xlabel="Output bitstring (binary order)", ylabel="Probability",
                xticks=[0,16,32,48,63], xticklabels=["000000","010000","100000","110000","111111"])
    axes[0].set_title("Probability of each of the 64 bitstrings", fontsize=12)
    axes[0].tick_params(axis="x", labelsize=8); axes[0].legend(fontsize=9)
    image = axes[1].imshow(generated[:32], cmap="PiYG", vmin=0, vmax=1, aspect="auto", interpolation="nearest")
    fig.colorbar(image, ax=axes[1], ticks=[0,1], label="Output bit")
    axes[1].set(xlabel="Qubit", ylabel="New sample", xticks=range(6))
    axes[1].set_title("32 new bitstrings from the fitted circuit", fontsize=12)
    fig.tight_layout(); plt.close(fig)
    return fig


def angles_picture(target_beta, learned_beta, counts, wire):
    """Left: target and fitted angles. Right: how many training pairs isolate each qubit."""
    fig, axes = plt.subplots(1, 2, figsize=(11, 3))
    axes[0].plot(gen.WIRES, target_beta, "o", color="#171717", label="Target")
    axes[0].plot(gen.WIRES, learned_beta, "x", label="Fitted")
    axes[0].set(xlabel="Qubit", ylabel=r"Angle $\beta_j$ (radians)"); axes[0].legend(fontsize=9)
    axes[1].bar(gen.WIRES, counts, color=["#be185d" if j == wire else "#0f766e" for j in gen.WIRES])
    axes[1].set(xlabel="Qubit", ylabel="Pairs that isolate the qubit")
    fig.tight_layout(); plt.close(fig)
    return fig

"""Supplied code for the two exercises: the circuits, the loss function, and the circuit drawing.

The exercise notebooks import these functions. You can read and change them.
When you save this file, marimo reruns the notebook cells that use a changed function.

The presenter generates this file from tutorials.py, so the code matches the presentation.
"""
from pennylane import numpy as np
import pennylane as qml
import matplotlib.pyplot as plt


def circuit_picture(node, *args, **kwargs):
    fig, axes = qml.draw_mpl(node, level="top", decimals=2, style="black_white", fontsize=14)(*args, **kwargs)
    fig.set_size_inches(10, max(1.6, fig.get_size_inches()[1]))
    for label in axes.texts:
        name, separator, parameters = label.get_text().partition("\n")
        if name in ("RX", "RY", "RZ"):
            label.set_text(f"$R_{name[-1]}$" + separator + parameters)
    tape = qml.workflow.construct_tape(node, level="top")(*args, **kwargs)
    if any(getattr(m.obs, "name", "") == "QuadP" for m in tape.measurements):
        axes.text(.98, 0, r"$X_0$", transform=axes.get_yaxis_transform(), ha="left", va="center", fontsize=14)
        axes.text(.98, 1, r"$P_1$", transform=axes.get_yaxis_transform(), ha="left", va="center", fontsize=14)
    plt.close(fig)
    return fig


def trainable_block(theta):
    qml.RZ(theta[0], wires=0)
    qml.RY(theta[1], wires=0)
    qml.RZ(theta[2], wires=0)


@qml.qnode(
    qml.device("default.qubit", wires=1),
    interface="autograd", diff_method="backprop",
)
def training_model(x, weights):
    qml.RX(x, wires=0)
    qml.RZ(weights[0], wires=0)
    qml.RY(weights[1], wires=0)
    return qml.expval(qml.Z(0))


def regression_loss(weights, xs, targets):
    return np.mean((training_model(xs, weights) - targets) ** 2)

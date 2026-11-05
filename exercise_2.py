# /// script
# requires-python = ">=3.12,<3.13"
# dependencies = ["marimo==0.25.2", "pennylane==0.45.1", "matplotlib>=3.9,<4", "numpy>=2,<3"]
#
# [tool.marimo.runtime]
# auto_reload = "autorun"
# ///


import marimo


__generated_with = "0.25.2"


app = marimo.App(width='full', app_title='Training exercise', css_file='workshop.css')


@app.cell(hide_code=True)
def task_instructions(mo):
    mo.md(r"""
    # Exercise 2: freeze and restore learning

    ## Your task (six minutes)

    The notebook already contains the data, the circuit, the loss function, the starting weights, and the plots.
    You change one assignment: the weight update in `fit_regression`.
    That function is in the code cell directly below these instructions.
    Freezing the weights means keeping them at their starting values during training.

    1. Click the Run button at the bottom right. The check cell, below the code cell, shows the training loss before the first update and after 100 updates.
    2. Predict the loss curve if the weights never change.
    3. Replace the marked three-line assignment `weights = optimizer.step(...)` with `weights = weights`.
    4. Click Run again. If the edit is right, the check cell reports that the weights keep their starting values and that the loss stays constant.
    5. Open "Restore the optimizer assignment" in the check cell. Copy those three lines back in place of `weights = weights`, and click Run. The loss falls again.

    Change nothing else in the function. The check cell always uses the learning rate $\eta=0.2$ and 100 updates.
    After the check, try other settings with the sliders and the checkbox next to the plots further down.

    ## Algorithm guide

    ```text
    # Already in the notebook: data, circuit, loss function, starting weights.
    set the weights to their starting values
    record the loss
    repeat for the requested number of updates:
        if updates are enabled:
            compute new weights from the gradient of the loss
            # YOUR EDIT: keep the current weights instead
        record the loss with the current weights
    compare the last loss with the first loss
    restore the gradient update      # then check that the loss falls again
    ```

    ## Edit this function
    """)
    return


@app.cell
def edit_training(np, qml, regression_loss):
    def fit_regression(rate=0.2, steps=100, enabled=True):
        xs = np.linspace(-np.pi, np.pi, 21, requires_grad=False)
        targets = 0.7 * np.cos(xs) + 0.2 * np.sin(xs)
        weights = np.array([0.3, 0.7], requires_grad=True)
        optimizer = qml.GradientDescentOptimizer(stepsize=rate)
        history = [float(regression_loss(weights, xs, targets))]
        for _ in range(steps):
            if enabled:
                # YOUR EDIT: replace this whole three-line assignment with:
                # weights = weights
                # Keep the history.append line below. It records the loss with frozen weights.
                weights = optimizer.step(
                    lambda w: regression_loss(w, xs, targets), weights
                )
            history.append(float(regression_loss(weights, xs, targets)))
        return xs, targets, weights, np.array(history, requires_grad=False)
    return (fit_regression,)


@app.cell(hide_code=True)
def check_training(fit_regression, mo, onp):
    _, _, check_weights, check_history = fit_regression(rate=0.2, steps=100, enabled=True)
    if onp.allclose(check_history, check_history[0]) and onp.allclose(check_weights, [0.3, 0.7]):
        check_status = "The weights keep their starting values, so the loss stays constant. Now restore the optimizer assignment, so that the circuit learns again."
    elif check_history[-1] < 1e-8:
        check_status = "The loss falls below $10^{-8}$, so the circuit learns. Predict the loss with frozen weights, then edit the marked assignment."
    else:
        check_status = "The loss neither stays constant nor falls below $10^{-8}$. Check the edited assignment, and undo any other change in the function."
    mo.vstack([
        mo.md(f"## Check\n\nTraining loss: `{check_history[0]:.6f}` before the first update, `{check_history[-1]:.6g}` after 100 updates.\n\n{check_status}"),
        mo.accordion({"Restore the optimizer assignment": mo.md("```python\nweights = optimizer.step(\n    lambda w: regression_loss(w, xs, targets), weights\n)\n```")}),
    ])
    return check_history, check_status, check_weights


@app.cell(hide_code=True)
def show_experiment(exercise_two_page):
    exercise_two_page
    return


@app.cell(hide_code=True)
def imports():
    import marimo as mo
    import numpy as onp
    from pennylane import numpy as np
    import pennylane as qml
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.size': 12, 'mathtext.fontset': 'cm', 'axes.spines.top': False, 'axes.spines.right': False, 'figure.facecolor': 'white', 'axes.prop_cycle': plt.cycler(color=['#0f766e', '#be185d', '#b45309'])})
    from exercise_circuits import circuit_picture, regression_loss, training_model
    from exercise_layout import input_output, source_of
    return (circuit_picture, input_output, mo, np, onp, plt, qml, regression_loss, source_of, training_model)


@app.cell(hide_code=True)
def exercise_controls(mo, onp):
    rate = mo.ui.slider(0, 0.6, step=0.02, value=0.2, label='Learning rate $\\eta$', show_value=True, full_width=True)
    updates = mo.ui.slider(0, 150, step=10, value=100, label='Updates', show_value=True, full_width=True)
    update_enabled = mo.ui.checkbox(value=True, label='Parameter updates')
    return (rate, update_enabled, updates)


@app.cell(hide_code=True)
def exercise_two(circuit_picture, fit_regression, input_output, mo, onp, plt, rate, training_model, update_enabled, updates):
    _xs, _targets, _weights, _history = fit_regression(rate.value, updates.value, update_enabled.value)
    _fig, _axes = plt.subplots(1, 2, figsize=(11, 3.3))
    _axes[0].plot(_xs, _targets, 'o', label='Target')
    _axes[0].plot(_xs, training_model(_xs, _weights), label='Model')
    _axes[0].set(xlabel='$x$', ylabel='Prediction', ylim=(-1, 1))
    _axes[0].legend()
    _axes[1].semilogy(onp.maximum(_history, 1e-14))
    _axes[1].set(xlabel='Updates', ylabel='Mean squared error')
    _fig.tight_layout()
    plt.close(_fig)
    _lab = mo.vstack([mo.md('## Training lab'), input_output([rate, updates, update_enabled], mo.vstack([circuit_picture(training_model, onp.pi / 3, _weights), _fig, mo.md(f'Training MSE: {_history[0]:.5f} to {_history[-1]:.3g}')]))])
    exercise_two_page = _lab
    return (exercise_two_page,)


@app.cell(hide_code=True)
def supplied_reference(mo, source_of, training_model, regression_loss):
    mo.accordion({'Code of the circuit and the loss function': mo.md('```python\n' + source_of(training_model, regression_loss) + '\n```')})
    return


if __name__ == "__main__":
    app.run()

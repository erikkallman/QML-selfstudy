# /// script
# requires-python = ">=3.12,<3.13"
# dependencies = ["marimo==0.25.2", "pennylane==0.45.1", "matplotlib>=3.9,<4", "numpy>=2,<3"]
#
# [tool.marimo.runtime]
# auto_reload = "autorun"
# ///


import marimo


__generated_with = "0.25.2"


app = marimo.App(width='full', app_title='Circuit exercise', css_file='workshop.css')


@app.cell(hide_code=True)
def task_instructions(mo):
    mo.md(r"""
    # Exercise 1: change the input rotation

    ## Your task (six minutes)

    The notebook already contains the circuit, the measurement, and the plots.
    You change one gate: the input rotation in `encoding_circuit`.
    That function is in the code cell directly below these instructions.
    The *$Z$ output* is the mean value of a $Z$ measurement on the qubit.

    1. Click the Run button at the bottom right. The check cell, below the code cell, shows the $Z$ output.
    2. Predict how the $Z$ output changes if the input rotation is $R_Y$ instead of $R_X$.
    3. In the marked line, replace `qml.RX` with `qml.RY`. Keep `x` and `wires=0` as they are.
    4. Click Run again. Read the new value in the check cell, then look at the circuit drawing and the curve below it.
    5. Explain why the $Z$ output changed. Hint: $R_X$ and $R_Y$ rotate the qubit about different axes.
    6. Change `qml.RY` back to `qml.RX`, and click Run again.

    The check cell always uses the same settings: input $x=\pi/3$, angles $\theta=(\pi/2,\pi/3,\pi/4)$, and the $Z$ measurement.
    With $R_X$, it shows $-0.5$.
    After the check, try other values with the sliders below it.

    ## Algorithm guide

    ```text
    # Already in the notebook: preparation, fixed gates, measurement, plots.
    prepare the qubit in the state |0>
    apply the input rotation RX(x)    # YOUR EDIT: change RX to RY below
    apply the fixed gates RZ, RY, RZ with the angles theta
    measure the mean Z value
    compare it with the value before your edit
    change RY back to RX
    ```

    ## Edit this function
    """)
    return


@app.cell
def edit_encoding(qml):
    def encoding_circuit(x):
        # YOUR EDIT: replace RX with RY. Keep x and wires=0 as they are.
        # Run this cell, read the check below, then change RY back to RX.
        qml.RX(x, wires=0)
    return (encoding_circuit,)


@app.cell(hide_code=True)
def check_encoding(mo, onp, quantum_model):
    _angles = [onp.pi / 2, onp.pi / 3, onp.pi / 4]
    fixed_output = float(quantum_model(onp.pi / 3, _angles, "Z"))
    if onp.isclose(fixed_output, -0.5):
        check_status = "This is the value with $R_X$. Predict the value with $R_Y$, then edit the marked line."
    elif onp.isclose(fixed_output, 0.25):
        check_status = "This is the value with $R_Y$. Explain why it differs from $-0.5$, then change `qml.RY` back to `qml.RX`."
    else:
        check_status = "This value matches neither $R_X$ ($-0.5$) nor $R_Y$ ($0.25$). Check the edited line: the gate name, the argument `x`, and `wires=0`."
    mo.md(f"## Check\n\n$Z$ output at the check settings: `{fixed_output:.6f}`.\n\n{check_status}")
    return check_status, fixed_output


@app.cell(hide_code=True)
def show_experiment(exercise_one_page):
    exercise_one_page
    return


@app.cell(hide_code=True)
def imports():
    import marimo as mo
    import numpy as onp
    import pennylane as qml
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.size': 12, 'mathtext.fontset': 'cm', 'axes.spines.top': False, 'axes.spines.right': False, 'figure.facecolor': 'white', 'axes.prop_cycle': plt.cycler(color=['#0f766e', '#be185d', '#b45309'])})
    from exercise_circuits import circuit_picture, trainable_block
    from exercise_layout import input_output, source_of
    return (circuit_picture, input_output, mo, onp, plt, qml, source_of, trainable_block)


@app.cell(hide_code=True)
def circuit_functions(encoding_circuit, qml, trainable_block):

    @qml.qnode(qml.device('default.qubit', wires=1))
    def quantum_model(x, theta, readout='Z'):
        encoding_circuit(x)
        trainable_block(theta)
        return qml.expval(qml.Z(0) if readout == 'Z' else qml.X(0))
    return (quantum_model,)


@app.cell(hide_code=True)
def exercise_controls(mo, onp):
    input_angle = mo.ui.slider(-float(onp.pi), float(onp.pi), step=0.01, value=float(onp.pi / 3), label='Input $x$', full_width=True)
    theta_one = mo.ui.slider(-float(onp.pi), float(onp.pi), step=0.05, value=float(onp.pi / 2), label='$\\theta_1$', full_width=True)
    theta_two = mo.ui.slider(-float(onp.pi), float(onp.pi), step=0.05, value=float(onp.pi / 3), label='$\\theta_2$', full_width=True)
    theta_three = mo.ui.slider(-float(onp.pi), float(onp.pi), step=0.05, value=float(onp.pi / 4), label='$\\theta_3$', full_width=True)
    readout = mo.ui.dropdown(['Z', 'X'], value='Z', label='Readout', full_width=True)
    return (input_angle, readout, theta_one, theta_three, theta_two)


@app.cell(hide_code=True)
def exercise_one(circuit_picture, input_angle, input_output, mo, onp, plt, quantum_model, readout, theta_one, theta_three, theta_two):
    _theta = onp.array([theta_one.value, theta_two.value, theta_three.value])
    _xs = onp.linspace(-onp.pi, onp.pi, 121)
    _value = float(quantum_model(input_angle.value, _theta, readout.value))
    _fig, _ax = plt.subplots(figsize=(10, 3.2))
    _ax.plot(_xs, quantum_model(_xs, _theta, readout.value))
    _ax.scatter([input_angle.value], [_value], color='#be185d', s=60)
    _ax.set(xlabel='$x$', ylabel=f'$\\langle {readout.value}\\rangle$', ylim=(-1.1, 1.1))
    plt.close(_fig)
    _lab = mo.vstack([mo.md('## Circuit lab'), input_output([input_angle, theta_one, theta_two, theta_three, readout], mo.vstack([circuit_picture(quantum_model, input_angle.value, _theta, readout.value), _fig, mo.md(f'$f_\\theta(x)={_value:.6f}$')]))])
    exercise_one_page = _lab
    return (exercise_one_page,)


@app.cell(hide_code=True)
def supplied_reference(mo, source_of, trainable_block, quantum_model):
    mo.accordion({'Code of the fixed gates and the measurement': mo.md('```python\n' + source_of(trainable_block, quantum_model) + '\n```')})
    return


if __name__ == "__main__":
    app.run()

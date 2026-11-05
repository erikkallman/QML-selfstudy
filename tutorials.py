# /// script
# requires-python = ">=3.12,<3.13"
# dependencies = ["marimo==0.25.2", "pennylane==0.45.1", "matplotlib>=3.9,<4", "numpy>=2,<3"]
# ///

import marimo

__generated_with = "0.25.2"
app = marimo.App(
    width="full",
    app_title="Quantum Machine Learning Dojo",
    css_file="workshop.css",
)


@app.cell
def imports():
    import inspect
    import textwrap
    import marimo as mo
    import numpy as onp
    from pennylane import numpy as np
    import pennylane as qml
    import matplotlib.pyplot as plt
    import figure_style
    import research_generation as gen
    import research_generation_figures as gen_fig
    import research_memory as mem
    import research_memory_figures as mem_fig
    import participant_package
    plt.rcParams.update({"font.size": 12, "mathtext.fontset": "cm", "axes.spines.top": False,
                         "axes.spines.right": False, "figure.facecolor": "white",
                         "axes.prop_cycle": plt.cycler(color=["#0f766e", "#be185d", "#b45309"])})
    return (
        figure_style,
        gen,
        gen_fig,
        inspect,
        mem,
        mem_fig,
        mo,
        np,
        onp,
        participant_package,
        plt,
        qml,
        textwrap,
    )


@app.cell
def layouts(inspect, mo, textwrap):
    def source_of(*functions):
        return "\n\n".join(textwrap.dedent(inspect.getsource(getattr(f, "func", f))).strip() for f in functions)

    def step(title, explanation, code):
        prose = mo.md(f"### {title}\n\n" + textwrap.dedent(explanation).strip())
        listing = mo.md("```python\n" + code + "\n```")
        return mo.Html(f'<section class="tutorial-step"><div class="tutorial-explanation">{prose.text}</div>'
                       f'<div class="tutorial-code">{listing.text}</div></section>')

    def input_output(controls, output):
        inputs = mo.vstack(controls, align="stretch", gap=1.5)
        return mo.Html(f'<div class="experiment-layout"><div class="experiment-inputs" role="group" aria-label="Inputs">{inputs}</div>'
                       f'<div class="experiment-output" role="group" aria-label="Output">{mo.as_html(output)}</div></div>')

    def tutor(question, answer):
        prompt = mo.md(question).text
        response = mo.md(answer).text
        return mo.Html(
            f'<details class="audience-question"><summary>{prompt}</summary>'
            f'<div class="audience-answer">{response}</div></details>'
        )

    def lesson_notes(text):
        return mo.Html(f'<div class="chapter-notes">{mo.md(text).text}</div>')

    return input_output, lesson_notes, source_of, step, tutor


@app.cell
def figure_layouts(lesson_notes, mo):
    def notes_beside(text, *figures):
        # Use .text: formatting an Html object directly folds newlines and breaks code blocks.
        pictures = "".join(mo.as_html(figure).text for figure in figures)
        return mo.Html(f'<section class="notes-figure">{lesson_notes(text).text}'
                       f'<div class="notes-figure-picture">{pictures}</div></section>')

    def caption(text):
        return mo.Html(f'<div class="figure-caption">{mo.md(text).text}</div>')

    return caption, notes_beside


@app.cell
def chapter_text(mo, step, tutor):
    chapters = mo.notebook_dir() / "chapters"

    def prose(name):
        """The text of one chapter file, such as "memory/01-where.md"."""
        return (chapters / name).read_text(encoding="utf-8")

    def prose_step(name, code):
        """A step from a chapter file whose first line is the step's "### " heading."""
        title, _, text = prose(name).partition("\n")
        return step(title.removeprefix("### "), text, code)

    def question(name):
        """A question from a chapter file: the question, a blank line, then the answer."""
        prompt, _, answer = prose(name).partition("\n\n")
        return tutor(prompt, answer.strip())

    return prose, prose_step, question


@app.cell
def circuit_drawing(plt, qml):
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

    return (circuit_picture,)


@app.cell
def diagrams(figure_style, plt):
    def flow_picture(kind="training"):
        fig, ax = plt.subplots(figsize=(12, 3.8))
        ax.set(xlim=(0, 12), ylim=(0, 4)); ax.axis("off")
        box, arrow, panel = figure_style.bound_helpers(ax)
        if kind == "models":
            fig.set_size_inches(12, 5.8)
            ax.set_ylim(0, 5.6)
            paths = [
                (4.4, "1. Variational predictor: fit circuit angles", ["Input $x$", "Circuit $U_\\theta$", "Mean readout", "Prediction $f_\\theta(x)$"]),
                (2.6, "2. Kernel method: fit a classical predictor from similarities", ["Inputs $x,x'$", "Overlap circuit", "Similarity $k(x,x')$", "Classical predictor"]),
                (.8, "3. Generative model: fit a distribution, then draw samples", ["Condition $x$", "Circuit $U_\\beta$", "Measure bits", "New sample $y$"]),
            ]
            for y, heading, labels in paths:
                ax.text(.2, y+.95, heading, fontsize=12, color="#0f766e")
                for i, label in enumerate(labels):
                    box(.2+3*i, y, label, "#ccfbf1" if i == 1 else "#f1f5f9", 2.3)
                    if i < 3:
                        arrow((2.5+3*i,y+.36),(3.2+3*i,y+.36))
        elif kind == "training":
            # One column, top to bottom: data, quantum circuit, classical loss and update.
            fig.set_size_inches(4.5, 6.6)
            ax.set(xlim=(0, 6.4), ylim=(1.1, 10.4))
            panel(2.05, 5.3, 3.3, 3.55, "Quantum\ncircuit", "#f0fdfa", "#0f766e")
            panel(2.05, 1.4, 3.3, 3.55, "Classical\ncomputer", "#f5f5f5", "#475569")
            rows=[(9.45, "Input $x$", "#f1f5f9"), (7.75, "Encode\n$R_X(x)$", "#ccfbf1"),
                  (6.65, "Trainable\n$U(\\theta)$", "#ccfbf1"), (5.55, "Measure\n$\\langle Z\\rangle$", "#ccfbf1"),
                  (3.85, "Prediction\n$f_\\theta(x)$", "#f1f5f9"), (2.75, "Loss\n$(f-y)^2$", "#fce7f3"),
                  (1.65, "Optimizer\n$\\theta-\\eta\\nabla L$", "#fef3c7")]
            for i,(y,label,color) in enumerate(rows):
                box(2.4, y, label, color, 2.6)
                if i < len(rows)-1: arrow((3.7, y), (3.7, rows[i+1][0]+.72))
            box(.1, 2.75, "Target $y$", "#f1f5f9")
            arrow((1.75, 3.11), (2.4, 3.11))
            arrow((5.0, 2.01), (5.0, 7.01), connectionstyle="arc,angleA=0,angleB=0,armA=28,armB=28,rad=8")
            ax.text(6.05, 4.51, "Classical feedback changes the parameters", rotation=90,
                    ha="center", va="center", fontsize=10, color="#475569")
        else:
            raise ValueError(f"Unknown diagram {kind!r}. The research diagrams are in "
                             "research_memory_figures.py and research_generation_figures.py.")
        fig.tight_layout(); plt.close(fig)
        return fig

    return (flow_picture,)


@app.cell
def circuit_functions(qml):
    def encoding_circuit(x):
        qml.RX(x, wires=0)

    def trainable_block(theta):
        qml.RZ(theta[0], wires=0)
        qml.RY(theta[1], wires=0)
        qml.RZ(theta[2], wires=0)

    @qml.qnode(qml.device("default.qubit", wires=1))
    def encoded_only(x):
        encoding_circuit(x)
        return qml.expval(qml.Z(0))

    @qml.qnode(qml.device("default.qubit", wires=1))
    def quantum_model(x, theta, readout="Z"):
        encoding_circuit(x)
        trainable_block(theta)
        return qml.expval(qml.Z(0) if readout == "Z" else qml.X(0))

    return encoded_only, encoding_circuit, quantum_model, trainable_block


@app.cell
def tab_states(mo):
    circuit_view, set_circuit_view = mo.state("Tutorial")
    training_view, set_training_view = mo.state("Tutorial")
    memory_view, set_memory_view = mo.state("Tutorial")
    generation_view, set_generation_view = mo.state("Tutorial")
    models_view, set_models_view = mo.state("Tutorial")
    chapter_view, set_chapter_view = mo.state("Start")
    return (chapter_view, circuit_view, generation_view, memory_view, set_chapter_view,
            set_circuit_view, set_generation_view, set_memory_view, set_training_view, training_view,
            models_view, set_models_view)


@app.cell
def exercise_controls(mo, onp):
    input_angle=mo.ui.slider(-float(onp.pi), float(onp.pi), step=.01, value=float(onp.pi/3), label=r"Input $x$",full_width=True)
    theta_one=mo.ui.slider(-float(onp.pi),float(onp.pi),step=.05,value=float(onp.pi/2),label=r"$\theta_1$",full_width=True)
    theta_two=mo.ui.slider(-float(onp.pi),float(onp.pi),step=.05,value=float(onp.pi/3),label=r"$\theta_2$",full_width=True)
    theta_three=mo.ui.slider(-float(onp.pi),float(onp.pi),step=.05,value=float(onp.pi/4),label=r"$\theta_3$",full_width=True)
    readout=mo.ui.dropdown(["Z","X"],value="Z",label="Readout",full_width=True)
    rate=mo.ui.slider(0,.6,step=.02,value=.2,label=r"Learning rate $\eta$",show_value=True,full_width=True)
    updates=mo.ui.slider(0,150,step=10,value=100,label="Updates",show_value=True,full_width=True)
    update_enabled=mo.ui.checkbox(value=True,label="Parameter updates")
    return (
        input_angle,
        rate,
        readout,
        theta_one,
        theta_three,
        theta_two,
        update_enabled,
        updates,
    )


@app.cell
def training_functions(np, qml):
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

    def fit_regression(rate=0.2, steps=100, enabled=True):
        xs = np.linspace(-np.pi, np.pi, 21, requires_grad=False)
        targets = 0.7 * np.cos(xs) + 0.2 * np.sin(xs)
        weights = np.array([0.3, 0.7], requires_grad=True)
        optimizer = qml.GradientDescentOptimizer(stepsize=rate)
        history = [float(regression_loss(weights, xs, targets))]
        for _ in range(steps):
            if enabled:
                weights = optimizer.step(
                    lambda w: regression_loss(w, xs, targets), weights
                )
            history.append(float(regression_loss(weights, xs, targets)))
        return xs, targets, weights, np.array(history, requires_grad=False)

    def shifted_derivative(x, weights, index):
        shift = np.eye(len(weights), requires_grad=False)[index] * np.pi / 2
        return (training_model(x, weights + shift) - training_model(x, weights - shift)) / 2

    return fit_regression, regression_loss, shifted_derivative, training_model


@app.cell
def exercise_one(
    circuit_view,
    circuit_picture,
    encoded_only,
    encoding_circuit,
    input_angle,
    input_output,
    lesson_notes,
    mo,
    onp,
    plt,
    quantum_model,
    readout,
    set_circuit_view,
    source_of,
    step,
    theta_one,
    theta_three,
    theta_two,
    trainable_block,
    tutor,
):
    _theta=onp.array([theta_one.value,theta_two.value,theta_three.value])
    _xs=onp.linspace(-onp.pi,onp.pi,121)
    _value=float(quantum_model(input_angle.value,_theta,readout.value))
    _fig,_ax=plt.subplots(figsize=(10,3.2))
    _ax.plot(_xs,quantum_model(_xs,_theta,readout.value))
    _ax.scatter([input_angle.value],[_value],color="#be185d",s=60)
    _ax.set(xlabel=r"$x$",ylabel=rf"$\langle {readout.value}\rangle$",ylim=(-1.1,1.1));plt.close(_fig)
    _story=mo.vstack([
        mo.md("## Exercise 1: build a circuit that predicts"),
        lesson_notes(r"""
        ### The code task

        Open your copy of `exercise_1.py`. The notebook supplies a working circuit and its plots.
        You change one gate in `encoding_circuit`, inside the marked `edit_encoding` cell.

        1. Read the task and run the starting code. Record the fixed-settings $Z$ output.
        2. Predict the effect of changing the input rotation from $R_X$ to $R_Y$.
        3. Make that one-line edit, run the cell, and compare the check and circuit drawing.
        4. Explain the change, then restore $R_X$.

        ```text
        # Supplied: initial state, later gates, readout, and plots.
        encode the input with RX(x)  # YOUR EDIT: use RY(x), then restore RX(x)
        apply the supplied later gates
        measure the mean Z output
        compare both encodings at the same fixed settings
        ```

        The task instructions come first in the exercise notebook. The sections below explain the supplied circuit.
        """),
        step("1. Encoding - turn one number into a state",r"""
        We start with one qubit in $\lvert0\rangle$. Our input is a real number $x$.
        The gate $R_X(x)$ rotates it by $x$ radians around the Bloch sphere's $X$ axis.
        This makes the state, and therefore its measurement probabilities, depend on the input.

        A $Z$ measurement returns $+1$ for $\lvert0\rangle$ and $-1$ for $\lvert1\rangle$.
        Averaging repeated runs gives $\langle Z\rangle=P(0)-P(1)$.
        The circuit below computes that average after encoding the input.
        """,source_of(encoding_circuit,encoded_only)),
        circuit_picture(encoded_only,onp.pi/3),
        tutor(r"What is $\langle Z\rangle$ at $x=0$, $\pi/2$, and $\pi$?",r"The rotation gives $\langle Z\rangle=\cos x$. The three values are $1$, $0$, and $-1$. Each is a mean over repeated measurements."),
        step("2. Give the model adjustable angles",r"""
        The next block has three parameters. Input $x$ describes the example.
        $\theta$ describes the model.
        For a fixed $\theta$, sweeping $x$ traces one prediction curve.
        Changing $\theta$ selects another curve from the functions this circuit can represent.
        Exercise 2 chooses these angles using data.

        Read the circuit from left to right. Changing gate order changes the function.
        """,source_of(trainable_block,quantum_model)),
        circuit_picture(quantum_model,onp.pi/3,[onp.pi/2,onp.pi/3,onp.pi/4],"Z"),
        step("3. Choose what the output means",r"""
        The readout returns the expectation of an observable.
        Here an observable is the measurement we choose to turn the state into a number.
        $Z$ reads the difference between zero and one probabilities.
        $X$ instead reads the difference between $\lvert+\rangle$ and $\lvert-\rangle$ probabilities.
        Both expectations lie between $-1$ and $+1$.
        Compare them for the same prepared state and gate sequence.
        """,'theta = [np.pi / 2, np.pi / 3, np.pi / 4]\nquantum_model(np.pi / 3, theta, "Z")\nquantum_model(np.pi / 3, theta, "X")'),
        tutor(r"Which angle leaves the $Z$ readout unchanged?", r"The final angle $\theta_3$. The gate $R_Z(\theta_3)$ commutes with $Z$, so changing it leaves $\langle Z\rangle$ unchanged. It can change $\langle X\rangle$. Switch to $X$ readout and vary $\theta_3$ again."),
        step("4. Make the six-minute edit",r"""
        Replace `qml.RX` with `qml.RY` in `encoding_circuit`. Keep the angles and $Z$ readout fixed.
        Run the edited cell and compare its output with the original.
        Restore `qml.RX` before moving on.
        """,source_of(encoding_circuit)),
        tutor(r"How does replacing $R_X$ with $R_Y$ change the output at the starting angles?", r"At $x=\pi/3$ and $\theta=(\pi/2,\pi/3,\pi/4)$, the $Z$ output changes from $-0.5$ to $+0.25$. The gates after the encoding distinguish the two rotations."),
        tutor(r"Why do bare $R_X$ and $R_Y$ rotations give the same $Z$ readout?",r"Both give $\langle Z\rangle=\cos x$ when applied to $\lvert0\rangle$. The later gates distinguish their states. Inspect the gate sequence as well as the output."),
    ])
    _lab=mo.vstack([mo.md("## Circuit lab"),input_output(
        [input_angle,theta_one,theta_two,theta_three,readout],mo.vstack([
            circuit_picture(quantum_model,input_angle.value,_theta,readout.value),_fig,
            mo.md(rf"$f_\theta(x)={_value:.6f}$"),
        ]))])
    exercise_one_page=mo.ui.tabs({"Tutorial":_story,"Lab":_lab},value=circuit_view(),on_change=set_circuit_view)
    return (exercise_one_page,)


@app.cell
def exercise_two(
    circuit_picture,
    fit_regression,
    flow_picture,
    input_output,
    lesson_notes,
    mo,
    notes_beside,
    onp,
    plt,
    rate,
    regression_loss,
    set_training_view,
    shifted_derivative,
    source_of,
    step,
    training_model,
    training_view,
    tutor,
    update_enabled,
    updates,
):
    _xs,_targets,_weights,_history=fit_regression(rate.value,updates.value,update_enabled.value)
    _fig,_axes=plt.subplots(1,2,figsize=(11,3.3))
    _axes[0].plot(_xs,_targets,"o",label="Target");_axes[0].plot(_xs,training_model(_xs,_weights),label="Model")
    _axes[0].set(xlabel=r"$x$",ylabel="Prediction",ylim=(-1,1));_axes[0].legend()
    _axes[1].semilogy(onp.maximum(_history,1e-14));_axes[1].set(xlabel="Updates",ylabel="Mean squared error")
    _fig.tight_layout();plt.close(_fig)
    _story=mo.vstack([
        mo.md("## Exercise 2: close the training loop"),
        notes_beside(r"""
        ### The code task

        Open your copy of `exercise_2.py`. The dataset, model, and loss function are supplied.
        You change the marked weight assignment in `fit_regression`, inside the `edit_training` cell.

        1. Run the starting code and inspect the fixed-settings loss check.
        2. Predict the loss curve when the weights stay fixed.
        3. Replace the marked three-line optimizer assignment with `weights = weights`, then run the cell.
        4. Check the flat loss, restore the optimizer assignment, and confirm that learning resumes.

        ```text
        # Supplied: data, circuit, loss, and starting weights.
        record the initial loss
        repeat the training loop:
            compute new weights     # YOUR EDIT: temporarily keep the old weights
            record the current loss # Keep this line so the flat loss is visible
        compare the initial and final loss
        restore the update and check that loss falls again
        ```

        The notebook includes the original optimizer assignment in a reset block.
        The sections below explain why that assignment makes learning possible.
        """, flow_picture("training")),
        step("1. Make an error signal",r"""
        Training changes the circuit's parameters according to a learning rule.
        We supply 21 input values and targets $y=0.7\cos x+0.2\sin x$.
        The training circuit has two adjustable angles.
        For each input, subtract its target from the prediction, square the difference, then average over the dataset.
        This mean squared error is the loss. Lower loss means closer predictions on these training points.

        Follow the arrows: the quantum circuit produces a prediction; the classical computer computes the loss.
        """,source_of(training_model,regression_loss)),
        step("2. Compute a gradient from circuit evaluations",r"""
        Each weight in this circuit appears once in a Pauli rotation.
        A gradient tells us how sensitive the loss is to a small change in each weight.
        Hold the input and other weight fixed. Two shifted evaluations give the derivative:

        $$\partial_{\theta_j}f=\frac{f(\theta_j+\pi/2)-f(\theta_j-\pi/2)}{2}.$$

        Apply the chain rule to the squared-error loss:
        $\partial_{\theta_j}L=\frac{2}{N}\sum_i(f_\theta(x_i)-y_i)\partial_{\theta_j}f_\theta(x_i)$.
        Here $N=21$ is the number of training pairs.
        Each prediction error weights the circuit's sensitivity at that input; their average gives the loss gradient.
        The simulator uses backpropagation for speed. Hardware estimates shifted expectations from repeated measurements.
        Other generators and reused parameters require their own derivative rules.
        [Gradient rule](https://arxiv.org/abs/1811.11184).
        """, source_of(shifted_derivative)),
        tutor("What stays fixed when estimating one weight's derivative?", r"Keep the input and every other weight fixed. Shift only the selected weight by $+\pi/2$ and $-\pi/2$. Apply the loss's chain rule after computing the prediction derivative."),
        step("3. Use the loss to change the angles",r"""
        Start from the same two angles on each run. The optimizer computes a gradient and updates them.
        It moves opposite the gradient to reduce the loss, using $\eta$ to set the step size.
        A small step can make slow progress. An overly large step can overshoot a low-loss region.
        The dataset stays fixed. Each loss value in the history belongs to a new parameter vector.

        The simulator uses backpropagation. On hardware, a suitable shift rule estimates derivatives from repeated circuit executions.
        """,source_of(fit_regression)),
        circuit_picture(training_model,onp.pi/3,[.3,.7]),
        step("4. Break the feedback, then restore it",r"""
        Replace the optimizer assignment with `weights = weights` and run the cell.

        Restore the update. Compare this with setting $\eta=0$ or disabling parameter updates in the Lab.
        These are three ways to isolate the same part of the loop.
        """,'# Inside the loop, replace the optimizer assignment with:\nweights = weights'),
        tutor("What happens to the loss when the weights stay fixed?", r"The loss stays at its initial value. The circuit makes the same predictions on the fixed dataset. Setting $\eta=0$ or disabling parameter updates also keeps the weights fixed."),
        tutor("Does a lower training loss show a quantum advantage?",r"The loss measures fit to the training inputs. Classical least squares with $\cos x$ and $\sin x$ fits this target too. Assessing an advantage requires a useful task and a comparison of total resource costs."),
        step("5. Read the two plots together",r"""
        First compare the prediction curve with the target points. Then inspect the loss history.
        A flat loss with fixed parameters is different from a loss that falls but stops above zero.

        At the default settings, the training MSE falls from about 0.07477 to $3.82\times10^{-9}$.
        This circuit is independent of the encoding edit in Exercise 1.
        """,'xs, targets, weights, history = fit_regression(rate=0.2, steps=100)\nprint(history[0], history[-1])'),
        mo.accordion({"Classical baseline for this training task": lesson_notes(r"""
        The target is $0.7\cos x+0.2\sin x$.
        A classical linear model with features $\cos x$ and $\sin x$ fits it by least squares.
        Its two fitted coefficients are $0.7$ and $0.2$, giving a fit to numerical precision on these training points.

        This target lets us check the circuit's training loop against a known solution.
        A practical comparison also tests new data and counts data preparation, fitting, circuit executions, and readout costs.
        """)}),
    ])
    _lab=mo.vstack([mo.md("## Training lab"),input_output([rate,updates,update_enabled],mo.vstack([
        circuit_picture(training_model,onp.pi/3,_weights),_fig,
        mo.md(f"Training MSE: {_history[0]:.5f} to {_history[-1]:.3g}"),
    ]))])
    exercise_two_page=mo.ui.tabs({"Tutorial":_story,"Lab":_lab},value=training_view(),on_change=set_training_view)
    return (exercise_two_page,)


@app.cell
def photonic_controls(mo):
    squeezing=mo.ui.slider(0,8,step=.5,value=5,label="Effective squeezing (dB)",show_value=True,full_width=True)
    photonic_shots=mo.ui.slider(200,10000,step=200,value=2000,label="Samples (uses of the device)",show_value=True,full_width=True)
    query=mo.ui.slider(.25,2,step=.05,value=1.5,label=r"Query frequency $b$",show_value=True,full_width=True)
    return photonic_shots, query, squeezing


@app.cell
def photonic_case(
    caption,
    circuit_picture,
    input_output,
    lesson_notes,
    mem,
    mem_fig,
    memory_view,
    mo,
    notes_beside,
    onp,
    photonic_shots,
    prose,
    prose_step,
    query,
    question,
    set_memory_view,
    source_of,
    squeezing,
):
    _latent,_observed,_nu=mem.displacement_samples(photonic_shots.value,squeezing.value)
    _,_baseline,_nu0=mem.displacement_samples(photonic_shots.value,0)
    _b=onp.linspace(0,2,81)
    _estimate=mem.characteristic_estimate(_observed,1j*_b,_nu)
    _estimate0=mem.characteristic_estimate(_baseline,1j*_b,_nu0)
    _fig=mem_fig.lab_picture(_latent,_observed,_b,_estimate0,_estimate,squeezing.value,query.value)
    _rms0=mem.rms_error(_nu0,query.value,photonic_shots.value)
    _rms=mem.rms_error(_nu,query.value,photonic_shots.value)
    _story=mo.vstack([
        mo.md("## Research case 1: learning from quantum data with a quantum memory"),
        lesson_notes(prose("memory/01-before-you-start.md")),
        mo.accordion({"Terms used in this chapter": lesson_notes(prose("memory/08-terms.md"))}),
        lesson_notes(prose("memory/02-where.md")),
        lesson_notes(prose("memory/03-background.md")),
        notes_beside(prose("memory/04-question.md"), mem_fig.timeline_picture(),
                     caption(prose("memory/04-question-caption.md"))),
        mo.accordion({"Optional: the characteristic function as eigenvalues of the device's channel":
                      lesson_notes(prose("memory/04-question-panel.md"))}),
        question("memory/04-question-q1.md"),
        question("memory/04-question-q2.md"),
        notes_beside(prose("memory/05-idea.md"),
                     mem_fig.schemes_picture(), caption(prose("memory/05-idea-caption-schemes.md")),
                     mem_fig.noise_picture(5), caption(prose("memory/05-idea-caption-noise.md"))),
        circuit_picture(mem.gaussian_sensor,.9+.1j,5),
        lesson_notes(prose("memory/05-idea-circuit.md")),
        question("memory/05-idea-q1.md"),
        question("memory/05-idea-q2.md"),
        lesson_notes(prose("memory/06-study-brief.md")),
        lesson_notes(prose("memory/07-chapter-and-study.md")),
        prose_step("memory/09-step-1.md", source_of(mem.gaussian_sensor, mem.displacement_samples)),
        prose_step("memory/10-step-2.md", source_of(mem.characteristic_estimate)),
        question("memory/10-step-2-q1.md"),
        question("memory/10-step-2-q2.md"),
        prose_step("memory/11-step-3.md", source_of(mem.characteristic_truth, mem.rms_error, mem.sample_ratio)),
        prose_step("memory/12-step-4.md", source_of(mem.many_mode_ratio)),
        lesson_notes(prose("memory/13-closing.md")),
        question("memory/13-closing-q1.md"),
        question("memory/13-closing-q2.md"),
        question("memory/13-closing-q3.md"),
        question("memory/13-closing-q4.md"),
        lesson_notes(prose("memory/13-further-reading.md")),
    ])
    _study=mo.vstack([
        mo.md("## The study in detail"),
        lesson_notes(prose("memory/study-1-tasks.md")),
        notes_beside(prose("memory/study-2-setup.md"), mem_fig.setup_picture(),
                     caption(prose("memory/study-2-setup-caption.md"))),
    ])
    _ratio=mem.sample_ratio(_rms0,_rms)
    _lab=mo.vstack([mo.md("## Quantum-memory lab"),input_output([squeezing,photonic_shots,query],mo.vstack([
        _fig,
        mo.md(f"RMS error of the estimate at $b={query.value:.2f}$ with {photonic_shots.value:,} samples: "
              f"{_rms0:.4f} at 0 dB (baseline), {_rms:.4f} at {squeezing.value:g} dB. "
              f"The baseline needs {_ratio:.1f} times as many samples to reach the same error."),
        mo.accordion({"Probe and memory circuit": circuit_picture(mem.gaussian_sensor,.9+.1j,squeezing.value)}),
    ])),
        lesson_notes(prose("memory/lab-0-intro.md")),
        question("memory/lab-1-squeezing.md"),
        question("memory/lab-2-samples.md"),
        question("memory/lab-3-query.md"),
        question("memory/lab-4-zero.md"),
    ])
    photonic_page=mo.ui.tabs({"Tutorial":_story,"Study":_study,"Lab":_lab},value=memory_view(),on_change=set_memory_view)
    return (photonic_page,)


@app.cell
def generation_controls(mo):
    training_pairs = mo.ui.slider(2000, 20000, step=2000, value=12000, label="Training pairs", show_value=True, full_width=True)
    generation_shots = mo.ui.slider(256, 4096, step=256, value=2048, label="Generated samples", show_value=True, full_width=True)
    selected_wire = mo.ui.dropdown({str(j): j for j in range(6)}, value="1", label="Selected qubit", full_width=True)
    generation_input = mo.ui.dropdown(["All zero", "Isolate selected qubit", "All one"], value="All zero", label="Generation input", full_width=True)
    return generation_input, generation_shots, selected_wire, training_pairs


@app.cell
def generation_fit(gen, training_pairs):
    generation_result = gen.run_demo(n_train=training_pairs.value)
    return (generation_result,)


@app.cell
def generation_case(
    circuit_picture,
    gen,
    gen_fig,
    generation_input,
    generation_result,
    generation_shots,
    generation_view,
    input_output,
    lesson_notes,
    mo,
    notes_beside,
    onp,
    prose,
    prose_step,
    question,
    selected_wire,
    set_generation_view,
    source_of,
    training_pairs,
):
    _result = generation_result
    _wire = selected_wire.value
    _x = {"All zero": onp.zeros(6, dtype=int), "Isolate selected qubit": gen.isolating_input(_wire),
          "All one": onp.ones(6, dtype=int)}[generation_input.value]
    _learned = _result["fit"]["beta"]
    _target_p = gen.conditional_probabilities(_x, _result["target_beta"])
    _learned_p = gen.conditional_probabilities(_x, _learned)
    _generated = gen.sample_outputs(_x, _learned, generation_shots.value, seed=31)
    _empirical = gen.empirical_probabilities(_generated)
    _fig = gen_fig.distribution_picture(_target_p, _learned_p, _empirical, _generated)
    _angles = gen_fig.angles_picture(_result["target_beta"], _learned, _result["fit"]["counts"], _wire)
    _metrics = _result["metrics"]
    _story = mo.vstack([
        mo.md("## Research case 2: train a quantum generative model from single-bit averages"),
        notes_beside(prose("generation/01-question-and-idea.md"), gen_fig.training_picture()),
        lesson_notes(prose("generation/02-study.md")),
        mo.accordion({"Terms used in this chapter": lesson_notes(prose("generation/03-terms.md"))}),
        prose_step("generation/04-step-1.md", source_of(gen.probability_circuit, gen.conditional_probabilities)),
        prose_step("generation/05-step-2.md", source_of(gen.shallow_layers)),
        circuit_picture(gen.probability_qnode, onp.zeros(6,dtype=int), _result["target_beta"]),
        gen_fig.graph_picture(1),
        question("generation/05-step-2-question-1.md"),
        prose_step("generation/06-step-3.md", source_of(gen.make_dataset, gen.local_event_mask)),
        question("generation/06-step-3-question-1.md"),
        question("generation/06-step-3-question-2.md"),
        prose_step("generation/07-step-4.md", source_of(gen.fit_local)),
        prose_step("generation/08-step-5.md", source_of(gen.sample_outputs)),
        question("generation/08-step-5-question-1.md"),
        prose_step("generation/09-step-6.md", 'result = gen.run_demo(n_train=12000)\nprint(result["metrics"]["all_zero_tvd_initial"])\nprint(result["metrics"]["all_zero_tvd_learned"])\n# Training receives only the observed pairs:\nfit = gen.fit_local(result["x_train"], result["y_train"])'),
    ])
    _lab = mo.vstack([
        mo.md("## Structured-generation lab"),
        input_output([
            training_pairs,
            question("generation/10-lab-question-1.md"),
            generation_shots,
            question("generation/10-lab-question-2.md"),
            selected_wire,generation_input,
            question("generation/10-lab-question-3.md"),
        ], mo.vstack([
            mo.md("### New bitstrings from the fitted circuit"), _fig,
            mo.md(f"Input $x$ = `{''.join(str(int(bit)) for bit in _x)}`. "
                  f"TVD between the target and the fitted circuit at this input: {gen.total_variation(_target_p,_learned_p):.4f} (0 means identical)."),
            mo.md("### Fitted angles and their training pairs"), _angles,
            mo.md(f"Input 000000, TVD before and after fitting: {_metrics['all_zero_tvd_initial']:.4f} to {_metrics['all_zero_tvd_learned']:.4f}. "
                  f"Held-out NLL on mixed inputs: {_metrics['mixed_heldout_nll_learned']:.4f} nats "
                  f"(target circuit: {_metrics['mixed_heldout_nll_oracle']:.4f}; uniform guess: {onp.log(64):.4f})."),
            mo.accordion({"Circuit for the selected input": circuit_picture(gen.probability_qnode, _x, _learned)}),
        ])),
    ])
    generative_page = mo.ui.tabs({"Tutorial":_story,"Lab":_lab},value=generation_view(),on_change=set_generation_view)
    return (generative_page,)


@app.cell
def participant_download(mo, participant_package):
    participant_zip = participant_package.build_archive(mo.notebook_dir())
    code_download = mo.download(
        data=participant_zip, filename="qml-dojo-participants.zip",
        mimetype="application/zip", label="Download participant code",
    )
    return code_download, participant_zip


@app.cell
def opening(circuit_picture, code_download, encoding_circuit, fit_regression, flow_picture,
            lesson_notes, mo, onp, quantum_model, source_of, step, tutor):
    start_page = mo.vstack([
        lesson_notes("""
        | Minutes | Chapter |
        | --- | --- |
        | 0-8 | Start: prediction, data, loss, and parameters |
        | 8-18 | Circuit exercise, including six minutes of coding |
        | 18-30 | Training exercise, including six minutes of coding |
        | 30-35 | Models: predictors, kernels, and generators |
        | 35-45 | Quantum-memory research case |
        | 45-55 | Structured-generation research case |
        | 55-60 | Outlook and discussion |
        """),

        mo.md("## Why a quantum model can learn"),
        lesson_notes(r"""
        - Encode an input in a quantum state.
        - Measure the circuit to obtain a prediction.
        - Fit gate angles from data, then test the fitted model.

        We begin with a one-qubit model. Later, we learn the noise distribution of an optical process
        from quantum data, and fit a six-qubit generator from measurements.
        """),
        lesson_notes(r"""
        ### Three learning problems

        The first exercises build a predictor. The research cases broaden what we mean by learning.
        - What data do we observe?
        - what do we infer?
        - How do we check the result?

        | Problem | Observed data | What we learn | Check |
        | --- | --- | --- | --- |
        | Predict a number | Input/target pairs $(x,y)$ | Gate angles for $f_\theta(x)$ | Prediction error |
        | Learn from quantum data | Samples from an optical process, recorded before the queries are known | The characteristic function of the process's displacement distribution | Error at queries chosen after the data |
        | Generate samples | Input/output bitstrings $(x,y)$ | Angles of a conditional generator | Whole-string probabilities and unused data |

        The predictor and the generator are quantum models for classical data.
        The optical case belongs to the other branch of QML, learning from quantum data:
        there the quantum resource is a quantum memory used to collect the data, not a circuit model.
        The generator shows how circuit structure can enable fitting.
        """),
        code_download,
        step("1. A circuit that predicts", r"""
        The input $x$ describes one example. The angles $\theta$ describe the model.
        The circuit prepares a state, applies gates, and measures an observable $M$:

        $$f_\theta(x)=\langle0|U(x,\theta)^\dagger M U(x,\theta)|0\rangle.$$

        Here $M=Z$. Individual $Z$ measurements return $+1$ or $-1$.
        Their mean estimates the expectation value. Our simulator computes that expectation value.
        Changing the gate angles changes the outcome probabilities smoothly.
        We can measure how the predictions respond, then use data to choose angles with lower prediction error.
        """, source_of(encoding_circuit, quantum_model)),
        circuit_picture(quantum_model, onp.pi/3, [onp.pi/2,onp.pi/3,onp.pi/4], "Z"),
        tutor("Which values describe the input, and which describe the model?",
              r"$x$ describes the example. The angles $\theta$ determine the model's predictions and can change during training."),
        step("2. Data determines how the parameters change", r"""
        A labeled example pairs an input $x_i$ with a target $y_i$.
        Mean squared error compares predictions with targets:

        $$L(\theta)=\frac1N\sum_i(f_\theta(x_i)-y_i)^2.$$
        $N$ counts the examples. Squaring makes either direction of error contribute positively.

        Gradient descent updates the angles:
        $\theta\leftarrow\theta-\eta\nabla_\theta L$.
        The learning rate $\eta$ controls the update size.
        This first model uses a classical optimizer around a quantum forward computation.
        """, source_of(fit_regression)),
        flow_picture("training"),
        tutor(r"What changes if we repeat the circuit with the same $\theta$?",
              "Measurement samples can change. The model's expected predictions stay fixed. Training changes the angles according to the learning rule."),
    ])
    return (start_page,)


@app.cell
def model_functions(onp, qml):
    def classical_fit(xs, targets):
        features = onp.column_stack([onp.cos(xs), onp.sin(xs)])
        coefficients = onp.linalg.lstsq(features, targets, rcond=None)[0]
        return coefficients, features @ coefficients

    @qml.qnode(qml.device("default.qubit", wires=1))
    def reuploading_model(x, weights):
        for row in weights:
            qml.RX(x, wires=0)
            qml.Rot(*row, wires=0)
        return qml.expval(qml.Z(0))

    @qml.qnode(qml.device("default.qubit", wires=1))
    def overlap_probabilities(x, other):
        qml.RX(x, wires=0)
        qml.adjoint(qml.RX)(other, wires=0)
        return qml.probs(wires=[0])

    def quantum_kernel(x, other):
        return overlap_probabilities(x, other)[0]
    return classical_fit, overlap_probabilities, quantum_kernel, reuploading_model


@app.cell
def model_controls(mo):
    repetitions = mo.ui.slider(1,4,step=1,value=2,label="Encoding repetitions",show_value=True,full_width=True)
    return (repetitions,)


@app.cell
def models(circuit_picture, flow_picture, gen, input_output, lesson_notes, mo, models_view,
           onp, overlap_probabilities, plt, quantum_kernel, repetitions,
           reuploading_model, set_models_view, source_of, step, training_model, tutor):
    _weights = onp.random.default_rng(7).uniform(-onp.pi,onp.pi,(4,3))
    _grid = onp.linspace(-onp.pi,onp.pi,128,endpoint=False)
    _one = reuploading_model(_grid,_weights[:1])
    _many = reuploading_model(_grid,_weights[:repetitions.value])
    _figure,_axes = plt.subplots(1,2,figsize=(11,3.5))
    _axes[0].plot(_grid,_one,label="One encoding")
    _axes[0].plot(_grid,_many,label="Selected model")
    _axes[0].set(xlabel=r"$x$",ylabel=r"$\langle Z\rangle$",ylim=(-1.1,1.1));_axes[0].legend(fontsize=9)
    _axes[1].bar(onp.arange(5),onp.abs(onp.fft.rfft(_many))[:5]/len(_grid))
    _axes[1].set(xlabel="Frequency",ylabel="Fourier coefficient magnitude",xticks=range(5))
    _figure.tight_layout();plt.close(_figure)
    _story = mo.vstack([
        mo.md("## Three roles for a quantum model"),
        lesson_notes(r"""
        Exercise 2 used a circuit to predict a number. We now compare that role with computing similarities and generating samples.
        For each approach, identify its input, its output, and the parameters fitted from data.

        | Approach used here | Circuit output | What gets fitted |
        | --- | --- | --- |
        | Variational predictor | A mean readout used as a prediction | Circuit angles |
        | Quantum kernel method | A similarity between two encoded examples | Coefficients of a classical predictor |
        | Circuit Born model | Sampled output bitstrings | Parameters that shape the output distribution |

        These names describe different choices. Variational training describes how parameters are fitted;
        generative modeling describes the goal. A circuit Born model can be trained variationally.
        Kernel methods can also learn their feature maps; our kernel example keeps the map fixed.
        [QNNs and kernels in the QML framework](https://arxiv.org/html/2303.09491#S2.SS2).
        """),
        flow_picture("models"),
        step("1. Variational predictors: fit angles to predict a value", r"""
        Purpose: predict a target value or class from an input.

        - Input: a number $x$, encoded in the circuit's state.
        - Output: the mean readout $f_\theta(x)$, used here as the prediction.
        - Learning: fit the gate angles $\theta$ using input/target pairs and a loss.
        - Our example: Exercise 2 fits a one-qubit circuit by gradient descent.

        The literature often calls such parametrized models quantum neural networks (QNNs).
        Their gate arrangement and encoding determine which functions they can represent.
        Repeated encoding is one design choice within this approach.
        """, source_of(training_model)),
        circuit_picture(training_model,onp.pi/3,[.3,.7]),
        tutor("Which quantities does the optimizer change in our predictor?",
              r"The two circuit angles. Input values and target values stay fixed during training. The updated angles change the predictions."),
        mo.accordion({"Design extension: repeat the encoding inside a variational predictor": mo.vstack([
            lesson_notes(r"""
            The first circuit produces sine and cosine terms that complete one cycle over an input interval of length $2\pi$.
            We call this frequency one. A term such as $\cos(2x)$ completes two cycles over that interval.

            Repeating $R_X(x)$ between adjustable blocks can add higher frequencies.
            For this circuit, $r$ encodings allow integer frequencies up to $r$; some coefficients can still vanish.
            The Lab holds the gate angles fixed and changes the number of encoding blocks.
            Its bars show how much of each frequency appears in the prediction curve.
            [Encoding and expressive power](https://arxiv.org/abs/2008.08605).
            """),
            mo.md("```python\n" + source_of(reuploading_model) + "\n```"),
            circuit_picture(reuploading_model,onp.pi/3,_weights[:2]),
            tutor("Can more optimizer updates introduce a frequency that the circuit cannot represent?",
                  "The circuit's encoding and structure determine its available frequencies. Updates change their coefficients. Changing the encoding structure changes the available frequency range."),
        ])}),
        step("2. Quantum kernel methods: predict from similarities", r"""
        Purpose: learn from how similar pairs of encoded examples are.

        - Input to the quantum computation: two examples, $x$ and $x'$.
        - Circuit output: their similarity $k(x,x')$.
        - Learning in our fixed-map example: fit coefficients in a classical kernel predictor.
        - Workflow: estimate pairwise similarities, fit that predictor, then compare new inputs with training examples.

        A feature map prepares $\lvert\phi(x)\rangle=U(x)\lvert0\rangle$.
        Our overlap kernel is
        $$k(x,x')=|\langle\phi(x')|\phi(x)\rangle|^2.$$
        Apply $U(x)$ and then $U(x')^\dagger$. The zero-outcome probability gives this squared overlap.
        It is one for equal encoded states and zero for orthogonal states.

        A fitted predictor can combine similarities as $f(x)=\sum_i a_i k(x,x_i)$.
        The displayed code computes the kernel; the coefficients $a_i$ would come from a classical learning algorithm.
        Our one-qubit kernel equals $\cos^2((x-x')/2)$, which is also cheap to evaluate classically.
        [Original quantum feature-space implementation](https://arxiv.org/abs/1804.11326).
        """, source_of(overlap_probabilities,quantum_kernel)),
        circuit_picture(overlap_probabilities,onp.pi/3,0.0),
        tutor("What remains to be learned after computing the similarities?",
              r"The classical predictor's coefficients, such as the $a_i$ in the kernel expansion. Our overlap circuit supplies similarity values. A training algorithm uses those values and the labels to fit the predictor."),
        step("3. Circuit Born models: fit a distribution and generate samples", r"""
        Purpose: produce new outputs with the patterns observed in training data.

        - Input: a prepared state and, for a conditional model, a condition $x$.
        - Output: one measured bitstring $y$ per run.
        - Learning: fit parameters that shape the probabilities of those strings.
        - Our later example: estimate six phase angles from input/output records, then generate new six-bit strings.

        The Born rule gives the conditional output distribution:
        $$p_\beta(y\mid x)=|\langle y|U(x,\beta)|0\cdots0\rangle|^2.$$
        A circuit Born machine uses these measurement probabilities as its generative model.
        Variational optimization is one fitting method; the later research case uses a direct local estimator.
        [Circuit Born machines](https://arxiv.org/abs/1804.04168).

        The two supplied functions use the same circuit layers.
        One asks the small simulator for probabilities; the other draws measured bitstrings.
        Hardware estimates those probabilities through repeated sampling.
        """, source_of(gen.probability_circuit,gen.sample_circuit)),
        tutor("Can a generative model also use variational training?",
              "Yes. Generative describes the goal of learning a distribution and producing samples. Variational describes fitting parameters by optimizing an objective. A circuit Born machine can have both descriptions."),
        lesson_notes("""
        ### Read model names along separate axes

        - Task: predict a value, classify an input, generate samples, or learn properties of a physical system.
        - Model construction: a parametrized circuit, a quantum kernel, a reservoir, or a thermal-state model.
        - Architecture: how components connect, such as convolution and pooling in a QCNN.
        - Training: which quantities are fitted and which procedure fits them.

        This is a reading guide for the selected examples. The literature uses several overlapping classifications.
        Explicit predictors and kernel predictors also have mathematical connections; their resource costs and training procedures can differ.
        [Explicit, implicit, and re-uploading models](https://arxiv.org/html/2110.13162#S2).

        The optical research case next turns to the other branch of QML, learning from quantum data,
        where the quantum resource acts in data collection rather than in the model.
        The structured-generation case then develops the sample-producing model introduced here.
        """),
        mo.accordion({"Other model names in the literature": lesson_notes("""
        These names help locate a paper within the broader literature. Several can describe the same model.

        | Name | What it specifies | Relation to the examples |
        | --- | --- | --- |
        | Quantum convolutional neural network (QCNN) | A hierarchy of local operations and pooling | A structured architecture for tasks such as quantum-state classification |
        | Quantum reservoir computing | Input-driven quantum dynamics and a trained readout | In the original scheme, the dynamics stay fixed while classical readout weights are fitted |
        | Quantum Boltzmann machine | A trainable Hamiltonian and its thermal state | An energy-based construction that can model a data distribution |
        | Quantum GAN | A generator and discriminator trained adversarially | A training arrangement for a generative task; quantum and classical components can be combined |

        Sources: [QCNN](https://arxiv.org/abs/1810.03787),
        [quantum reservoir](https://arxiv.org/abs/1602.08159),
        [quantum Boltzmann machine](https://arxiv.org/abs/1601.02036),
        [hybrid quantum GAN](https://arxiv.org/abs/1904.00043).
        """)}),
    ])
    _lab = mo.vstack([
        mo.md("## Variational encoding lab"),
        input_output([repetitions],mo.vstack([
            circuit_picture(reuploading_model,onp.pi/3,_weights[:repetitions.value]),_figure,
            mo.md("Fixed gate angles; the control changes the number of input-encoding blocks."),
        ])),
    ])
    models_page = mo.ui.tabs({"Tutorial":_story,"Lab":_lab},value=models_view(),on_change=set_models_view)
    return (models_page,)


@app.cell
def closing(lesson_notes, mo, tutor):
    outlook_page = mo.vstack([
        mo.md("## Outlook"),
        lesson_notes("""
        ### Classical-data benchmarks

        Bowles, Ahmed, and Schuld compare 12 quantum models across six task
        families and 160 datasets. Standard classical methods generally perform
        better in this benchmark. The result covers those models, datasets, and tuning choices.
        [Benchmark study](https://arxiv.org/abs/2403.07059v2).

        ### Learning from quantum data

        Liu et al. send probes entangled with a quantum memory through an unknown optical process.
        Their 100-mode estimate compares sample complexity with an extrapolated vacuum and heterodyne baseline.
        Their hypothesis test, with the query revealed after the measurements,
        beats a proven lower bound for every scheme without a quantum memory.
        [Photonic process-learning study](https://arxiv.org/html/2502.07770v2).

        ### Structured generation

        Huang et al. separate efficient training from the cost of sampling.
        The 68-physical-qubit prototype maps to 816 shallow qubits and remains
        within classical simulation reach. Larger estimates use earlier sampling
        data as a proxy. Sampling-hardness claims depend on the stated assumptions.
        [Generative-model study](https://arxiv.org/html/2509.09033v1).

        ### Noise and access

        Cotler, Gong, and Kannan show how noise in access to an unknown system
        can remove ideal learning gains, even with a fault-tolerant learner.
        They also identify structured cases where gains survive.
        [Noisy quantum learning theory](https://arxiv.org/abs/2512.10929v2).

        ### Classical learning for quantum hardware

        Sivak et al. use a classical reinforcement-learning controller to tune
        quantum error correction. Learning changes the device's control settings.
        [Reinforcement-learning control study](https://arxiv.org/abs/2511.08493v4).
        """),
        tutor("Which resource does a claimed advantage save?",
              "Name the quantity: experimental samples, runtime, memory, or another measured resource. State the task, baseline, data access, and target error."),
        lesson_notes("""
        ### Questions to investigate next

        - Which measurement correlations survive the experimental noise?
        - How does training cost grow with qubit count and circuit depth?
        - How do stronger classical samplers change the comparison?
        - What is the total cost of preparing data, fitting the model, and producing useful outputs?
        """),
        tutor("What would you change in the next experiment?",
              "Choose one change: a new target, a different readout, another encoding, fewer measurements, or a noisy device. Predict its effect, run the comparison, and record the result."),
    ])
    return (outlook_page,)


@app.cell(hide_code=True)
def heading(mo):
    mo.md("""
    # Quantum Machine Learning Dojo
    """)
    return


@app.cell(hide_code=True)
def pages(
    chapter_view,
    exercise_one_page,
    exercise_two_page,
    generative_page,
    models_page,
    mo,
    outlook_page,
    photonic_page,
    set_chapter_view,
    start_page,
):
    presentation_page = mo.ui.tabs({
        "Start":start_page, "Circuit":exercise_one_page, "Training":exercise_two_page,
        "Models":models_page, "Quantum memory":photonic_page,
        "Structured generation":generative_page, "Outlook":outlook_page,
    }, value=chapter_view(), on_change=set_chapter_view)
    presentation_page
    return (presentation_page,)


if __name__ == "__main__":
    app.run()

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
    from functools import partial
    import marimo as mo
    import numpy as onp
    from pennylane import numpy as np
    import pennylane as qml
    import matplotlib.pyplot as plt
    from matplotlib.patches import Ellipse, FancyArrowPatch, FancyBboxPatch
    import research_generation as gen
    import participant_package
    plt.rcParams.update({"font.size": 12, "mathtext.fontset": "cm", "axes.spines.top": False,
                         "axes.spines.right": False, "figure.facecolor": "white",
                         "axes.prop_cycle": plt.cycler(color=["#0f766e", "#be185d", "#b45309"])})
    return (
        Ellipse,
        FancyArrowPatch,
        FancyBboxPatch,
        gen,
        inspect,
        mo,
        np,
        onp,
        partial,
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
def diagrams(Ellipse, FancyArrowPatch, FancyBboxPatch, onp, plt):
    def flow_picture(kind="training"):
        fig, ax = plt.subplots(figsize=(12, 3.8))
        ax.set(xlim=(0, 12), ylim=(0, 4)); ax.axis("off")
        def box(x, y, text, color, width=1.65, size=11):
            ax.add_patch(FancyBboxPatch((x, y), width, .72, boxstyle="round,pad=0.05,rounding_size=0.06",
                                       facecolor=color, edgecolor="#64748b", linewidth=1))
            ax.text(x+width/2, y+.36, text, ha="center", va="center", fontsize=size)
        def arrow(a, b, color="#475569", **kw):
            ax.add_patch(FancyArrowPatch(a, b, arrowstyle="->", mutation_scale=13, color=color, **kw))
        def panel(x, y, width, height, label, color, ink):
            ax.add_patch(FancyBboxPatch((x, y), width, height, boxstyle="round,pad=0,rounding_size=0.12",
                                       facecolor=color, edgecolor="none", zorder=0))
            ax.text(x-.15, y+height-.25, label, ha="right", va="top", fontsize=11, color=ink)
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
        elif kind == "timeline":
            # Two columns, time runs downward. The amber query box is the only difference in order:
            # learning reveals the query after the data, parameter estimation knows it before.
            fig.set_size_inches(5.7, 5.2)
            ax.set(xlim=(-.9, 7.4), ylim=(2.15, 9.75))
            query = "#fef3c7"
            ax.text(1.5, 9.25, "Learning (this case)\ndata first, query later", ha="center", va="center", fontsize=11, color="#0f766e")
            ax.text(5.6, 9.25, "Parameter estimation\nquery first, data later", ha="center", va="center", fontsize=11, color="#475569")
            ax.plot([3.55, 3.55], [2.3, 9.7], color="#cbd5e1", linewidth=1, linestyle="--")
            arrow((-.45, 8.45), (-.45, 3.4))
            ax.text(-.7, 5.9, "time", rotation=90, ha="center", va="center", fontsize=10, color="#475569")
            learning = [("Run the process $N$ times\n(with or without memory)", "#ccfbf1"),
                        ("Store the samples\n$\\zeta_1,\\dots,\\zeta_N$", "#f1f5f9"),
                        ("Query revealed: $\\beta$\n(Task 2: $\\beta=\\gamma$)", query),
                        ("Answer $\\hat\\lambda(\\beta)$\nfrom the stored samples", "#f1f5f9")]
            estimation = [("Query known: $\\beta$", query),
                          ("Design the measurement\nfor this $\\beta$", "#ccfbf1"),
                          ("Run the process $N$ times\nwith that measurement", "#ccfbf1"),
                          ("Estimate $\\lambda(\\beta)$\nfor this $\\beta$ only", "#f1f5f9")]
            for x0, column in ((0.0, learning), (4.1, estimation)):
                for i, (label, color) in enumerate(column):
                    y = 7.7 - 1.4 * i
                    box(x0, y, label, color, 3.0, size=10)
                    if i < len(column) - 1: arrow((x0 + 1.5, y), (x0 + 1.5, y - .68))
            ax.text(1.5, 2.75, "One data set answers\nevery later query", ha="center", va="center", fontsize=9.5, color="#475569")
            ax.text(5.6, 2.75, "One measurement design\nper known query", ha="center", va="center", fontsize=9.5, color="#475569")
        elif kind == "local":
            # One column, top to bottom: data, one qubit's estimate, repeated per qubit, then generation.
            fig.set_size_inches(4.6, 5.4)
            ax.set(xlim=(0, 6.6), ylim=(1.1, 8.8))
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
        elif kind == "setup":
            # The optics of Liu et al. (Supplementary Section A, Fig. S1), top to bottom, grouped under
            # the gates of the circuit in step 1. Amber marks the memory, as in the two-schemes figure.
            fig.set_size_inches(5.6, 10.85)
            ax.set(xlim=(0, 7.6), ylim=(-3.9, 11.2))
            memory, teal_ink, pink_ink, gray = "#b45309", "#0f766e", "#9d174d", "#475569"
            for y0, y1, label, color, ink in ((8.55, 11.15, "Two-mode squeezing (S)", "#f0fdfa", teal_ink),
                                             (4.75, 8.35, "Device: displacement $\\alpha$ (D)", "#fdf2f8", pink_ink),
                                             (.1, 4.55, "Bell measurement (BS + homodyne)", "#f0fdfa", teal_ink)):
                ax.add_patch(FancyBboxPatch((.1, y0), 7.4, y1-y0, boxstyle="round,pad=0,rounding_size=0.12",
                                           facecolor=color, edgecolor="none", zorder=0))
                ax.text(.3, y1-.15, label, ha="left", va="top", fontsize=10.5, color=ink)
            # One beam, two polarization modes. Boxes are drawn over the lines.
            ax.plot([4.9, 4.9], [3.72, 8.75], color=gray, linewidth=2, zorder=.5)
            ax.plot([6.0, 6.0], [3.72, 8.75], color=memory, linewidth=2, zorder=.5)
            # The paper does not number the OPOs; Supp. A.2 says one is squeezed in x, the other in p.
            box(3.0, 9.85, "OPO 1\nsqueezed in $X$", "#ccfbf1", 2.1, size=10)
            box(5.3, 9.85, "OPO 2\nsqueezed in $P$", "#ccfbf1", 2.1, size=10)
            ax.text(.3, 9.55, "each OPO: PPKTP\ncrystal in a cavity,\npump 775 nm,\nsqueezed light 1550 nm",
                    ha="left", va="center", fontsize=8.5, color=gray)
            box(4.15, 8.75, "PBS, then HWP:\nmix H and V 50:50", "#ccfbf1", 2.6, size=10)
            arrow((4.05, 9.85), (4.85, 9.47)); arrow((6.35, 9.85), (6.05, 9.47))
            ax.text(4.8, 7.95, "V: probe", ha="right", va="center", fontsize=9, color=gray)
            ax.text(6.1, 7.95, "H: memory", ha="left", va="center", fontsize=9, color=memory)
            # One box for both modulators. The text gives no order; Fig. S1 draws PM, then IM.
            ax.text(1.95, 7.65, "laser beam", ha="center", va="center", fontsize=9, color=gray)
            arrow((1.95, 7.5), (1.95, 7.22))
            box(.25, 6.45, "IM sets Re $\\alpha$\nPM sets Im $\\alpha$", "#fce7f3", 3.4, size=10)
            box(4.35, 6.45, "99:1 tapping\nmirror", "#fce7f3", 2.2, size=10)
            arrow((3.65, 6.81), (4.35, 6.81))
            ax.text(4.0, 7.27, "weak coherent\nstate, V", ha="center", va="bottom", fontsize=8.5, color=pink_ink)
            box(.25, 5.0, "arbitrary waveform generator:\ndrive $\\propto f_k(t)$, amplitudes set $\\alpha_k$",
                "#fce7f3", 4.2, size=9.5)
            arrow((1.95, 5.72), (1.95, 6.45))
            ax.text(6.1, 5.95, "not displaced", ha="left", va="center", fontsize=8.5, color=memory)
            # After the second HWP the two modes are displaced squeezed vacua, no longer probe and memory.
            box(3.85, 3.0, "HWP at −22.5°: mixes H and V\n50:50, reverts the first HWP", "#ccfbf1", 3.4, size=9.5)
            arrow((4.9, 3.0), (4.9, 2.47)); arrow((6.0, 3.0), (6.0, 2.47))
            # One local oscillator beam: the PBS pairs each squeezed mode with one of its polarization components.
            box(.25, 1.75, "local oscillator (LO)\ncircular polarization", "#f1f5f9", 2.9, size=9.5)
            box(3.85, 1.75, "PBS: separates H and V,\njoins each to one LO component", "#ccfbf1", 3.4, size=9.5)
            arrow((3.15, 2.11), (3.85, 2.11))
            box(3.55, .35, "homodyne $X$", "#ccfbf1", 1.7, size=10)
            box(5.65, .35, "homodyne $P$", "#ccfbf1", 1.7, size=10)
            arrow((4.9, 1.75), (4.4, 1.07)); arrow((6.0, 1.75), (6.5, 1.07))
            ax.text(.3, .71, "each homodyne detector:\nHWP at 22.5°, PBS,\ntwo photodiodes",
                    ha="left", va="center", fontsize=8.5, color=gray)
            box(3.55, -1.0, "digitizer: time traces\nof both detectors", "#f1f5f9", 3.8, size=10)
            arrow((4.4, .35), (4.4, -.28)); arrow((6.5, .35), (6.5, -.28))
            ax.text(.3, -.64, "per mode $k$: $\\int f_k(t)\\,q(t)\\,dt$\nof each trace gives\n$\\zeta_k=\\alpha_k+\\epsilon_k$",
                    ha="left", va="center", fontsize=9, color=gray)
            # Each mode is a temporal mode: one 1 µs time bin weighted by the mode function f_k(t)
            # (Supp. A.3): a 3.8 MHz sinusoid under a Gaussian envelope of 320 ns FWHM.
            t = onp.linspace(-.5, .5, 300)
            wave = onp.cos(2*onp.pi*3.8*t) * onp.exp(-.5*(t/(.320/2.3548))**2)
            for i, label in enumerate(["mode 1", "mode 2", "mode 3", "…", "mode $n$"]):
                x0 = .3+1.45*i
                if label == "…":
                    box(x0, -2.45, "…", "#f1f5f9", 1.3, size=10)
                else:
                    box(x0, -2.45, "", "#ccfbf1", 1.3)
                    ax.plot(x0+.65+1.2*t, -2.09+.27*wave, color=teal_ink, linewidth=1)
                    ax.text(x0+.65, -2.62, label, ha="center", va="top", fontsize=9, color=gray)
            ax.text(3.8, -3.0, "time →   each mode: one 1 µs time bin, weighted by $f_k(t)$\n"
                    "$f_k(t)$: 3.8 MHz sinusoid, Gaussian envelope of 320 ns FWHM\n"
                    "one sample: $n$ modes, $n$ = 100 (Task 1) or 120 (Task 2)",
                    ha="center", va="top", fontsize=9, color=gray)
        else:
            # Side by side, top to bottom: without a memory (one mode) and with a memory (two modes).
            # The amber arrows mark the beamsplitter's second input: vacuum on the left, the memory on the right.
            fig.set_size_inches(5.4, 6.5)
            ax.set(xlim=(-.3, 7.5), ylim=(.5, 9.75))
            second_input = "#b45309"
            ax.text(1.2, 9.2, "Without a memory\none mode per use", ha="center", va="center", fontsize=11, color="#475569")
            ax.text(5.15, 9.2, "With a memory\ntwo modes per use", ha="center", va="center", fontsize=11, color="#0f766e")
            ax.plot([2.65, 2.65], [.6, 9.7], color="#cbd5e1", linewidth=1, linestyle="--")
            box(.15, 7.6, "Vacuum probe", "#f1f5f9", 2.1, size=10)
            box(.15, 5.9, "Unknown device\ndisplacement $\\alpha$", "#fce7f3", 2.1, size=10)
            box(.15, 4.2, "50:50\nbeamsplitter", "#ccfbf1", 2.1, size=10)
            box(.15, 2.5, "Detect $X$ and $P$\n(heterodyne)", "#ccfbf1", 2.1, size=10)
            box(-.15, .8, "Sample $\\zeta=\\alpha+\\epsilon$\nvariance 1/2 per part", "#f1f5f9", 2.7, size=10)
            arrow((1.2, 7.6), (1.2, 6.62)); arrow((1.4, 5.9), (1.6, 4.92))
            arrow((1.2, 4.2), (1.2, 3.22)); arrow((1.2, 2.5), (1.2, 1.52))
            arrow((.55, 5.45), (.75, 4.92), color=second_input)
            ax.text(.2, 5.62, "vacuum", ha="left", va="center", fontsize=9, color=second_input)
            box(4.05, 7.6, "Two-mode\nsqueezing", "#ccfbf1", 2.2, size=10)
            box(2.95, 5.9, "Unknown device\ndisplacement $\\alpha$", "#fce7f3", 2.0, size=10)
            box(5.35, 5.9, "Memory\nbypasses device", "#ccfbf1", 2.0, size=10)
            box(4.05, 4.2, "50:50\nbeamsplitter", "#ccfbf1", 2.2, size=10)
            box(4.05, 2.5, "Detect $X$ and $P$\n(Bell measurement)", "#ccfbf1", 2.2, size=10)
            box(3.7, .8, "Sample $\\zeta=\\alpha+\\epsilon$\nvariance $e^{-2r}/2$ per part", "#f1f5f9", 2.9, size=10)
            arrow((4.75, 7.6), (3.95, 6.62)); arrow((5.55, 7.6), (6.35, 6.62))
            arrow((3.95, 5.9), (4.6, 4.92)); arrow((6.35, 5.9), (5.7, 4.92), color=second_input)
            arrow((5.15, 4.2), (5.15, 3.22)); arrow((5.15, 2.5), (5.15, 1.52))
            ax.text(4.15, 7.15, "probe", ha="right", va="center", fontsize=9, color="#475569")
            ax.text(6.15, 7.15, "memory", ha="left", va="center", fontsize=9, color="#475569")
        fig.tight_layout(); plt.close(fig)
        return fig

    def quadrature_variances(squeezing_db):
        """Closed-form variances in units where X=(a+a^dagger)/2, so the vacuum has variance 1/4."""
        r = squeezing_db * onp.log(10) / 20
        return {
            "vacuum": 0.25,
            "squeezed_x": onp.exp(-2 * r) / 4, "squeezed_p": onp.exp(2 * r) / 4,
            "two_mode_single": onp.cosh(2 * r) / 4, "two_mode_covariance": onp.sinh(2 * r) / 4,
            "heterodyne": 0.5, "bell": onp.exp(-2 * r) / 2,
        }

    def noise_picture(squeezing_db=5):
        """Three rows: one mode, two-mode correlations, and the noise in one recorded sample."""
        v = quadrature_variances(squeezing_db)
        rng = onp.random.default_rng(3)
        gray, teal = "#64748b", "#0f766e"
        fig, axes = plt.subplots(3, 2, figsize=(4.8, 7.8))
        def frame(ax, limit, xlabel, ylabel, title):
            ax.set(xlim=(-limit, limit), ylim=(-limit, limit), aspect="equal")
            ax.set_xlabel(xlabel, fontsize=10, labelpad=1); ax.set_ylabel(ylabel, fontsize=10, labelpad=1)
            ax.set_title(title, fontsize=9.5); ax.tick_params(labelsize=7.5)
        def spread(ax, sx, sy, color, dashed=False):
            ax.add_patch(Ellipse((0, 0), 2 * sx, 2 * sy, facecolor="none" if dashed else color,
                                 alpha=1 if dashed else .3, edgecolor=color, linewidth=1.2,
                                 linestyle="--" if dashed else "-"))
        spread(axes[0, 0], .5, .5, gray)
        frame(axes[0, 0], 1.1, "$X$", "$P$", "One mode: vacuum\n" + r"$\mathrm{Var}\,X=\mathrm{Var}\,P=0.25$")
        spread(axes[0, 1], .5, .5, gray, dashed=True)
        spread(axes[0, 1], onp.sqrt(v["squeezed_x"]), onp.sqrt(v["squeezed_p"]), teal)
        frame(axes[0, 1], 1.1, "$X$", "$P$", f"One mode: squeezed, {squeezing_db:g} dB\n"
              + rf"$\mathrm{{Var}}\,X={v['squeezed_x']:.3f}$, $\mathrm{{Var}}\,P={v['squeezed_p']:.3f}$")
        c, s = v["two_mode_single"], v["two_mode_covariance"]
        for ax, sign in ((axes[1, 0], 1), (axes[1, 1], -1)):
            points = rng.multivariate_normal([0, 0], [[c, sign * s], [sign * s, c]], 500)
            ax.scatter(points[:, 0], points[:, 1], s=3, alpha=.35, color=teal, linewidths=0)
            ax.plot([-2, 2], [-2 * sign, 2 * sign], color=gray, linewidth=.9, linestyle="--")
        frame(axes[1, 0], 2, r"$X_\mathrm{p}$", r"$X_\mathrm{m}$", "Two modes: $X$ correlated\n"
              + rf"$\mathrm{{Var}}(X_\mathrm{{p}}-X_\mathrm{{m}})={v['bell']:.2f}$")
        frame(axes[1, 1], 2, r"$P_\mathrm{p}$", r"$P_\mathrm{m}$", "Two modes: $P$ anticorrelated\n"
              + rf"$\mathrm{{Var}}(P_\mathrm{{p}}+P_\mathrm{{m}})={v['bell']:.2f}$")
        for ax, variance, color, title in ((axes[2, 0], v["heterodyne"], gray, "Sample noise, no memory"),
                                           (axes[2, 1], v["bell"], teal, f"Sample noise, memory, {squeezing_db:g} dB")):
            noise = rng.normal(scale=onp.sqrt(variance), size=(500, 2))
            ax.scatter(noise[:, 0], noise[:, 1], s=3, alpha=.35, color=color, linewidths=0)
            spread(ax, onp.sqrt(variance), onp.sqrt(variance), color)
            frame(ax, 2, r"$\mathrm{Re}\,\epsilon$", r"$\mathrm{Im}\,\epsilon$", f"{title}\nvariance {variance:.2f} per part")
        fig.tight_layout(h_pad=1.0, w_pad=.8); plt.close(fig)
        return fig

    return flow_picture, noise_picture, quadrature_variances


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
def photonic_functions(onp, partial, qml):
    @partial(qml.transforms.split_non_commuting, grouping_strategy=None)
    @qml.qnode(qml.device("default.gaussian", wires=2))
    def gaussian_sensor(alpha, squeezing_db):
        r = squeezing_db * onp.log(10) / 20
        qml.TwoModeSqueezing(r, 0, wires=[0, 1])
        qml.Displacement(abs(alpha), onp.angle(alpha), wires=0)
        qml.Beamsplitter(onp.pi / 4, 0, wires=[0, 1])
        return (
            qml.expval(qml.QuadX(0)), qml.var(qml.QuadX(0)),
            qml.expval(qml.QuadP(1)), qml.var(qml.QuadP(1)),
        )

    def displacement_samples(shots, squeezing_db, seed=19):
        rng = onp.random.default_rng(seed)
        alpha = rng.choice([-0.9, 0.9], shots) + 0.12 * (
            rng.normal(size=shots) + 1j * rng.normal(size=shots)
        )
        _, vx, _, vp = gaussian_sensor(0j, squeezing_db)
        noise = (
            onp.sqrt(float(vx) / 2) * rng.normal(size=shots)
            + 1j * onp.sqrt(float(vp) / 2) * rng.normal(size=shots)
        )
        return alpha, alpha + noise, float((vx + vp) / 2)

    def characteristic_estimate(observations, beta, noise_power):
        beta = onp.atleast_1d(beta)
        phase = (
            observations.conj()[:, None] * beta[None, :]
            - beta.conj()[None, :] * observations[:, None]
        )
        return onp.exp(noise_power * abs(beta) ** 2) * onp.exp(phase).mean(axis=0)

    def characteristic_truth(b):
        return onp.cos(1.8 * b) * onp.exp(-2 * 0.12 ** 2 * b ** 2)

    return (
        characteristic_estimate,
        characteristic_truth,
        displacement_samples,
        gaussian_sensor,
    )


@app.cell
def photonic_controls(mo):
    squeezing=mo.ui.slider(0,8,step=.5,value=5,label="Effective squeezing (dB)",show_value=True,full_width=True)
    photonic_shots=mo.ui.slider(200,10000,step=200,value=2000,label="Samples (uses of the device)",show_value=True,full_width=True)
    query=mo.ui.slider(.25,2,step=.05,value=1.5,label=r"Query frequency $b$",show_value=True,full_width=True)
    return photonic_shots, query, squeezing


@app.cell
def photonic_case(
    caption,
    characteristic_estimate,
    characteristic_truth,
    circuit_picture,
    displacement_samples,
    flow_picture,
    gaussian_sensor,
    input_output,
    lesson_notes,
    memory_view,
    mo,
    noise_picture,
    notes_beside,
    onp,
    photonic_shots,
    plt,
    query,
    set_memory_view,
    source_of,
    squeezing,
    step,
    tutor,
):
    _latent,_observed,_nu=displacement_samples(photonic_shots.value,squeezing.value)
    _,_baseline,_nu0=displacement_samples(photonic_shots.value,0)
    _b=onp.linspace(0,2,81);_truth=characteristic_truth(_b)
    _estimate=characteristic_estimate(_observed,1j*_b,_nu)
    _estimate0=characteristic_estimate(_baseline,1j*_b,_nu0)
    _fig,_axes=plt.subplots(1,2,figsize=(11,3.5))
    _axes[0].scatter(_observed.real[:600],_observed.imag[:600],s=5,alpha=.25,label=r"Recorded samples $\zeta$")
    _axes[0].scatter(_latent.real[:100],_latent.imag[:100],s=7,label=r"True displacements $\alpha$ (not used by the estimator)")
    _axes[0].set(xlabel=r"Real part ($X$ direction)",ylabel=r"Imaginary part ($P$ direction)");_axes[0].legend(fontsize=9)
    _axes[0].set_title("Displacements and recorded samples", fontsize=12)
    _axes[1].plot(_b,_truth,color="#171717",label=r"Exact $\lambda$ (not available in an experiment)")
    _axes[1].plot(_b,_estimate0.real,label="Estimate at 0 dB (heterodyne baseline)",alpha=.6)
    _axes[1].plot(_b,_estimate.real,label=f"Estimate at {squeezing.value:g} dB")
    _axes[1].axvline(query.value, color="#737373", linestyle=":", linewidth=1)
    _axes[1].scatter([query.value], [characteristic_truth(query.value)], color="#171717", s=35, zorder=4)
    _axes[1].set(xlabel=r"Query frequency $b$",ylabel=r"$\mathrm{Re}\,\lambda(ib)$");_axes[1].legend(fontsize=9)
    _axes[1].set_title(r"Characteristic function at $\beta=ib$", fontsize=12)
    _fig.tight_layout();plt.close(_fig)
    _rms0=onp.sqrt((onp.exp(2*_nu0*query.value**2)-abs(characteristic_truth(query.value))**2)/photonic_shots.value)
    _rms=onp.sqrt((onp.exp(2*_nu*query.value**2)-abs(characteristic_truth(query.value))**2)/photonic_shots.value)
    _story=mo.vstack([
        mo.md("## Research case 1: learning from quantum data with a quantum memory"),
        lesson_notes(r"""
        ### Where this case sits in QML

        Quantum machine learning has two main branches, and "learning" means something different in each.

        - Quantum models for classical data: a circuit with trainable parameters is fitted to classical training data,
          then predicts or generates. The other chapters of this presentation cover this branch:
          the predictor, the kernel, and the generator.
        - Learning from quantum data: the unknown object is itself quantum, a quantum state or a quantum process.
          A learner accesses it through repeated experiments and must then predict its properties.
          This branch is *quantum learning theory*. "Learning" has its meaning from statistical learning theory:
          after the experiments, the learner receives questions about the unknown object, called *queries*,
          and must answer each one to accuracy $\epsilon$, using as few experiments as possible.
          The central quantity is the *sample complexity*, the number of experiments needed.

        This case belongs to the second branch.
        A *learning scheme* is the whole procedure: what to prepare, what to measure, and how to compute the answers.
        The paper uses this word (Theorem 3).
        The quantum resource of this case is not a circuit model.
        It is a *quantum memory*: storage of a quantum state, unmeasured, between two steps of an experiment.
        "The idea" below explains what it does.

        In this branch, quantum advantages are proven without complexity-theoretic assumptions.
        For several learning tasks, a quantum memory provably reduces the sample complexity
        by a factor that grows exponentially with system size
        ([Chen, Cotler, Huang, and Li, 2021](https://arxiv.org/abs/2111.05881)).
        These lower bounds hold for every scheme without a quantum memory.
        Experiments on up to 40 superconducting qubits have demonstrated such an advantage
        ([Huang et al., Science, 2022](https://arxiv.org/abs/2112.00778)).
        For quantum models on classical data, known advantages rely on complexity-theoretic assumptions or remain unproven,
        and standard benchmarks favor classical models (see the Outlook).

        The chapter builds the case in this order: the physics of one mode of light, the learning task,
        the idea of the quantum memory, the study, and then a simulation, step by step.
        """),
        lesson_notes(r"""
        ### Background: one mode of light

        #### Modes and quadratures

        A *mode* is one degree of freedom of the electromagnetic field, for example one polarization in one time bin.
        At a fixed place, the field of one mode oscillates at the light's frequency $\omega$.
        Any such oscillation is the sum of a cosine part and a sine part:
        $$E(t)\propto X\cos\omega t+P\sin\omega t.$$
        The two amplitudes $X$ and $P$ are the mode's *quadratures*.
        The name refers to the phase difference of a quarter period, 90 degrees, between cosine and sine.
        In quantum mechanics, $X$ and $P$ are observables that do not commute:
        $X=(a+a^\dagger)/2$ and $P=(a-a^\dagger)/(2i)$, where $a$ is the mode's annihilation operator.
        They play the roles of position and momentum of a harmonic oscillator.

        #### Phase space and homodyne detection

        The plane with axes $X$ and $P$ is the mode's *phase space*.
        Each direction in this plane, at an angle $\theta$, belongs to one quadrature, $X\cos\theta+P\sin\theta$.
        *Homodyne detection* measures one such quadrature:
        it mixes the light with a strong reference laser, and the phase of that laser sets $\theta$.

        #### Vacuum noise and squeezing

        The *vacuum state* is the state with zero photons.
        In it, $\operatorname{Var}(X)=\operatorname{Var}(P)=1/4$,
        the minimum allowed by the uncertainty relation $\operatorname{Var}(X)\operatorname{Var}(P)\geq1/16$.
        So one mode cannot have both variances below $1/4$.

        *Squeezing* reduces the variance of one quadrature and increases the variance of the other by the same factor.
        A single-mode squeezed vacuum with *squeezing parameter* $r$ has
        $\operatorname{Var}(X)=e^{-2r}/4$ and $\operatorname{Var}(P)=e^{2r}/4$.
        In optics, squeezed light is produced by nonlinear optical processes, such as parametric down-conversion.
        Squeezing is quoted in decibels: $s=10\log_{10}e^{2r}$.
        The squeezed variance is then reduced by the factor $e^{-2r}=10^{-s/10}$, which is 0.32 at 5 dB.
        Row 1 of the noise figure under "The idea" shows both states.

        #### Displacements

        A *displacement* by a complex number $\alpha$ adds a classical field of fixed amplitude to the mode:
        it adds $\operatorname{Re}\alpha$ to the cosine amplitude $X$ and $\operatorname{Im}\alpha$ to the sine amplitude $P$.
        In phase space, it moves the state of the mode by $\alpha$.
        """),
        notes_beside(r"""
        ### The question

        #### The unknown device

        Consider an optical device that applies a random displacement to every mode that passes through it.
        At each use, $\alpha$ is an independent random variable with the same probability distribution $p(\alpha)$.
        The paper calls such a device a *random displacement process*.
        The distribution $p(\alpha)$ characterizes the device's noise. It is the unknown object to be learned.

        $\alpha$ is not observed directly.
        Each use of the device gives one *sample*: a measurement result equal to $\alpha$ plus measurement noise.

        #### The learning task: samples first, queries later

        The task has two phases, as training and testing do in machine learning:

        1. Use the device $N$ times and record the $N$ samples.
        2. Afterwards, answer queries.

        In computer science, a query is a request sent to a system, which returns an answer,
        as with a database query or a question put to a trained model.
        Here the query comes from outside the learner, arrives only after the samples are recorded,
        and must be answered from the stored samples alone.
        The paper uses the same word: "After all measurements are completed, the scheme receives the query $\beta$" (Theorem 3).

        #### What a query asks

        A query is a complex number $\beta$. Its answer is the *characteristic function*
        $$\lambda(\beta)=\mathbb{E}_\alpha\left[e^{\alpha^*\beta-\beta^*\alpha}\right],$$
        the Fourier transform of $p(\alpha)$.
        The exponent equals $2i\operatorname{Im}(\alpha^*\beta)$, so the term $e^{\alpha^*\beta-\beta^*\alpha}$ is a wave across phase space.
        It oscillates when the displacement $\alpha$ moves along one direction, and it stays constant along the perpendicular direction.
        $\beta$ sets that direction and how fast the wave oscillates: one full period for every change of $\pi/\lvert\beta\rvert$ in $\alpha$.
        So $\beta$ is a frequency in phase space, the variable of the Fourier transform.
        It is not the frequency $\omega$ of the light.
        $\lambda(\beta)$ is the mean of this wave over the device's displacements.

        Each query therefore uses the displacements along one direction in phase space only:
        the direction along which its wave oscillates.
        For $\beta=ib$, for example, $\lambda(ib)$ is the mean of $e^{2ib\operatorname{Re}\alpha}$,
        so it uses only the $X$ part of each displacement.
        While the learner records the samples, it does not know which direction a later query will use.

        #### Success and sample complexity

        The learner succeeds if its estimate $\hat\lambda(\beta)$ is within $\epsilon$ of $\lambda(\beta)$ for every query in a given set.
        The question of this case is how large $N$ must be, that is, the task's sample complexity.
        It depends on how the samples are collected.

        #### The task in machine-learning terms

        | Machine-learning term | In this case |
        |:---|:---|
        | Unknown target | The distribution $p(\alpha)$ of the device's displacements |
        | Training data | The $N$ samples $\zeta_1,\dots,\zeta_N$, recorded before any query is known |
        | Learned model | The estimate $\hat\lambda(\beta)$, computed from the stored samples for any query $\beta$ |
        | Test query | A phase-space frequency $\beta$ chosen after the samples are recorded |
        | Test error | $\lvert\hat\lambda(\beta)-\lambda(\beta)\rvert$ |
        | Sample complexity | The $N$ needed for test error at most $\epsilon$ on every query in a given set |
        | Where the quantum resource acts | In data collection: the measurement scheme, with or without a quantum memory |

        One difference from standard machine learning: the learner also chooses how the data are collected,
        that is, which measurement is performed in each experiment.
        The quantum advantage in this case comes entirely from that choice.
        """, flow_picture("timeline"), caption(r"""
        Learning collects the data before the query is known;
        parameter estimation designs the measurement for a known query.
        Task 2 of the study enforces the left order.
        """)),
        notes_beside(r"""
        ### The idea

        #### Learning schemes and measurements

        Each use of the device takes a mode in and gives a mode out.
        The information about $\alpha$ is in the output state, and a scheme must measure that state to obtain it.
        A measurement turns a quantum state into a number, the measurement outcome.
        After the measurement, only the number remains. The state is no longer available.
        A scheme must also choose what to measure:
        $X$ and $P$ do not commute, so one measurement cannot determine both exactly on the same state.
        So two choices decide what a scheme can learn: when it measures, and which systems one measurement acts on.

        Every scheme stores numbers, for example in a computer file. That is classical memory.
        Quantum learning theory sorts schemes by whether they can also store quantum states:

        - A scheme *without a quantum memory* measures each output as soon as the device produces it,
          and keeps only the outcome.
          Each measurement acts on the output of one use alone.
          The scheme may use earlier outcomes to choose the next measurement.
        - A scheme *with a quantum memory* can keep quantum systems unmeasured for a while.
          Later, one measurement can act on several systems together.
          This is a *joint measurement*; learning theory also calls it an entangled measurement.

        "Memory" means this storage of a quantum state between two steps of the experiment,
        as a computer's memory stores data between two steps of a program.
        A quantum memory stores the state itself, not a measurement outcome.

        #### Without a memory: one mode per use

        The standard scheme uses a single mode for each use of the device, the *probe*.
        It prepares the probe in the vacuum state and sends it through the device.
        It then measures $X$ and $P$ of the probe simultaneously. This measurement is *heterodyne detection*.
        Heterodyne detection splits the probe on a 50:50 beamsplitter and measures $X$ on one output and $P$ on the other.
        The beamsplitter's second input port admits a mode in the vacuum state, which adds another $1/4$ to each reading.
        This added noise is the cost of measuring two non-commuting quadratures at once.
        Each sample therefore has noise variance $1/2$ in its real part and $1/2$ in its imaginary part:
        $1/4$ from the vacuum noise of the probe and $1/4$ from the second input port.

        #### A known query needs no memory

        Suppose the learner knew the query before it recorded any samples.
        Then it would need the displacements along one direction of phase space only.
        For $\beta=ib$, that direction is $X$.
        The learner could squeeze the probe in $X$ and measure $X$ alone by homodyne detection.
        Each sample would then have noise variance $e^{-2r}/4$ in $X$: 0.079 at 5 dB.
        That is less noise than the memory scheme below gives, and it needs one mode only.
        But these samples carry no information about $P$.
        They cannot answer a query along any other direction.

        #### A late query needs every direction

        In the learning task, the query arrives after the samples are recorded.
        Each sample must therefore support a query along any direction.
        With one mode, the uncertainty relation forbids low noise in $X$ and $P$ together.
        The standard single-mode scheme that covers every direction is heterodyne detection,
        with noise variance $1/2$ in each part.

        #### With a memory: two modes per use

        The quantum memory in this case is a second mode, the *memory* (m).
        Two modes have observables that neither mode has alone.
        The combinations $X_\text{p}-X_\text{m}$ and $P_\text{p}+P_\text{m}$ commute,
        although $X$ and $P$ of each single mode do not.
        So one joint measurement can determine both combinations exactly,
        and the uncertainty relation allows both variances to be small at once.
        Separate measurements cannot do this.
        Measuring $X_\text{p}$ and $X_\text{m}$ separately gives $X_\text{p}-X_\text{m}$,
        but then $P_\text{p}$ and $P_\text{m}$ can no longer be measured exactly, so $P_\text{p}+P_\text{m}$ is lost.

        *Two-mode squeezing* with parameter $r$ prepares the probe (p) and the memory in the *two-mode squeezed vacuum*, where
        $$\operatorname{Var}(X_\text{p}-X_\text{m})=\operatorname{Var}(P_\text{p}+P_\text{m})=e^{-2r}/2.$$
        For two modes in the vacuum state, both variances equal $1/2$.
        The two-mode squeezed vacuum is entangled. Each of its modes on its own has variance $\cosh(2r)/4$, above the vacuum value.

        Only the probe passes through the device. The memory is stored, unmeasured, until the probe returns.
        A joint measurement of both modes, the *Bell measurement*, then determines $X_\text{p}-X_\text{m}$ and $P_\text{p}+P_\text{m}$.
        The displacement adds $\operatorname{Re}\alpha$ and $\operatorname{Im}\alpha$ to them, so each sample is
        $$\zeta=(X_\text{p}-X_\text{m})+i\,(P_\text{p}+P_\text{m})=\alpha+\epsilon.$$
        The noise $\epsilon$ has variance $e^{-2r}/2$ in each part: 0.16 at 5 dB, against $1/2$ without a memory.
        If the memory were measured before the probe returned, only an outcome would remain,
        and the scheme would belong to the class without a quantum memory.

        #### The two schemes side by side

        | Step | Without a quantum memory | With a quantum memory |
        |:---|:---|:---|
        | Prepare | The probe alone, in the vacuum state | The probe and the memory, in the two-mode squeezed vacuum |
        | Use the device | The probe passes through it | The probe passes through it; the memory is stored, unmeasured |
        | Measure | The probe alone, by heterodyne detection | The probe and the memory together, by the Bell measurement |
        | Keep | The outcomes | The outcomes |
        | Noise per part of a sample | $1/2$ | $e^{-2r}/2$, which is 0.16 at 5 dB |

        Both schemes end with numbers only, and both use the same estimator to answer queries.
        They differ in which measurement produced the numbers.

        At 0 dB ($r=0$), the memory is an independent mode in the vacuum state.
        It then plays the role of the vacuum at the second input port in heterodyne detection,
        and the scheme with a memory reduces to the scheme without one.

        So the memory helps only when the query arrives after the samples.
        For a query known in advance, one squeezed mode measured by homodyne detection does better.
        Step 3 shows how the noise variance sets the sample complexity.
        """, flow_picture("memory"), caption(r"""
        The two schemes. Heterodyne detection mixes the probe with vacuum at the beamsplitter's second input.
        With a memory, the memory enters that same input (amber arrows).
        At 0 dB the memory is in the vacuum state, and the two schemes coincide.
        """), noise_picture(5), caption(r"""
        Quadrature noise at 5 dB, in units where $X=(a+a^\dagger)/2$.
        Row 1: one mode; squeezing narrows $X$ and widens $P$ (dashed: vacuum).
        Row 2: samples of the two-mode squeezed vacuum. Each quadrature alone is wide;
        the spread across the dashed line, $X_\text{p}-X_\text{m}$ or $P_\text{p}+P_\text{m}$, is narrow.
        Row 3: the noise $\epsilon$ in one recorded sample, without and with the memory.
        Shaded regions: one standard deviation.
        """)),
        circuit_picture(gaussian_sensor,.9+.1j,5),
        lesson_notes(r"""
        #### The scheme with a memory as a circuit

        The circuit shows one use with $\alpha=0.9+0.1i$ and 5 dB of squeezing.
        Wire 0 is the probe and wire 1 is the memory. From left to right:

        - S: two-mode squeezing with $r=5\ln(10)/20=0.58$ prepares the two-mode squeezed vacuum.
        - D: the displacement of the probe. Its parameters are $\lvert\alpha\rvert=0.91$ and $\arg\alpha=0.11$.
        - BS: a 50:50 beamsplitter, with angle $\pi/4=0.79$.
        - The two detectors are homodyne measurements of $X$ on wire 0 and $P$ on wire 1.
          The beamsplitter and these two measurements implement the Bell measurement.

        Step 1 below builds this circuit in code.
        """),
        lesson_notes(r"""
        ### The study

        Liu et al. implemented the scheme with a memory in an optical experiment.
        [Published version (Science, 2025)](https://preskill.caltech.edu/pubs/preskill-2025-quantum-learning.pdf);
        [arXiv full text](https://arxiv.org/html/2502.07770v2).
        In the experiment, the device acts on $n$ modes and applies one displacement to each.
        The $n$ displacements have a joint distribution $p(\alpha)$ on $\mathbb{C}^n$, so they can be correlated.
        The team ran two tasks.

        #### Task 1: estimate the characteristic function of a 100-mode device

        The team estimated the device's characteristic function $\lambda(\beta)$.
        They determined the sample complexity by Monte Carlo resampling of their measured data.
        At 4.8 dB of squeezing, they estimate about $10^7$ samples.
        Without squeezing ($r=0$, the scheme without a memory), they measured only smaller numbers of modes.
        An exponential fit to those results, extrapolated to 100 modes, gives about $7.3\times10^{18}$ samples:
        11.8 orders of magnitude more.

        The paper states that this comparison does not prove an advantage.
        The authors' lower bound for schemes without a memory (Theorem 3) applies to learning every process in a broad class.
        A scheme that uses prior knowledge of the specific process family could need fewer samples.

        #### Task 2: a hypothesis test with a proven advantage

        Task 2 removes that prior knowledge. It uses two families of processes:

        - Family A: $p_A(\alpha)$ is a Gaussian distribution, with characteristic function $\lambda_A(\beta)=e^{-\lvert\beta\rvert^2/2\sigma^2}$.
        - Family B: $p_B(\alpha)=p_A(\alpha)\left[1\pm4\epsilon_0\sin\!\left(2\operatorname{Im}(\alpha^\dagger\gamma)\right)\right]$ with $0<\epsilon_0\leq1/4$.
          This is $p_A$ modulated by a sinusoid whose wave vector is set by $\gamma\in\mathbb{C}^n$.
          Its characteristic function has two additional peaks, at $\beta=\gamma$ and $\beta=-\gamma$.
          The paper calls B the three-peak family.

        Each round runs in this order:

        1. A referee chooses family A or B and samples $\gamma$ from a normal distribution.
        2. The team sends $N=10^5$ probes through the process and measures all of them.
        3. The referee reveals $\gamma$, but not the family.
        4. The team evaluates its estimate $\hat\lambda(\gamma)$ and compares it with a threshold.
           In the noiseless limit, $\lambda_A(\gamma)\approx0$ and $\lvert\lambda_B(\gamma)\rvert\approx2\epsilon_0$.

        Because $\gamma$ is revealed only after the measurements, the measurement cannot be optimized for the one frequency $\beta=\gamma$.
        It must support an estimate of $\lambda(\beta)$ at any $\beta$ the referee could reveal.
        This is the defining structure of a learning task: data first, query second, as with training and test data.
        If $\gamma$ were known in advance, the task would be the estimation of one known parameter, a problem of quantum metrology.
        The late query is also what makes the authors' lower bound apply to every scheme without a memory.

        Results with 120 modes and $N=10^5$:

        - Proven bound: every scheme without a memory identifies the family with probability
          at most $0.5+3.8\times10^{-11}$. Random guessing gives 0.5.
        - Measured: the scheme with a memory identified the family with probability $0.563\pm0.025$.
          This exceeds the bound with 99.3% confidence.
        - Estimated: a scheme without a memory needs about $1.6\times10^{14}$ samples to reach 0.563.
          That is 9.2 orders of magnitude more than $10^5$.
        """),
        notes_beside(r"""
        #### How the experiment implements the scheme

        The experiment builds the circuit shown under "The idea" from optical components.
        The figure groups the components under the gates of that circuit.
        Each fact below names its source in the arXiv version.

        - S, two-mode squeezing: two optical parametric oscillators (OPOs) emit continuous-wave squeezed light at 1550 nm.
          Each OPO is an optical cavity with a nonlinear crystal (PPKTP), pumped at 775 nm (Supplementary Section A.1).
          The two outputs are single-mode squeezed vacua with orthogonal polarizations.
          Phase locks set one to be squeezed in $X$ and the other in $P$ (Supplementary Section A.2).
          A polarizing beamsplitter (PBS) combines them into one beam.
          A half-wave plate (HWP) then mixes the two polarizations 50:50 (Fig. S1).
          The result is a two-mode squeezed vacuum in the two polarization modes of one beam.
          The vertical polarization (V) is the probe, and the horizontal polarization (H) is the memory (Supplementary Section A).
          So the memory travels in the same beam as the probe.
          It is stored only for the time the probe takes to pass the device, so no separate storage device is needed.
        - D, the device: a laser beam, the displacement beam, passes an intensity modulator (IM) and a phase modulator (PM) (Fig. S1).
          The IM sets $\operatorname{Re}\alpha$ and the PM sets $\operatorname{Im}\alpha$ (Supplementary Section A.4).
          The IM also displaces the beam in $P$. The team corrects this crosstalk
          by subtracting it from the displacement that the PM sets (Supplementary Section A.4).
          An arbitrary waveform generator drives both modulators and so implements the random displacement process (Fig. S1).
          For mode $k$, each drive waveform is proportional to the mode function $f_k(t)$ (defined below).
          The amplitudes of the two waveforms set the displacement $\alpha_k$ at the 3.8 MHz sideband frequency (Supplementary Section A.4).
          The displacement beam is a weak coherent state in V polarization (Supplementary Section A.4).
          It enters the squeezed beam through a 99:1 tapping mirror, a highly reflective mirror (Supplementary Sections A and A.4).
          Because it is V-polarized, it displaces the probe and not the memory (Supplementary Section A).
        - BS and the two detectors, the Bell measurement: a second HWP, at −22.5°, reverses the polarization mixing of the first HWP.
          It mixes H and V 50:50, as the beamsplitter BS does in the circuit.
          Its outputs are two displaced single-mode squeezed vacua, in H and V.
          The displacement is split evenly between them (Supplementary Section A).
          A PBS then separates H and V.
          The local oscillator (LO), a strong coherent beam with circular polarization, enters at the same PBS.
          Each squeezed mode leaves the PBS together with the orthogonal polarization component of the LO.
          Each pair passes a HWP at 22.5° and a PBS, whose two outputs go to the two photodiodes of a balanced homodyne detector.
          The circular polarization gives the two LO components a relative phase of $\pi/2$.
          So one detector measures $X$ and the other $P$, each the squeezed quadrature of its mode (Supplementary Section A).

        A digitizer records the outputs of both detectors as time traces (Fig. S1; Supplementary Section A.3).
        Each mode is a *temporal mode*: one 1 µs time bin of the beam, weighted by a mode function $f_k(t)$ (Supplementary Section A.3).
        The mode function is a 3.8 MHz sinusoid under a Gaussian envelope with a full width at half maximum of 320 ns
        (main text; Supplementary Section A.3).
        For mode $k$, the team multiplies each trace by $f_k(t)$ and integrates (Supplementary Eq. S1).
        The two values give the entry $\zeta_k$ of the sample, as in step 2 (Supplementary Section B.2).
        One sample therefore takes $n$ time bins: $n=100$ in Task 1 and $n=120$ in Task 2.
        """, flow_picture("setup"), caption(r"""
        The optical setup, simplified from Fig. S1 of the paper.
        Each shaded group implements one gate of the circuit shown under "The idea": S, D, and the Bell measurement.
        The two vertical lines are the V and H polarization modes of one beam.
        The amber line is the memory, the H polarization, which the device does not displace.
        Bottom row: the mode function $f_k(t)$ of each temporal mode.
        Left out: the phase locks with their 50 Hz lock–measure cycle, and the optical losses.
        """)),
        lesson_notes(r"""
        ### This chapter and the study

        | | The study | This chapter |
        |:---|:---|:---|
        | Modes | 100 in Task 1, 120 in Task 2 | 1 |
        | Hardware | Optical experiment | PennyLane simulator of Gaussian states |
        | Squeezing | 0, 2.3, and 4.8 dB | 0 to 8 dB, set in the Lab |
        | Device | Family defined by a characteristic function with three peaks; displacements correlated across modes | Mixture of two Gaussians in $p(\alpha)$, centred at $-0.9$ and $+0.9$ on the real axis |
        | Estimator | Characteristic-function estimator (Eq. S9) | The same estimator, for one mode |
        | Baseline without memory | One vacuum probe per use, heterodyne detection | The 0 dB setting, which reduces to the same baseline |
        | Task 2, the hypothesis test | Included | Not included |

        A classical computer simulates one Gaussian mode exactly, in well under a second.
        With one mode, squeezing reduces the sample complexity by a constant factor: about 26 at 5 dB and query frequency $b=1.5$.
        The study's large factors come from many modes; the last question in step 5 derives the scaling.
        This chapter therefore demonstrates the noise reduction per sample, not a quantum advantage.
        The steps below simulate the scheme with a memory and estimate $\lambda$ from its samples.
        """),
        mo.accordion({"Terms used in this chapter": lesson_notes(r"""
        | Term | Meaning |
        |:---|:---|
        | Learning from quantum data | The branch of QML in which the unknown object is a quantum state or process, accessed through repeated experiments. Its theory is quantum learning theory. |
        | Learning scheme | The whole procedure: what to prepare, what to measure, and how to compute the answers. |
        | Quantum memory | Storage of a quantum state, unmeasured, between two steps of an experiment, so that it can be measured jointly with later parts. Here, the memory mode. |
        | Joint measurement | One measurement that acts on several systems together. Learning theory also calls it an entangled measurement. |
        | Query | A question about $p(\alpha)$ that the learner must answer from the stored samples: a phase-space frequency $\beta$, whose answer is $\lambda(\beta)$. It arrives after the samples are recorded. The paper uses this word (Theorem 3). |
        | Mode | One degree of freedom of the electromagnetic field, quantized as a harmonic oscillator with annihilation operator $a$. |
        | Quadratures $X$, $P$ | The cosine and sine amplitudes of the mode's field, $E(t)\propto X\cos\omega t+P\sin\omega t$. As observables, $X=(a+a^\dagger)/2$ and $P=(a-a^\dagger)/(2i)$, with $[X,P]=i/2$. |
        | Phase space | The plane with axes $X$ and $P$. The direction at angle $\theta$ belongs to the quadrature $X\cos\theta+P\sin\theta$. |
        | Displacement $\alpha$ | The operation that adds $\operatorname{Re}\alpha$ to $X$ and $\operatorname{Im}\alpha$ to $P$. |
        | Random displacement process | The paper's name for the device: at each use, $\alpha$ is an independent random variable with distribution $p(\alpha)$. |
        | Vacuum state | The state with zero photons. $\operatorname{Var}(X)=\operatorname{Var}(P)=1/4$, the minimum allowed by $\operatorname{Var}(X)\operatorname{Var}(P)\geq1/16$. |
        | Heterodyne detection | Simultaneous measurement of $X$ and $P$ of one mode: a 50:50 beamsplitter with vacuum at its second input port, then homodyne detection of $X$ on one output and $P$ on the other. It adds variance $1/4$ to each quadrature. With one vacuum probe per use, it is the study's baseline. |
        | Homodyne detection | Measurement of one quadrature, $X\cos\theta+P\sin\theta$, of one mode. The light is mixed with a strong reference laser, whose phase sets $\theta$. |
        | Squeezing | Reducing the variance of one quadrature below the vacuum value $1/4$, while the conjugate quadrature's variance grows by the same factor. A single-mode squeezed vacuum has $\operatorname{Var}(X)=e^{-2r}/4$ and $\operatorname{Var}(P)=e^{2r}/4$. |
        | Squeezing parameter $r$ | The real number that sets the strength of squeezing; $r=0$ means no squeezing. |
        | Two-mode squeezed vacuum | The entangled state prepared by two-mode squeezing with parameter $r$: $\operatorname{Var}(X_\text{p}-X_\text{m})=\operatorname{Var}(P_\text{p}+P_\text{m})=e^{-2r}/2$. |
        | Squeezing in dB | $s=10\log_{10}e^{2r}$, so $e^{-2r}=10^{-s/10}$. |
        | Effective squeezing | The squeezing that remains after optical losses. The Lab sets this value. |
        | Probe | The mode that passes through the device; wire 0 in the circuit. |
        | Memory | The mode stored outside the device and measured with the probe at the end; wire 1. |
        | Bell measurement | Joint measurement of the commuting observables $X_\text{p}-X_\text{m}$ and $P_\text{p}+P_\text{m}$: a 50:50 beamsplitter, then homodyne detection of $X$ on one output and $P$ on the other. |
        | Sample $\zeta$ | The result of one use: $\zeta=(X_\text{p}-X_\text{m})+i(P_\text{p}+P_\text{m})=\alpha+\epsilon$. |
        | Noise power $\nu$ | $\nu=e^{-2r}=10^{-s/10}$. Each part of $\epsilon$ has variance $\nu/2$. |
        | Characteristic function $\lambda(\beta)$ | The Fourier transform of $p(\alpha)$: $\lambda(\beta)=\mathbb{E}_\alpha[e^{\alpha^*\beta-\beta^*\alpha}]$. |
        | Phase-space frequency $\beta$ | The variable of the Fourier transform over phase space. The wave $e^{\alpha^*\beta-\beta^*\alpha}$ oscillates along one direction of phase space, with one period for every change of $\pi/\lvert\beta\rvert$ in $\alpha$. It is not the frequency $\omega$ of the light. |
        | Query frequency $b$ | The phase-space frequency in $\beta=ib$. The wave $e^{2ib\operatorname{Re}\alpha}$ completes one period for every change of $\pi/b$ in $\operatorname{Re}\alpha$. |
        | RMS error | Root-mean-square error: the square root of the mean squared error over repeated experiments. |
        | Sample complexity | The number of samples a scheme needs to reach a target error. |
        """)}),
        step("1. Simulate one use of the device",r"""
        `gaussian_sensor` builds the circuit shown under "The idea".
        Wire 0 is the probe and wire 1 is the memory.
        Its inputs are the displacement `alpha` and the squeezing in dB.
        It returns the mean and variance of $X$ on wire 0 and of $P$ on wire 1, in PennyLane's units (see the $\sqrt2$ question in step 2).

        Our code generates each displacement as
        $$\alpha=c+0.12\,(g_1+i\,g_2),$$
        where $c$ is $-0.9$ or $+0.9$ with probability 1/2 each, and $g_1$, $g_2$ are independent standard normal variables.
        So $p(\alpha)$ is an equal mixture of two Gaussians, centred at $-0.9$ and $+0.9$ on the real axis,
        each with standard deviation 0.12 in both the real and imaginary directions.

        The code generates each $\alpha$, so the code knows it.
        `characteristic_estimate` (step 3) never receives $\alpha$.
        Its inputs are the samples $\zeta$ and the noise power $\nu$, which follows from the squeezing.
        """,source_of(gaussian_sensor)),
        step("2. Why the memory reduces the measurement noise",r"""
        In the two-mode squeezed vacuum, $X_\text{p}$ and $X_\text{m}$ are positively correlated,
        and $P_\text{p}$ and $P_\text{m}$ are negatively correlated (row 2 of the noise figure under "The idea").
        Each single quadrature has variance $\cosh(2r)/4$, larger than the vacuum value $1/4$: 0.43 at 5 dB.
        The combinations $X_\text{p}-X_\text{m}$ and $P_\text{p}+P_\text{m}$ have variance $e^{-2r}/2$:
        0.16 at 5 dB, against $1/2$ without squeezing.

        The 50:50 beamsplitter maps these combinations onto single modes.
        After it, the $X$ quadrature of wire 0 equals $(X_\text{p}-X_\text{m})/\sqrt2$,
        and the $P$ quadrature of wire 1 equals $(P_\text{p}+P_\text{m})/\sqrt2$.
        Homodyne detection of these two quadratures is the Bell measurement.
        The displacement acts on the probe only, so it adds $\operatorname{Re}\alpha$ to $X_\text{p}-X_\text{m}$
        and $\operatorname{Im}\alpha$ to $P_\text{p}+P_\text{m}$.

        In the units defined above, the two results give one sample:
        $$\zeta=(X_\text{p}-X_\text{m})+i\,(P_\text{p}+P_\text{m})=\alpha+\epsilon.$$
        The noise $\epsilon$ is the value of the two combinations before the displacement.
        Its real and imaginary parts are independent Gaussian variables, each with variance $\nu/2$.
        The *noise power* is $\nu=e^{-2r}=10^{-s/10}$: 1 at 0 dB and 0.32 at 5 dB.

        At 0 dB ($r=0$), the memory is in the vacuum state and uncorrelated with the probe.
        Wire 1 then supplies the vacuum at the beamsplitter's second input port,
        and the circuit implements heterodyne detection of the probe alone, with noise variance $1/2$ per part.
        This is the study's baseline, and the Lab's 0 dB curve shows it.

        `displacement_samples` returns the true displacements, the samples $\zeta$, and $\nu$.
        The estimator in step 3 uses only $\zeta$ and $\nu$.
        """,source_of(displacement_samples)),
        tutor("Does more squeezing change the distribution of the displacements?",r"No. $p(\alpha)$ is the same at every setting. Squeezing reduces only the variance of $\epsilon$, from $1/2$ per part at 0 dB to 0.16 at 5 dB. In the Lab's left plot, the samples $\zeta$ lie closer to the true displacements $\alpha$ at higher squeezing."),
        tutor("Why must the memory bypass the device?",r"The real part of the sample is $X_\text{p}-X_\text{m}$. It contains $\operatorname{Re}\alpha$ only because the displacement acts on the probe alone. If the device displaced both modes by $\alpha$, $\operatorname{Re}\alpha$ would cancel in $X_\text{p}-X_\text{m}$."),
        tutor(r"Why does the code divide the readings by $\sqrt{2}$?",r"PennyLane's Gaussian simulator uses $\hbar=2$, where its quadrature $x$ equals $2X$ in the units of this chapter. The two homodyne results then have means $\sqrt{2}\operatorname{Re}\alpha$ and $\sqrt{2}\operatorname{Im}\alpha$. Dividing by $\sqrt{2}$ gives $\zeta$ in the units of $\alpha$. The simulator returns means and variances, not single measurement results, so `displacement_samples` samples each $\zeta$ from the normal distribution with those moments."),
        step("3. Estimate the characteristic function from the samples",r"""
        "The question" defined the characteristic function, the Fourier transform of $p(\alpha)$:
        $$\lambda(\beta)=\mathbb{E}_{\alpha}\left[e^{\alpha^*\beta-\beta^*\alpha}\right].$$
        It determines $p(\alpha)$ uniquely, by Fourier inversion.
        We use $\beta=ib$ with $b$ real. Then the exponent is $2ib\operatorname{Re}\alpha$, so
        $$\lambda(ib)=\mathbb{E}_{\alpha}\left[e^{2ib\operatorname{Re}\alpha}\right].$$
        Its real part is the mean of $\cos(2b\operatorname{Re}\alpha)$.
        We call $b$ the *query frequency*: the wave $e^{2ib\operatorname{Re}\alpha}$ completes one period for every change of $\pi/b$ in $\operatorname{Re}\alpha$.
        It can be chosen after all samples are recorded.

        A structure of width $d$ in $p(\alpha)$ contributes to $\lambda(ib)$ mainly at $b$ of order $1/d$.
        In our device, the separation 1.8 between the two Gaussians gives the factor $\cos(1.8b)$.
        Their standard deviation 0.12 gives the factor $e^{-2(0.12)^2b^2}$, which matters only at large $b$.

        The estimator replaces each unknown $\alpha$ with its sample $\zeta_k$:
        $$\hat\lambda(ib)=e^{\nu b^2}\,\frac1N\sum_{k=1}^{N}e^{2ib\operatorname{Re}\zeta_k}.$$
        Because $\epsilon$ is Gaussian and independent of $\alpha$, $\mathbb{E}[e^{2ib\operatorname{Re}\zeta}]=\lambda(ib)\,e^{-\nu b^2}$.
        The prefactor $e^{\nu b^2}$ removes this bias, so $\mathbb{E}[\hat\lambda(ib)]=\lambda(ib)$.
        This is the paper's Eq. S9, for one mode.
        In machine-learning terms, the stored samples are the training data and $\hat\lambda$ is the learned model:
        it answers any query $b$ after the samples are recorded.

        The prefactor also scales the statistical error.
        Each term in the sum has modulus 1, so for large $b$ the RMS error is approximately $e^{\nu b^2}/\sqrt N$.
        At $b=1.5$, $e^{\nu b^2}$ is 9.5 at 0 dB and 2.0 at 5 dB.
        Squeezing reduces $\nu$, and with it this factor.
        """,source_of(characteristic_estimate)),
        step("4. Compare the estimate with the exact answer",r"""
        We defined the synthetic device, so its characteristic function is known exactly:
        $$\lambda(ib)=\cos(1.8b)\,e^{-2(0.12)^2b^2}.$$
        The cosine comes from the two Gaussians at $\pm0.9$. The exponential comes from their standard deviation 0.12.

        `characteristic_estimate` never uses this formula. Its inputs are the samples, the query, and $\nu$.
        `characteristic_truth` is used only to score the estimate and to draw the black curve in the Lab.

        The Lab reports the *RMS error* of the estimate: the square root of its mean squared error over repeated experiments.
        At the selected query $b$, the gap between the estimate and the black curve is the test error of this one experiment;
        the RMS error is its typical size over repeated experiments.
        The Lab also reports how many times more samples the 0 dB baseline needs to reach the same RMS error.
        That ratio compares the *sample complexity* of the two settings.
        """,source_of(characteristic_truth)),
        tutor("How does the Lab compute the RMS error and the sample ratio?",r"With $N$ samples, noise power $\nu$, and query frequency $b$, the RMS error is $\sqrt{(e^{2\nu b^2}-\lvert\lambda(ib)\rvert^2)/N}$. The numerator is the variance of one term of the estimator. Averaging $N$ independent terms divides that variance by $N$, so four times as many samples halve the RMS error. The sample ratio is the numerator at 0 dB divided by the numerator at the chosen squeezing. Both quantities use the exact $\lambda$, which an experiment does not have."),
        step("5. Change one setting at a time in the Lab",r"""
        Start with $N=2000$ samples and $b=1.5$.

        - Increase the squeezing from 0 to 5 dB.
          The noise variance per part falls from $1/2$ to 0.16, so the samples lie closer to the true displacements.
          The RMS error falls from 0.21 to 0.04, and the sample ratio rises to about 26.
        - Keep the squeezing fixed and increase $N$. The RMS error falls as $1/\sqrt N$.
        - Increase $b$. The RMS error grows approximately as $e^{\nu b^2}$.
          At 0 dB, $\nu=1$, so the growth is fastest there.
        """,'latent, observed, nu = displacement_samples(2000, squeezing_db=5)\n# The estimate uses only the samples and the calibrated noise power.\nestimate = characteristic_estimate(observed, beta=1.5j, noise_power=nu)'),
        tutor("Which setting gives samples closer to the true displacements: 0 or 5 dB?", r"5 dB. The noise variance per part is $\nu/2$: 0.5 at 0 dB and 0.16 at 5 dB. Compare at equal $N$ and $b$. The distribution $p(\alpha)$ is the same in both settings."),
        tutor("Why can the estimate differ from the exact curve?", r"The estimator is unbiased: its mean over repeated experiments equals $\lambda(ib)$. One experiment with $N$ samples has a statistical error, with the RMS value shown under the plots. That error grows with $b$ because the prefactor $e^{\nu b^2}$ grows."),
        tutor("With one mode the reduction is a factor of about 26. How does the study reach 11.8 orders of magnitude?", r"With $n$ modes, a query $\beta$ has one entry per mode, and the prefactor becomes $e^{\nu\lvert\beta\rvert^2}=\prod_j e^{\nu\lvert\beta_j\rvert^2}$, one factor per mode. If every entry has modulus $b$, the number of samples needed scales as $e^{2\nu nb^2}$. The ratio between 0 dB and $s$ dB is then approximately $e^{2(1-\nu)nb^2}$, which grows exponentially with $n$. For Task 2, the paper also proves that every scheme without a memory needs a number of samples that grows exponentially with the number of modes."),
        lesson_notes(r"""
        ### What this case shows about QML

        In the predictor and generator chapters, the quantum resource is a circuit model.
        Here the model is a classical formula, and the quantum resource is the memory used to collect the data.
        With one mode, the memory reduces the sample complexity by a constant factor.
        With $n$ modes, the reduction grows exponentially with $n$, and for the study's hypothesis test it is proven.
        The memory helps only because the queries arrive after the samples: this is a learning task, not the estimation of one known parameter.
        Learning from quantum data is the branch of QML in which quantum advantages are proven without complexity-theoretic assumptions.
        """),
    ])
    _ratio=(_rms0/_rms)**2
    _lab=mo.vstack([mo.md("## Quantum-memory lab"),input_output([squeezing,photonic_shots,query],mo.vstack([
        _fig,
        mo.md(f"RMS error of the estimate at $b={query.value:.2f}$ with {photonic_shots.value:,} samples: "
              f"{_rms0:.4f} at 0 dB (baseline), {_rms:.4f} at {squeezing.value:g} dB. "
              f"The baseline needs {_ratio:.1f} times as many samples to reach the same error."),
        mo.accordion({"Probe and memory circuit": circuit_picture(gaussian_sensor,.9+.1j,squeezing.value)}),
    ]))])
    photonic_page=mo.ui.tabs({"Tutorial":_story,"Lab":_lab},value=memory_view(),on_change=set_memory_view)
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
def graph_drawing(gen, plt):
    def graph_picture(wire):
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

    return (graph_picture,)


@app.cell
def generation_case(
    circuit_picture,
    flow_picture,
    gen,
    generation_input,
    generation_result,
    generation_shots,
    generation_view,
    graph_picture,
    input_output,
    lesson_notes,
    mo,
    notes_beside,
    onp,
    plt,
    selected_wire,
    set_generation_view,
    source_of,
    step,
    training_pairs,
    tutor,
):
    _result = generation_result
    _wire = selected_wire.value
    _x = onp.zeros(6, dtype=int)
    if generation_input.value == "Isolate selected qubit":
        _x[list(gen.NEIGHBORS[_wire])] = 1
    elif generation_input.value == "All one":
        _x[:] = 1
    _learned = _result["fit"]["beta"]
    _target_p = gen.conditional_probabilities(_x, _result["target_beta"])
    _learned_p = gen.conditional_probabilities(_x, _learned)
    _generated = gen.sample_outputs(_x, _learned, generation_shots.value, seed=31)
    _empirical = gen.empirical_probabilities(_generated)
    _fig, _axes = plt.subplots(1, 2, figsize=(11, 3.5))
    _axes[0].plot(_target_p, color="#171717", label="Target circuit")
    _axes[0].plot(_learned_p, label="Fitted circuit")
    _axes[0].scatter(onp.arange(64), _empirical, s=8, alpha=.6, label="New samples")
    _axes[0].set(xlabel="Output bitstring (binary order)", ylabel="Probability",
                 xticks=[0,16,32,48,63], xticklabels=["000000","010000","100000","110000","111111"])
    _axes[0].set_title("Probability of each of the 64 bitstrings", fontsize=12)
    _axes[0].tick_params(axis="x", labelsize=8); _axes[0].legend(fontsize=9)
    _image = _axes[1].imshow(_generated[:32], cmap="PiYG", vmin=0, vmax=1, aspect="auto", interpolation="nearest")
    _fig.colorbar(_image, ax=_axes[1], ticks=[0,1], label="Output bit")
    _axes[1].set(xlabel="Qubit", ylabel="New sample", xticks=range(6))
    _axes[1].set_title("32 new bitstrings from the fitted circuit", fontsize=12)
    _fig.tight_layout(); plt.close(_fig)
    _angles, _axes = plt.subplots(1, 2, figsize=(11, 3))
    _axes[0].plot(gen.WIRES, _result["target_beta"], "o", color="#171717", label="Target")
    _axes[0].plot(gen.WIRES, _learned, "x", label="Fitted")
    _axes[0].set(xlabel="Qubit", ylabel=r"Angle $\beta_j$ (radians)"); _axes[0].legend(fontsize=9)
    _axes[1].bar(gen.WIRES, _result["fit"]["counts"], color=["#be185d" if j == _wire else "#0f766e" for j in gen.WIRES])
    _axes[1].set(xlabel="Qubit", ylabel="Pairs that isolate the qubit")
    _angles.tight_layout(); plt.close(_angles)
    _metrics = _result["metrics"]
    _story = mo.vstack([
        mo.md("## Research case 2: train a quantum generative model from single-bit averages"),
        notes_beside(r"""
        ### The question

        A *generative model* is a parametrized probability distribution that is fitted to training samples
        and can then produce new samples. A language model is an example: it fits a distribution over word sequences.

        A quantum circuit defines such a distribution.
        Each run ends with a computational-basis measurement of every qubit, which gives a bitstring $y$ such as `010011`.
        By the Born rule, a circuit that prepares the state $\lvert\psi\rangle$ gives $y$ with probability $\lvert\langle y\vert\psi\rangle\rvert^2$.
        If the gate angles are parameters, the circuit is a generative model:
        training fits the angles, and each run produces one sample.

        Two known results make a useful quantum generative model hard to obtain.

        - For some circuit families, no known classical algorithm produces samples with the circuit's probabilities
          in a time that grows only polynomially with the number of qubits.
          Complexity theory gives reasons to expect that no such algorithm exists.
        - Training large circuits by gradient descent can fail.
          The variance of the loss gradient can decrease exponentially with the number of qubits (*barren plateaus*),
          or the loss can have many suboptimal local minima.

        The study asks: is there a circuit family that a classical computer can train efficiently from data,
        but whose samples a classical computer cannot produce efficiently?

        ### The idea

        The study uses a circuit of constant depth on a grid of qubits, with four layers:

        1. Input bit $x_j$ sets the initial state of qubit $j$: $x_j=0$ gives $\lvert+\rangle$, $x_j=1$ gives $\lvert0\rangle$.
        2. Each qubit $j$ undergoes the rotation $R_Z(2\beta_j)$. The angles $\beta_j$ are the model's parameters.
        3. A CZ gate acts on every edge of the grid. CZ gates entangle neighboring qubits that start in $\lvert+\rangle$.
        4. Every qubit is measured in the $X$ basis.

        A CZ gate acts as the identity if either of its qubits is in $\lvert0\rangle$.
        So if $x_j=0$ and $x_k=1$ for every neighbor $k$ of qubit $j$, the output bit $y_j$ depends only on $\beta_j$:
        $P(y_j=1)=\sin^2\beta_j$.
        The mean of $y_j$ over the training pairs with this input pattern then determines $\beta_j$ (step 4).
        No gradient descent is needed.

        With input $x=000000$, every qubit starts in $\lvert+\rangle$ and every CZ gate entangles its two qubits.
        The output bits are then correlated across the whole grid.
        For large grids, this is the case that the study argues a classical computer cannot sample efficiently.
        The diagram shows the training steps.
        """, flow_picture("local")),
        lesson_notes(r"""
        ### The study

        Huang et al., Google Quantum AI, arXiv preprint, September 2025:
        [full text](https://arxiv.org/html/2509.09033v1); the appendices cited below are in the
        [PDF](https://arxiv.org/pdf/2509.09033v1).

        **Definition.** The paper defines *generative quantum advantage* (Definition 2):
        a quantum computer learns to generate the desired outputs substantially better than any classical computer.
        "Better" means fewer training samples, higher accuracy, faster learning or generation,
        or outputs that a classical computer cannot practically produce.
        The definition covers both learning from data and generating new samples.

        **Model.** The authors call their circuits *instantaneously deep quantum neural networks* (IDQNNs; Definition 16).
        An IDQNN has exactly the four layers listed above, so its depth is constant in the number of qubits.
        The paper proves (Lemma 2) that sampling an IDQNN gives the same output distribution as running a deep circuit on fewer qubits.
        In that mapping, one direction of the grid is time.
        Each *shallow qubit* of the IDQNN corresponds to one physical qubit at one time step of the deep circuit.
        An input bit of 0 corresponds to a gate that carries the qubit's state to the next time step.
        An input bit of 1 corresponds to a mid-circuit measurement and reset of that physical qubit.

        **Training, on a classical computer.** Each angle is computed from the mean of one output bit,
        with the formula $\hat\beta_j=\tfrac12\arccos(1-2\bar y_j)$ (Eq. S.2.1, Appendix C.2.a).
        The training data come from the same circuit family, with angles that the authors chose.
        The training inputs are a mixture: one third all zeros,
        one third with each bit 1 with probability 0.4, and one third with probability 0.8.
        For the hardware runs, the team learned each angle set from 200,000 training pairs.
        In simulations of larger circuits, about $10^6$ training pairs brought the gate errors of the learned model below $10^{-3}$,
        the best two-qubit gate error of current hardware (Fig. 2c).

        **Hardware run (measured).** A Google superconducting processor ran the deep form of the circuit:
        up to 68 physical qubits over 12 time steps, which equals $68\times12=816$ shallow qubits.
        To avoid mid-circuit measurements, the team ran only the input $x=000\ldots0$.
        The paper states that the more input bits are 0, the harder classical sampling becomes, and that this input is the hardest.
        The score is the *linear cross-entropy benchmark* of $N$ samples $y_1,\dots,y_N$ from an $n$-qubit circuit:
        $$F_\text{XEB}=\frac{2^n}{N}\sum_{k=1}^{N}p_\text{ideal}(y_k)-1,$$
        where $p_\text{ideal}$ is the noiseless circuit's output distribution.
        Uniformly random bitstrings give $F_\text{XEB}=0$. For random circuits, ideal samples give $F_\text{XEB}\approx1$.
        At sizes where $p_\text{ideal}$ is too costly to compute, the team also ran *Clifford* versions of the circuits,
        with each $2\beta_j$ rounded to a multiple of $\pi/2$.
        By the Gottesman-Knill theorem, a classical computer computes the ideal probability of any bitstring of such a circuit efficiently.
        At sizes where both scores are available, the paper reports close agreement between the Clifford XEB and the XEB of the original circuits.

        **Classical models (simulated).** Transformers with $10^6$ to $10^8$ parameters, and separately XGBoost classifiers,
        were trained on the same data to predict the output bits one at a time.
        The training data contain many pairs with $x=000\ldots0$ itself.
        These are direct samples of the target distribution at that input, which favors the classical models.
        The team drew 200,000 samples from each model and scored them with KL divergence and XEB.
        At the smallest sizes, the classical models matched the target distribution closely (Fig. 2d).
        As the size grew, their XEB fell much faster than the hardware's (Fig. 2d).
        The authors report them as substantially worse than the quantum hardware, even with its noise.

        **Beyond-classical estimate (inferred, not run).** The authors do not expect 816 shallow qubits to be beyond classical simulation.
        For a larger case, they took the 67-qubit random circuits of an earlier Google experiment (Morvan et al., the paper's Ref. 30)
        and rewrote them as an IDQNN with 34,304 shallow qubits.
        They simulated only the training step on that model.
        For generation, they used the XEB that the earlier experiment measured as a proxy for the learned model's XEB.
        They compared it with the estimated best XEB that the Frontier supercomputer could reach with $10^{30}$ floating-point operations,
        about 18,800 years of Frontier time (Fig. 2e).
        They call 34,304 an upper bound on the qubits needed, because better mappings may exist.

        **Hardness, proven under an assumption.** Sampling an IDQNN equals sampling a deep circuit (Lemma 2, proven).
        Proposition 4 then shows: if a classical algorithm with polynomial running time could sample *exactly* from such deep circuits,
        the non-uniform polynomial hierarchy would collapse to a finite level.
        The polynomial hierarchy is a sequence of complexity classes that generalizes P and NP;
        its collapse is widely considered unlikely.
        Hardness for samples that are only *approximately* right needs further conjectures, which the paper cites but does not prove.

        ### This chapter and the study

        | | The study | This chapter |
        |:---|:---|:---|
        | Size | 816 shallow qubits, run as a deep circuit on 68 physical qubits over 12 time steps | 6 qubits on a 2-by-3 grid, simulated directly |
        | Hardware | Superconducting processor, with noise | Noiseless PennyLane simulator |
        | Circuit | IDQNN (Definition 16): initial states from $x$, $R_Z$, CZ on the grid edges, $X$-basis measurement | The same four layers |
        | Input bit 1 | Initial state $\lvert0\rangle$; on hardware, a mid-circuit measurement and reset | Initial state $\lvert0\rangle$ |
        | Training data | Pairs from the same circuit family, with angles the authors chose | The same, with six angles that we chose |
        | Training inputs | One third all zeros, one third 40% ones, one third 80% ones | The same mixture |
        | Training rule | Eq. (S.2.1) | The same formula |
        | Training pairs | 200,000 per angle set | 2,000 to 20,000 (Lab slider) |
        | Score | Linear XEB against the ideal circuit | TVD and held-out NLL, computed exactly |
        | Classical models | XGBoost and transformers | Left out |
        | Classical simulation | Not expected to be hard at 816 shallow qubits; inferred hard at 34,304 | Easy: all 64 probabilities computed exactly |

        This chapter therefore demonstrates the training rule on a circuit with correlated output bits.
        It does not show a quantum advantage, and it compares with no classical generative model.
        """),
        mo.accordion({"Terms used in this chapter": lesson_notes(r"""
        | Term | Meaning |
        |:---|:---|
        | Generative model | A parametrized probability distribution, fitted to training samples, from which new samples can be drawn. |
        | Bitstring | A sequence of bits, such as `010011`. Six qubits give $2^6=64$ possible bitstrings. |
        | Conditional distribution $p(y\mid x)$ | The probability of output bitstring $y$, given input bitstring $x$. |
        | Training pair $(x,y)$ | One input bitstring and the output bitstring that the target circuit produced for it. |
        | Target circuit | The circuit with chosen angles that produced the training pairs. |
        | Fitted circuit | The same circuit with the angles that we estimate. |
        | Sample | One bitstring from one run of a circuit. |
        | Training | Estimating the angles from training pairs. The paper calls this *learning*. |
        | Generation | Running the fitted circuit to produce new samples. The paper calls this *inference*. |
        | Graph | The fixed set of qubit pairs (edges) that receive a CZ gate. Our grid has 7 edges. |
        | Neighbors | The qubits that share an edge with a given qubit. |
        | CZ gate | The two-qubit gate $\operatorname{diag}(1,1,1,-1)$: it multiplies the $\lvert11\rangle$ component by $-1$. It entangles two qubits that start in $\lvert+\rangle$, and acts as the identity when either qubit is in $\lvert0\rangle$. |
        | Angle $\beta_j$ | The adjustable parameter of qubit $j$. The code applies the phase rotation $R_Z(2\beta_j)=e^{-i\beta_jZ}$. |
        | $X$-basis measurement | A Hadamard gate followed by a computational-basis measurement. It maps the relative phase between $\lvert0\rangle$ and $\lvert1\rangle$ onto the outcome probabilities. |
        | Initial state | Input bit $x_j=0$ prepares qubit $j$ in $\lvert+\rangle$; input bit $x_j=1$ leaves it in $\lvert0\rangle$, so its CZ gates act as the identity. |
        | Isolated qubit | Qubit $j$ is isolated by input $x$ if $x_j=0$ and $x_k=1$ for every neighbor $k$. |
        | Local decoupling | The paper's name for a property of the input distribution: every qubit is isolated with probability at least inverse-polynomial in the number of qubits. The training rule needs this property. |
        | Barren plateau | A loss landscape in which the variance of the gradient decreases exponentially with the number of qubits, so gradient descent makes no progress. |
        | IDQNN | Instantaneously deep quantum neural network: the paper's name for its constant-depth circuit family (Definition 16). |
        | Shallow qubit | One qubit of the IDQNN. On hardware, it corresponds to one physical qubit at one time step of a deep circuit. |
        | Linear XEB | Linear cross-entropy benchmark: $F_\text{XEB}=2^n\,\overline{p_\text{ideal}(y)}-1$, with the mean taken over the samples. 0 for uniformly random bitstrings; about 1 for ideal samples of a random circuit. |
        | Clifford circuit | A circuit of Clifford gates; here H, CZ, and $R_Z$ with angles that are multiples of $\pi/2$. By the Gottesman-Knill theorem, a classical computer simulates it efficiently. |
        | Total variation distance (TVD) | Half the sum of the absolute differences between two distributions. 0 means they are identical. |
        | Negative log-likelihood (NLL) | The average of $-\log p(y\mid x)$ over test pairs, in nats. Lower is better. |
        | Hard to sample classically | Proven in the paper for exact samples: no classical algorithm with polynomial running time produces them, unless the non-uniform polynomial hierarchy collapses. For approximate samples, the claim rests on further conjectures. At a fixed size, it is an estimate of the classical computing cost. |
        """)}),
        step("1. Know what the generator must reproduce", r"""
        Our code builds the training data from a *target circuit* with six chosen angles,
        `TARGET_BETA` $=[0.24, 0.51, 0.73, 0.92, 1.17, 1.36]$ radians.
        Each *training pair* holds an input bitstring $x$ and an output bitstring $y$, with six bits each.
        The same input gives different outputs on different runs.
        For a fixed input, the probabilities of the outputs form the *conditional distribution* $p(y\mid x)$.

        Our goal: find angles for a second circuit, the *fitted circuit*, so that it has the same distribution for every input.

        The fitted circuit must reproduce the joint distribution of the six output bits,
        not only the six marginal distributions. Two bits give an example:

        - $P(00)=P(11)=1/2$. The two bits are always equal.
        - $P(01)=P(10)=1/2$. The two bits are always different.

        Both distributions have the same marginals, $P(y_1=1)=P(y_2=1)=1/2$, but different joint distributions.

        Six output bits allow $2^6=64$ bitstrings.
        `conditional_probabilities` computes all 64 probabilities exactly.
        We use it only to score results. The training step never calls it.
        """, source_of(gen.probability_circuit, gen.conditional_probabilities)),
        step("2. Read the circuit layer by layer", r"""
        The drawing below shows the target circuit for input $x=000000$.
        It has the four layers from the introduction. Read it from left to right.

        1. **Prepare.** Input bit $x_j=0$ applies a Hadamard gate, which prepares qubit $j$ in $\lvert+\rangle$.
           Input bit $x_j=1$ leaves the qubit in $\lvert0\rangle$.
        2. **Rotate.** $R_Z(2\beta_j)=e^{-i\beta_jZ}$ multiplies $\lvert0\rangle$ by $e^{-i\beta_j}$ and $\lvert1\rangle$ by $e^{i\beta_j}$.
           The drawing shows the value $2\beta_j$ in each $R_Z$ box.
        3. **Entangle.** A CZ gate acts on each of the 7 edges of the grid.
           A CZ gate acts as the identity when either of its qubits is in $\lvert0\rangle$.
        4. **Measure.** A Hadamard on every qubit, then a computational-basis measurement.
           Together they measure in the $X$ basis, which maps the relative phase between $\lvert0\rangle$ and $\lvert1\rangle$ onto the outcome probabilities.

        We restrict every angle to $0\le\beta_j\le\pi/2$. Step 4 explains why.

        The graph under the drawing shows which qubits share a CZ gate.
        It highlights qubit 1 and its three neighbors.
        """, source_of(gen.shallow_layers)),
        circuit_picture(gen.probability_qnode, onp.zeros(6,dtype=int), _result["target_beta"]),
        graph_picture(1),
        tutor("How many output bitstrings can six qubits produce?", r"Six qubits give $2^6=64$ bitstrings. In general, $n$ qubits give $2^n$. At the study's 816 shallow qubits there are $2^{816}\approx4\times10^{245}$ bitstrings, far more than any computer can store probabilities for."),
        step("3. Isolate one qubit", r"""
        Look at qubit 1. Its neighbors are qubits 0, 2, and 4.
        Pick the training pairs where $x_1=0$ and $x_0=x_2=x_4=1$.
        Qubit 1 then starts in $\lvert+\rangle$ and all its neighbors start in $\lvert0\rangle$.
        We say that this input *isolates* qubit 1.

        The neighbors remain in $\lvert0\rangle$ up to a phase >up to a phase? means what here?<, so every CZ gate on qubit 1 acts as the identity.
        Qubit 1 is then acted on by three gates only: Hadamard, $R_Z(2\beta_1)$, Hadamard.
        Its output bit follows
        $$P(y_1=1)=\sin^2\beta_1.$$
        No other angle enters this probability.

        Training needs, for every qubit, training pairs whose input isolates it.
        The paper calls an input distribution with this property *locally decoupling*.
        Our mixture has it. A qubit with $d$ neighbors is isolated by a fraction
        $\tfrac13\left(0.6\cdot0.4^d+0.2\cdot0.8^d\right)$ of the training pairs:
        7.5% for the qubits with two neighbors (0, 2, 3, 5) and 4.7% for the qubits with three (1, 4).
        The all-zero third of the mixture isolates no qubit.
        `local_event_mask` finds, for every qubit, the training pairs whose input isolates it. It reads only the inputs, never the angles.
        """, source_of(gen.make_dataset, gen.local_event_mask)),
        tutor("Why does an input of 1 on each neighbor isolate qubit 1?", r"An input of 1 leaves that neighbor in $\lvert0\rangle$ up to a phase. A CZ gate multiplies the $\lvert11\rangle$ component of the two-qubit state by $-1$ and leaves the other components unchanged. With one qubit in $\lvert0\rangle$, the $\lvert11\rangle$ component has zero amplitude, so the gate acts as the identity. Qubit 1's output then depends on its own angle only."),
        tutor(r"Where does $\sin^2\beta$ come from?", r"Start in $\lvert0\rangle$. The Hadamard gives $(\lvert0\rangle+\lvert1\rangle)/\sqrt2$. $R_Z(2\beta)$ multiplies the two components by $e^{-i\beta}$ and $e^{i\beta}$. The final Hadamard gives outcome 1 the amplitude $(e^{-i\beta}-e^{i\beta})/2=-i\sin\beta$. Its squared modulus is $\sin^2\beta$."),
        step("4. Compute each angle from a bit mean", r"""
        For each qubit $j$, take the $n_j$ training pairs whose input isolates it.
        Compute the mean of its output bit over these pairs. Call it $\bar y_j$.
        Solve $\bar y_j=\sin^2\beta_j$ for the angle:
        $$\hat\beta_j=\tfrac12\arccos(1-2\bar y_j).$$
        For example, $\bar y_j=1/2$ gives $\hat\beta_j=\pi/4$.
        This is the paper's Eq. (S.2.1).
        The paper's Definition 16 writes the rotation as $R_Z(\theta)=e^{-i\theta Z/2}$, so its $\theta$ equals our $2\beta$.

        Inserting the six estimates into the circuit completes the training.
        There is no loss function, no gradient, and no repeated update.
        If no training pair isolates a qubit, `fit_local` stops with an error that names the qubit.

        $\bar y_j$ has variance $\sin^2\beta_j\cos^2\beta_j/n_j$, and $d\hat\beta_j/d\bar y_j=1/(2\sin\beta_j\cos\beta_j)$.
        By the delta method, each fitted angle therefore has standard error $1/(2\sqrt{n_j})$, independent of $\beta_j$.
        The approximation fails for angles close to 0 or $\pi/2$, where that derivative diverges.
        At 12,000 training pairs, 565 pairs isolate qubit 1, so its standard error is about 0.021 radians.
        The largest error over the six angles is 0.023 radians.

        Now the angle restriction. $\sin^2\beta$ has the same value for $\beta$ and $-\beta$,
        so a bit mean cannot distinguish the two signs.
        The two signs can still give different distributions of whole bitstrings.
        Flipping the sign of $\beta_0$ alone changes the distribution at $x=000000$ by a TVD of 0.28.
        Restricting every angle to $0\le\beta_j\le\pi/2$ makes the answer unique.
        """, source_of(gen.fit_local)),
        step("5. Generate new bitstrings and score them", r"""
        Now run the fitted circuit at input $x=000000$.
        All six qubits start in $\lvert+\rangle$, and all 7 CZ gates entangle their qubits, so the six output bits are correlated.
        In the study, this is the only input run on hardware, and the one the authors call hardest to simulate classically.

        Read the first Lab plot:

        - The black curve is the target circuit's probability for each of the 64 bitstrings.
        - The colored curve is the fitted circuit's probability. The gap between the two curves is the model error.
        - The dots are frequencies in a finite set of new samples. They scatter around the colored curve.
          This scatter is sampling error.
        - In the second plot, each row is one new six-bit sample.

        Two scores measure the fit:

        - *Total variation distance* (TVD) is half the sum of the absolute differences between two distributions,
          over all 64 bitstrings. 0 means they are identical.
          At the default settings, the TVD at input 000000 falls from 0.241 for an untrained circuit
          (every angle 0.15) to 0.016 for the fitted circuit.
        - *Held-out negative log-likelihood* (NLL) averages $-\log p(y\mid x)$ over 4,096 test pairs that training never saw.
          Lower is better. The untrained circuit scores 5.110 nats, the fitted circuit 3.939, and the target circuit itself 3.938.
          Uniformly random bitstrings would score $\log 64=4.159$.

        The study scores with linear XEB instead.
        At 816 shallow qubits, the distribution has $2^{816}$ entries, so TVD and exact NLL cannot be computed.
        """, source_of(gen.sample_outputs)),
        tutor("Does generating more samples improve the fitted angles?", r"No. More samples bring the dots closer to the fitted circuit's own probabilities. The angles stay the same. Their accuracy depends on the number of training pairs that isolate each qubit."),
        step("6. Try one change at a time in the Lab", r"""
        - Set the training pairs to 2,000, then to 20,000.
          The number of isolating pairs per qubit rises from about 90–170 to about 930–1,520.
          The largest angle error falls from 0.055 to 0.016 radians, and the TVD at 000000 from 0.055 to 0.010.
        - Keep the training pairs fixed and raise the number of generated samples.
          The dots settle onto the fitted curve. The angles do not change.
        - Choose a qubit and the input "Isolate selected qubit".
          That qubit's output bit is then 1 with probability $\sin^2\hat\beta_j$, independent of the other qubits.
        - Choose the input "All one". Every qubit starts in $\lvert0\rangle$, so every CZ gate acts as the identity,
          and the final Hadamards give each bit probability 1/2: all 64 bitstrings have probability $1/64$.
          The output distribution then does not depend on the angles.

        What the chapter shows: when the circuit's graph is known, single-bit means determine its angles, although its output bits are correlated.
        What it does not show: a quantum advantage. Six qubits are easy to simulate, and we compare with no classical generative model.
        """, 'result = gen.run_demo(n_train=12000)\nprint(result["metrics"]["all_zero_tvd_initial"])\nprint(result["metrics"]["all_zero_tvd_learned"])\n# Training receives only the observed pairs:\nfit = gen.fit_local(result["x_train"], result["y_train"])'),
    ])
    _lab = mo.vstack([
        mo.md("## Structured-generation lab"),
        input_output([
            training_pairs,
            tutor("Which angles get closer to the target with more training pairs?",
                  r"All of them, on average. Compare the crosses with the dots in the angle plot. Each angle's standard error is about $1/(2\sqrt{n_j})$, where $n_j$ is that qubit's count in the bar plot. Qubits 1 and 4 have three neighbors, so fewer training pairs isolate them and their standard errors are larger."),
            generation_shots,
            tutor("Do more generated samples move the fitted curve?",
                  "No. The fitted curve and the angles stay the same. More generated samples move the dots closer to the fitted curve, because sampling error shrinks."),
            selected_wire,generation_input,
            tutor("What changes when you isolate the selected qubit?",
                  r"Its neighbors remain in $\lvert0\rangle$ up to a phase, so their CZ gates act as the identity on it. Its output bit is then 1 with probability $\sin^2\hat\beta_j$. The input All one instead prepares every qubit in $\lvert0\rangle$, which gives all 64 bitstrings probability $1/64$."),
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

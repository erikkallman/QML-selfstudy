"""Figures for the Quantum memory chapter: the timeline, the two schemes, the setup, the noise, and the Lab.

The computation is in research_memory.py. Colours follow one key in every figure:
teal for squeezing and the measurement, pink for the device, amber for the memory
and for the query.
"""

import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, FancyBboxPatch
import numpy as np

from figure_style import diagram, finish
from research_memory import characteristic_truth, quadrature_variances


def timeline_picture():
    """Learning against parameter estimation: when the query becomes known."""
    # Two columns, time runs downward. The amber query box is the only difference in order:
    # learning reveals the query after the data, parameter estimation knows it before.
    fig, ax, box, arrow, _ = diagram((5.7, 5.2), (-.9, 7.4), (2.15, 9.75))
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
    return finish(fig)


def schemes_picture():
    """The scheme without a memory beside the scheme with one."""
    # Side by side, top to bottom: without a memory (one mode) and with a memory (two modes).
    # The amber arrows mark the beamsplitter's second input: vacuum on the left, the memory on the right.
    fig, ax, box, arrow, _ = diagram((5.4, 6.5), (-.3, 7.5), (.5, 9.75))
    second_input = "#b45309"
    ax.text(1.2, 9.2, "Without a memory\none mode per use", ha="center", va="center", fontsize=11, color="#475569")
    ax.text(5.15, 9.2, "With a memory\ntwo modes per use", ha="center", va="center", fontsize=11, color="#0f766e")
    ax.plot([2.65, 2.65], [.6, 9.7], color="#cbd5e1", linewidth=1, linestyle="--")
    box(.15, 7.6, "Vacuum probe", "#f1f5f9", 2.1, size=10)
    box(.15, 5.9, "Unknown device\ndisplacement $\\alpha$", "#fce7f3", 2.1, size=10)
    box(.15, 4.2, "50:50\nbeamsplitter", "#ccfbf1", 2.1, size=10)
    box(.15, 2.5, "Detect $X$ and $P$\n(heterodyne)", "#ccfbf1", 2.1, size=10)
    box(-.15, .8, "Sample $\\zeta=\\alpha+\\eta$\nvariance 1/2 per part", "#f1f5f9", 2.7, size=10)
    arrow((1.2, 7.6), (1.2, 6.62)); arrow((1.4, 5.9), (1.6, 4.92))
    arrow((1.2, 4.2), (1.2, 3.22)); arrow((1.2, 2.5), (1.2, 1.52))
    arrow((.55, 5.45), (.75, 4.92), color=second_input)
    ax.text(.2, 5.62, "vacuum", ha="left", va="center", fontsize=9, color=second_input)
    box(4.05, 7.6, "Two-mode\nsqueezing", "#ccfbf1", 2.2, size=10)
    box(2.95, 5.9, "Unknown device\ndisplacement $\\alpha$", "#fce7f3", 2.0, size=10)
    box(5.35, 5.9, "Memory\nbypasses device", "#ccfbf1", 2.0, size=10)
    box(4.05, 4.2, "50:50\nbeamsplitter", "#ccfbf1", 2.2, size=10)
    box(4.05, 2.5, "Detect $X$ and $P$\n(Bell measurement)", "#ccfbf1", 2.2, size=10)
    box(3.7, .8, "Sample $\\zeta=\\alpha+\\eta$\nvariance $e^{-2r}/2$ per part", "#f1f5f9", 2.9, size=10)
    arrow((4.75, 7.6), (3.95, 6.62)); arrow((5.55, 7.6), (6.35, 6.62))
    arrow((3.95, 5.9), (4.6, 4.92)); arrow((6.35, 5.9), (5.7, 4.92), color=second_input)
    arrow((5.15, 4.2), (5.15, 3.22)); arrow((5.15, 2.5), (5.15, 1.52))
    ax.text(4.15, 7.15, "probe", ha="right", va="center", fontsize=9, color="#475569")
    ax.text(6.15, 7.15, "memory", ha="left", va="center", fontsize=9, color="#475569")
    return finish(fig)


def setup_picture():
    """The optics of the experiment, grouped under the gates of the circuit."""
    # The optics of Liu et al. (Supplementary Section A, Fig. S1), top to bottom, grouped under
    # the gates of the circuit in step 1. Amber marks the memory, as in the two-schemes figure.
    fig, ax, box, arrow, _ = diagram((5.6, 10.85), (0, 7.6), (-3.9, 11.2))
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
    box(.25, 5.0, "arbitrary waveform generator:\ndrive $\\propto f_j(t)$, amplitudes set $\\alpha_j$",
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
    ax.text(.3, -.64, "per mode $j$: $\\int f_j(t)\\,q(t)\\,dt$\nof each trace gives\n$\\zeta_j=\\alpha_j+\\eta_j$",
            ha="left", va="center", fontsize=9, color=gray)
    # Each mode is a temporal mode: one 1 µs time bin weighted by the mode function f_j(t)
    # (Supp. A.3): a 3.8 MHz sinusoid under a Gaussian envelope of 320 ns FWHM.
    t = np.linspace(-.5, .5, 300)
    wave = np.cos(2*np.pi*3.8*t) * np.exp(-.5*(t/(.320/2.3548))**2)
    for i, label in enumerate(["mode 1", "mode 2", "mode 3", "…", "mode $n$"]):
        x0 = .3+1.45*i
        if label == "…":
            box(x0, -2.45, "…", "#f1f5f9", 1.3, size=10)
        else:
            box(x0, -2.45, "", "#ccfbf1", 1.3)
            ax.plot(x0+.65+1.2*t, -2.09+.27*wave, color=teal_ink, linewidth=1)
            ax.text(x0+.65, -2.62, label, ha="center", va="top", fontsize=9, color=gray)
    ax.text(3.8, -3.0, "time →   each mode: one 1 µs time bin, weighted by $f_j(t)$\n"
            "$f_j(t)$: 3.8 MHz sinusoid, Gaussian envelope of 320 ns FWHM\n"
            "one sample: $n$ modes, $n$ = 100 (Task 1) or 120 (Task 2)",
            ha="center", va="top", fontsize=9, color=gray)
    return finish(fig)


def noise_picture(squeezing_db=5):
    """Three rows: one mode, two-mode correlations, and the noise in one recorded sample."""
    v = quadrature_variances(squeezing_db)
    rng = np.random.default_rng(3)
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
    spread(axes[0, 1], np.sqrt(v["squeezed_x"]), np.sqrt(v["squeezed_p"]), teal)
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
        noise = rng.normal(scale=np.sqrt(variance), size=(500, 2))
        ax.scatter(noise[:, 0], noise[:, 1], s=3, alpha=.35, color=color, linewidths=0)
        spread(ax, np.sqrt(variance), np.sqrt(variance), color)
        frame(ax, 2, r"$\mathrm{Re}\,\eta$", r"$\mathrm{Im}\,\eta$", f"{title}\nvariance {variance:.2f} per part")
    fig.tight_layout(h_pad=1.0, w_pad=.8); plt.close(fig)
    return fig


def lab_picture(latent, observed, b, estimate_baseline, estimate, squeezing_db, query_b):
    """Left: recorded samples and true displacements. Right: the estimate of Re lambda(ib) against the exact curve."""
    fig, axes = plt.subplots(1, 2, figsize=(11, 3.5))
    axes[0].scatter(observed.real[:600], observed.imag[:600], s=5, alpha=.25, label=r"Recorded samples $\zeta$")
    axes[0].scatter(latent.real[:100], latent.imag[:100], s=7, label=r"True displacements $\alpha$ (not used by the estimator)")
    axes[0].set(xlabel=r"Real part ($X$ direction)", ylabel=r"Imaginary part ($P$ direction)"); axes[0].legend(fontsize=9)
    axes[0].set_title("Displacements and recorded samples", fontsize=12)
    axes[1].plot(b, characteristic_truth(b), color="#171717", label=r"Exact $\lambda$ (not available in an experiment)")
    axes[1].plot(b, estimate_baseline.real, label="Estimate at 0 dB (heterodyne baseline)", alpha=.6)
    axes[1].plot(b, estimate.real, label=f"Estimate at {squeezing_db:g} dB")
    axes[1].axvline(query_b, color="#737373", linestyle=":", linewidth=1)
    axes[1].scatter([query_b], [characteristic_truth(query_b)], color="#171717", s=35, zorder=4)
    axes[1].set(xlabel=r"Query frequency $b$", ylabel=r"$\mathrm{Re}\,\lambda(ib)$"); axes[1].legend(fontsize=9)
    axes[1].set_title(r"Characteristic function at $\beta=ib$", fontsize=12)
    fig.tight_layout(); plt.close(fig)
    return fig

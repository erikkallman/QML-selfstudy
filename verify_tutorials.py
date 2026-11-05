"""Check the actual tutorial functions, circuits, and research estimators."""
import os
import re
from pathlib import Path
os.environ.setdefault("MPLBACKEND", "Agg")

from tutorials import app
from matplotlib.backends.backend_agg import FigureCanvasAgg
from html.parser import HTMLParser

outputs, values = app.run()

class QuestionParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.elements = []

    def handle_starttag(self, tag, attrs):
        self.elements.append((tag, dict(attrs)))

question = values["tutor"](r"Which angle changes $\langle X\rangle$?", "The final angle can change this readout.")
parser = QuestionParser()
parser.feed(question.text)
details = [attrs for tag,attrs in parser.elements if tag == "details"]
assert len(details) == 1 and "open" not in details[0]
assert any(tag == "summary" for tag,_ in parser.elements)
assert any(tag == "marimo-tex" for tag,_ in parser.elements)
assert any(attrs.get("class") == "audience-answer" for _,attrs in parser.elements)
print("PASS: audience question uses a collapsed native disclosure with rendered math")
beside = values["notes_beside"]("```text\nfirst line\nsecond line\n```", values["mem_fig"].schemes_picture()).text
assert "first line\nsecond line" in beside and "marimo-mime-renderer" in beside
print("PASS: notes beside a figure keep code-block line breaks")
assert values["presentation_page"].value == "Start"
assert values["models_page"].value == "Tutorial"
assert values["participant_zip"].startswith(b"PK")

np, qml = values["onp"], values["qml"]
model = values["quantum_model"]
theta = [np.pi / 2, np.pi / 3, np.pi / 4]
np.testing.assert_allclose([values["encoded_only"](x) for x in [0,np.pi/2,np.pi]], [1,0,-1], atol=1e-10)
np.testing.assert_allclose(model(np.pi/3,theta), -.5, atol=1e-10)
namespace = model.func.__globals__
encoder = namespace["encoding_circuit"]
try:
    namespace["encoding_circuit"] = lambda x: qml.RY(x,wires=0)
    np.testing.assert_allclose(model(np.pi/3,theta), .25, atol=1e-10)
finally:
    namespace["encoding_circuit"] = encoder
assert values["source_of"](encoder).count("qml.RX") == 1
np.testing.assert_allclose([model(np.pi/3,[theta[0],theta[1],t],"Z") for t in [0,1]], [-.5,-.5], atol=1e-10)
assert abs(model(np.pi/3,theta,"X")-model(np.pi/3,[theta[0],theta[1],0],"X")) > .1
print("PASS: circuit gates, exercise edit, source listing, and readout")

_, _, weights, history = values["fit_regression"]()
assert history[-1] < 1e-8
for options in [{"rate":0,"steps":10},{"enabled":False,"steps":10}]:
    _, _, frozen, losses = values["fit_regression"](**options)
    np.testing.assert_allclose(frozen,[.3,.7])
    np.testing.assert_allclose(losses,losses[0])
print(f"PASS: training MSE {history[0]:.8f} to {history[-1]:.4g}; frozen feedback stays flat")

weights = values["np"].array([.3,.7], requires_grad=True)
gradient = qml.grad(lambda w: values["training_model"](.6,w))(weights)
for index in range(2):
    np.testing.assert_allclose(values["shifted_derivative"](.6,weights,index),gradient[index],atol=1e-10)
xs = np.linspace(-np.pi,np.pi,21)
target = .7*np.cos(xs)+.2*np.sin(xs)
coefficients,predictions = values["classical_fit"](xs,target)
np.testing.assert_allclose(coefficients,[.7,.2],atol=1e-12)
np.testing.assert_allclose(predictions,target,atol=1e-12)
points = np.array([-.8,0,.3,1.2])
gram = np.array([[values["quantum_kernel"](x,y) for y in points] for x in points])
np.testing.assert_allclose(gram,np.cos((points[:,None]-points[None,:])/2)**2,atol=1e-12)
assert np.linalg.eigvalsh(gram).min() > -1e-12
grid = np.linspace(-np.pi,np.pi,128,endpoint=False)
angles = np.random.default_rng(7).uniform(-np.pi,np.pi,(4,3))
for count in range(1,5):
    spectrum = np.abs(np.fft.rfft(values["reuploading_model"](grid,angles[:count])))/len(grid)
    assert spectrum[count+1:].max() < 1e-12
print("PASS: parameter shift, classical baseline, quantum kernel, and encoding frequency bounds")

mem, mem_fig, gen_fig = values["mem"], values["mem_fig"], values["gen_fig"]
elapsed = mem.self_check()
figure = values["circuit_picture"](mem.gaussian_sensor,.9+.1j,5)
labels = [t.get_text() for a in figure.axes for t in a.texts]
assert any("X" in label for label in labels) and any("P" in label for label in labels), labels
canvas = FigureCanvasAgg(mem_fig.noise_picture(5))
canvas.draw()
assert np.asarray(canvas.buffer_rgba())[..., :3].std() > 5
print(f"PASS: Gaussian units, both Bell readouts, sampling law, Fourier estimator, RMS comparison, "
      f"and noise-figure variances ({elapsed:.2f}s)")

result, elapsed = values["gen"].self_check()
print(f"PASS: structured generator circuit, local estimator, held-out scores, and samples ({elapsed:.2f}s)")
for name in ["exercise_one_page","exercise_two_page","photonic_page","generative_page"]:
    assert values[name].value == "Tutorial"
from matplotlib.patches import FancyBboxPatch
diagrams = {"training": lambda: values["flow_picture"]("training"),
            "models": lambda: values["flow_picture"]("models"),
            "schemes": mem_fig.schemes_picture, "timeline": mem_fig.timeline_picture,
            "setup": mem_fig.setup_picture, "local": gen_fig.training_picture}
for kind, draw in diagrams.items():
    fig = draw()
    canvas = FigureCanvasAgg(fig)
    canvas.draw()
    assert np.asarray(canvas.buffer_rgba())[...,:3].std() > 5
    # Every label whose centre lies in a box must fit inside the smallest such box.
    renderer = canvas.get_renderer()
    for ax in fig.axes:
        boxes = [p.get_window_extent(renderer) for p in ax.patches if isinstance(p, FancyBboxPatch)]
        for label in ax.texts:
            extent = label.get_window_extent(renderer)
            centre = ((extent.x0 + extent.x1) / 2, (extent.y0 + extent.y1) / 2)
            holders = [b for b in boxes if b.contains(*centre)]
            if holders:
                holder = min(holders, key=lambda b: b.width * b.height)
                assert holder.x0 <= extent.x0 and extent.x1 <= holder.x1, (kind, label.get_text())
print("PASS: diagram labels fit inside their boxes")

# Every chapter file that tutorials.py loads exists (app.run() above would fail otherwise),
# and every file in chapters/ is loaded, so no text is left behind unused.
here = Path(__file__).resolve().parent
loaded = set(re.findall(r'(?:prose|prose_step|question)\("([^"]+\.md)"', (here / "tutorials.py").read_text()))
present = {str(path.relative_to(here / "chapters")) for path in (here / "chapters").rglob("*.md")}
assert loaded == present, (sorted(present - loaded), sorted(loaded - present))
print(f"PASS: all {len(present)} chapter files are loaded")
print(f"All tutorial checks passed ({len(outputs)} computed cells).")

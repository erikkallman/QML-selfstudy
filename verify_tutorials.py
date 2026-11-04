"""Check the actual tutorial functions, circuits, and research estimators."""
import os
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
beside = values["notes_beside"]("```text\nfirst line\nsecond line\n```", values["flow_picture"]("memory")).text
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

sensor = values["gaussian_sensor"]
for db in [0,5,8]:
    mq,vq,mp,vp = sensor(.9+.1j,db)
    np.testing.assert_allclose([mq,mp],np.sqrt(2)*np.array([.9,.1]),atol=1e-12)
    np.testing.assert_allclose([vq,vp],10**(-db/10),atol=1e-12)
figure = values["circuit_picture"](sensor,.9+.1j,5)
labels = [t.get_text() for a in figure.axes for t in a.texts]
assert any("X" in label for label in labels) and any("P" in label for label in labels), labels
sample = values["displacement_samples"]
latent,observed,nu = sample(100000,5,seed=73)
np.testing.assert_array_equal(sample(100000,5,seed=73)[1],observed)
np.testing.assert_allclose([np.var((observed-latent).real),np.var((observed-latent).imag)], nu/2,rtol=.02)
estimate,truth = values["characteristic_estimate"],values["characteristic_truth"]
np.testing.assert_allclose(estimate(observed,0,nu),1,atol=1e-12)
b=np.array([.3,.7,1.2])
assert np.max(np.abs(estimate(observed,1j*b,nu)-truth(b))) < .015
assert np.max(np.abs(estimate(latent,1j*b,0)-truth(b))) < .015
for query in [.5,1,1.5]:
    rms0=np.sqrt((np.exp(2*query**2)-abs(truth(query))**2)/2000)
    rms5=np.sqrt((np.exp(2*nu*query**2)-abs(truth(query))**2)/2000)
    assert rms5 < rms0
print("PASS: Gaussian units, both Bell readouts, sampling law, Fourier estimator, and RMS comparison")

# The noise figure uses closed-form variances in units X=(a+a^dagger)/2.
# PennyLane's x is 2X, and its wire-0 reading is (x_p - x_m)/sqrt2, so its variance is 2 * Var(X_p - X_m).
variances = values["quadrature_variances"]
for db in [0, 5, 8]:
    _, pennylane_variance, _, _ = sensor(0j, db)
    np.testing.assert_allclose(2 * variances(db)["bell"], pennylane_variance, atol=1e-12)
np.testing.assert_allclose(variances(0)["bell"], variances(0)["heterodyne"], atol=1e-12)
canvas = FigureCanvasAgg(values["noise_picture"](5))
canvas.draw()
assert np.asarray(canvas.buffer_rgba())[..., :3].std() > 5
print("PASS: noise figure variances match the PennyLane circuit; 0 dB equals heterodyne")

result, elapsed = values["gen"].self_check()
print(f"PASS: structured generator circuit, local estimator, held-out scores, and samples ({elapsed:.2f}s)")
for name in ["exercise_one_page","exercise_two_page","photonic_page","generative_page"]:
    assert values[name].value == "Tutorial"
from matplotlib.patches import FancyBboxPatch
for kind in ["training","memory","timeline","setup","local","models"]:
    fig = values["flow_picture"](kind)
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
print(f"All tutorial checks passed ({len(outputs)} computed cells).")

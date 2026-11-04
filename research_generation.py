"""Six-qubit simulation of local-decoupling learning on a known graph.

Primary source: https://arxiv.org/pdf/2509.09033v1, II, C.2.a, C.3.a, H.2.
See ../research-tutorial-methods.md for the angle convention and scope.
Only PennyLane and NumPy are needed; Matplotlib is used by self_check().
"""

import inspect
import operator
import time

import numpy as np
import pennylane as qml


N_QUBITS = 6
WIRES = tuple(range(N_QUBITS))
# A 2-by-3 grid: top row 0,1,2; bottom row 3,4,5. Each layer is disjoint.
CZ_LAYERS = (((0, 3), (1, 4), (2, 5)), ((0, 1), (3, 4)), ((1, 2), (4, 5)))
EDGES = tuple(edge for layer in CZ_LAYERS for edge in layer)
NEIGHBORS = tuple(
    tuple(v if u == j else u for u, v in EDGES if j in (u, v))
    for j in WIRES
)
BIT_WEIGHTS = 1 << np.arange(N_QUBITS - 1, -1, -1)
OUTCOMES = ((np.arange(2**N_QUBITS)[:, None] & BIT_WEIGHTS) != 0).astype(np.uint8)
TARGET_BETA = np.array([0.24, 0.51, 0.73, 0.92, 1.17, 1.36])
INITIAL_BETA = np.full(N_QUBITS, 0.15)


def _bits(values, ndim, name):
    values = np.asarray(values)
    if values.ndim != ndim or values.shape[-1] != N_QUBITS:
        raise ValueError(f"{name} must have shape (..., {N_QUBITS}) and ndim={ndim}")
    if not np.all((values == 0) | (values == 1)):
        raise ValueError(f"{name} must contain only 0 and 1")
    return values.astype(np.uint8, copy=False)


def _beta(values):
    values = np.asarray(values, dtype=float)
    if values.shape != (N_QUBITS,) or not np.all(np.isfinite(values)):
        raise ValueError(f"beta must be a finite vector of length {N_QUBITS}")
    if np.any((values < 0) | (values > np.pi / 2)):
        raise ValueError("This illustration requires 0 <= beta <= pi/2")
    return values


def _positive_count(value, name):
    if isinstance(value, (bool, np.bool_)):
        raise ValueError(f"{name} must be a positive integer")
    try:
        count = operator.index(value)
    except TypeError as error:
        raise ValueError(f"{name} must be a positive integer") from error
    if count <= 0:
        raise ValueError(f"{name} must be a positive integer")
    return count


def shallow_layers(x, beta):
    """Queue the graph circuit, then rotate X readout into Z readout.

    beta is a phase half-angle: PennyLane receives RZ(2*beta).
    These low-level drawing functions assume already validated arguments.
    """
    for j in WIRES:
        if x[j] == 0:
            qml.Hadamard(wires=j)
    for j in WIRES:
        qml.RZ(2.0 * beta[j], wires=j)
    for layer in CZ_LAYERS:
        for edge in layer:
            qml.CZ(wires=edge)
    for j in WIRES:
        qml.Hadamard(wires=j)


def probability_circuit(x, beta):
    """Named quantum function for inspect.getsource and qml.draw_mpl."""
    shallow_layers(x, beta)
    return qml.probs(wires=WIRES)


def sample_circuit(x, beta):
    """Return X-basis outcomes encoded as zero and one bits."""
    shallow_layers(x, beta)
    return qml.sample(wires=WIRES)


probability_qnode = qml.QNode(
    probability_circuit,
    qml.device("default.qubit", wires=WIRES, seed=0),
    interface=None,
    diff_method=None,
)


def conditional_probabilities(x, beta):
    """Return 64 probabilities; wire 0 is the most significant bit."""
    x = _bits(x, 1, "x")
    beta = _beta(beta)
    probabilities = np.asarray(probability_qnode(x, beta), dtype=float)
    return probabilities / probabilities.sum()


def sample_outputs(x, beta, shots=2048, seed=2025):
    """Draw fresh finite-shot samples with a new, explicitly seeded device.

    Repeating this call with identical arguments and an integer seed repeats samples.
    A persistent QNode's seed would instead advance between calls.
    """
    x = _bits(x, 1, "x")
    beta = _beta(beta)
    shots = _positive_count(shots, "shots")
    device = qml.device("default.qubit", wires=WIRES, seed=seed)
    qnode = qml.QNode(sample_circuit, device, interface=None, diff_method=None)
    values = qml.set_shots(qnode, shots=shots)(x, beta)
    return np.asarray(values, dtype=np.uint8).reshape(shots, N_QUBITS)


def make_dataset(beta, n_samples=12000, seed=17):
    """Draw independent (x,y) pairs from the C.2.a three-part input mixture.

    Equal component weights: all-zero x; iid P(x_j=1)=0.4; iid P(x_j=1)=0.8.
    Grouping repeated inputs reduces device calls without changing the law.
    """
    beta = _beta(beta)
    n_samples = _positive_count(n_samples, "n_samples")
    rng = np.random.default_rng(seed)
    component = rng.integers(0, 3, size=n_samples)
    one_probability = np.array([0.0, 0.4, 0.8])[component]
    x = (rng.random((n_samples, N_QUBITS)) < one_probability[:, None]).astype(np.uint8)
    y = np.empty_like(x)
    for pattern in np.unique(x, axis=0):
        rows = np.flatnonzero(np.all(x == pattern, axis=1))
        device_seed = int(rng.integers(0, 2**32))
        y[rows] = sample_outputs(pattern, beta, shots=len(rows), seed=device_seed)
    return x, y


def local_event_mask(x):
    """Select x_j=0 with every graph neighbor set to 1, independently per j."""
    x = _bits(x, 2, "x")
    mask = np.zeros_like(x, dtype=bool)
    for j in WIRES:
        mask[:, j] = (x[:, j] == 0) & np.all(x[:, NEIGHBORS[j]] == 1, axis=1)
    return mask


def fit_local(x, y):
    """Fit only observed local bit means. No target or probability oracle is used.

    An isolated active qubit has P(y_j=1)=sin(beta_j)**2.
    Recover each angle by inversion on the declared branch [0,pi/2].
    """
    x, y = _bits(x, 2, "x"), _bits(y, 2, "y")
    if x.shape != y.shape:
        raise ValueError("x and y must have identical shapes")
    mask = local_event_mask(x)
    counts = mask.sum(axis=0)
    if np.any(counts == 0):
        missing = np.flatnonzero(counts == 0).tolist()
        raise ValueError(f"No local-decoupling samples for wires {missing}")
    ones = (mask * y).sum(axis=0)
    mean_y = ones / counts
    beta = 0.5 * np.arccos(np.clip(1.0 - 2.0 * mean_y, -1.0, 1.0))
    return {"beta": beta, "counts": counts, "ones": ones, "mean_y": mean_y, "mask": mask}


def empirical_probabilities(y):
    """Return a normalized 64-bin histogram in the same order as qml.probs."""
    y = _bits(y, 2, "y")
    if len(y) == 0:
        raise ValueError("y must contain at least one sample")
    return np.bincount(y @ BIT_WEIGHTS, minlength=2**N_QUBITS) / len(y)


def total_variation(p, q):
    """Return 0.5 * sum(abs(p-q)) for probability vectors."""
    p, q = np.asarray(p, dtype=float), np.asarray(q, dtype=float)
    for values in (p, q):
        if values.shape != (2**N_QUBITS,) or not np.all(np.isfinite(values)):
            raise ValueError("Expected a finite probability vector of length 64")
        if np.any(values < 0) or not np.isclose(values.sum(), 1.0):
            raise ValueError("Expected normalized, nonnegative probabilities")
    return float(0.5 * np.abs(p - q).sum())


def heldout_nll(beta, x, y):
    """Mean negative log likelihood in nats on unused pairs; no smoothing.

    A zero model probability for an observed outcome correctly gives infinity.
    This evaluator uses full probabilities; the local learner does not.
    """
    beta = _beta(beta)
    x, y = _bits(x, 2, "x"), _bits(y, 2, "y")
    if x.shape != y.shape or len(x) == 0:
        raise ValueError("Expected matching, nonempty x and y arrays")
    log_probabilities = np.empty(len(y), dtype=float)
    for pattern in np.unique(x, axis=0):
        rows = np.flatnonzero(np.all(x == pattern, axis=1))
        p = conditional_probabilities(pattern, beta)
        with np.errstate(divide="ignore"):
            log_probabilities[rows] = np.log(p[y[rows] @ BIT_WEIGHTS])
    return float(-log_probabilities.mean())


def numpy_reference_probabilities(x, beta):
    """Independent dense amplitude sum for circuit verification.

    Discard a global phase, then apply the X-basis Walsh-Hadamard matrix.
    This intentionally exponential calculation is limited to six qubits.
    """
    x, beta = _bits(x, 1, "x"), _beta(beta)
    z = OUTCOMES.astype(np.int64)
    allowed = np.all(z[:, x == 1] == 0, axis=1)
    edge_parity = sum(z[:, u] * z[:, v] for u, v in EDGES) % 2
    amplitude = allowed * (-1.0) ** edge_parity * np.exp(2j * (z @ beta))
    amplitude /= np.sqrt(2.0 ** np.count_nonzero(x == 0))
    hadamard = (-1.0) ** ((z @ z.T) % 2) / np.sqrt(len(z))
    return np.abs(hadamard @ amplitude) ** 2


def run_demo(n_train=12000, n_test=4096, n_generated=2048, seed=2025):
    """Return arrays and diagnostics for a notebook, with no UI or file writes.

    Training, mixed-input holdout, all-zero holdout, and generation use separate
    SeedSequence child streams. The model is fitted once, before evaluation.
    """
    seeds = [int(s.generate_state(1)[0]) for s in np.random.SeedSequence(seed).spawn(4)]
    target_beta, initial_beta = TARGET_BETA.copy(), INITIAL_BETA.copy()
    x_train, y_train = make_dataset(target_beta, n_train, seeds[0])
    fit = fit_local(x_train, y_train)
    x_test, y_test = make_dataset(target_beta, n_test, seeds[1])
    x_eval = np.zeros(N_QUBITS, dtype=np.uint8)
    y_test_zero = sample_outputs(x_eval, target_beta, n_test, seeds[2])
    x_test_zero = np.tile(x_eval, (len(y_test_zero), 1))
    y_generated = sample_outputs(x_eval, fit["beta"], n_generated, seeds[3])
    p_target = conditional_probabilities(x_eval, target_beta)
    p_initial = conditional_probabilities(x_eval, initial_beta)
    p_learned = conditional_probabilities(x_eval, fit["beta"])
    metrics = {
        "all_zero_tvd_initial": total_variation(p_target, p_initial),
        "all_zero_tvd_learned": total_variation(p_target, p_learned),
        "generated_histogram_tvd_target": total_variation(
            p_target, empirical_probabilities(y_generated)
        ),
        "max_beta_error": float(np.max(np.abs(fit["beta"] - target_beta))),
    }
    for label, beta in (("initial", initial_beta), ("learned", fit["beta"]), ("oracle", target_beta)):
        metrics[f"mixed_heldout_nll_{label}"] = heldout_nll(beta, x_test, y_test)
        metrics[f"all_zero_heldout_nll_{label}"] = heldout_nll(beta, x_test_zero, y_test_zero)
    return {
        "target_beta": target_beta,
        "initial_beta": initial_beta,
        "fit": fit,
        "x_train": x_train,
        "y_train": y_train,
        "x_test": x_test,
        "y_test": y_test,
        "x_eval": x_eval,
        "y_test_zero": y_test_zero,
        "y_generated": y_generated,
        "p_target": p_target,
        "p_initial": p_initial,
        "p_learned": p_learned,
        "outcomes": OUTCOMES.copy(),
        "metrics": metrics,
    }


def self_check():
    """Run bounded circuit, estimator, holdout, determinism, and drawing tests."""
    started = time.perf_counter()
    if qml.__version__ != "0.45.1":
        raise RuntimeError(f"Tests target PennyLane 0.45.1, found {qml.__version__}")
    beta = TARGET_BETA.copy()
    event_masks = local_event_mask(OUTCOMES)
    probability_table = np.array([conditional_probabilities(x, beta) for x in OUTCOMES])
    reference = np.array([numpy_reference_probabilities(x, beta) for x in OUTCOMES])
    np.testing.assert_allclose(probability_table, reference, atol=2e-14, rtol=0)
    np.testing.assert_allclose(probability_table.sum(axis=1), 1.0, atol=1e-14, rtol=0)
    for j in WIRES:
        means = probability_table[event_masks[:, j]] @ OUTCOMES[:, j]
        np.testing.assert_allclose(means, np.sin(beta[j]) ** 2, atol=2e-14, rtol=0)
    uniform = conditional_probabilities(np.ones(N_QUBITS, dtype=int), beta)
    np.testing.assert_allclose(uniform, 1 / 64, atol=1e-14, rtol=0)

    # Deterministic bit means exercise the inverse, including both endpoints.
    isolated_inputs = np.repeat(1 - np.eye(N_QUBITS, dtype=int), 4, axis=0)
    synthetic_outputs = np.zeros_like(isolated_inputs)
    for j, ones in enumerate((0, 1, 2, 3, 4, 2)):
        synthetic_outputs[4 * j : 4 * j + ones, j] = 1
    exact_fit = fit_local(isolated_inputs, synthetic_outputs)
    np.testing.assert_allclose(np.sin(exact_fit["beta"]) ** 2, np.array([0, 1, 2, 3, 4, 2]) / 4)
    np.testing.assert_array_equal(exact_fit["counts"], 4)
    for bad_x in (np.zeros((5, N_QUBITS)), np.ones((5, N_QUBITS))):
        try:
            fit_local(bad_x, np.zeros_like(bad_x))
        except ValueError as error:
            assert "No local-decoupling" in str(error)
        else:
            raise AssertionError("Uninformative inputs must fail explicitly")

    zero = np.zeros(N_QUBITS, dtype=int)
    np.testing.assert_array_equal(sample_outputs(zero, beta, 128, 7), sample_outputs(zero, beta, 128, 7))
    assert sample_outputs(zero, beta, 1, 7).shape == (1, N_QUBITS)
    first, second = make_dataset(beta, 256, 11), make_dataset(beta, 256, 11)
    for a, b in zip(first, second):
        np.testing.assert_array_equal(a, b)
    np.testing.assert_array_equal(fit_local(*first)["beta"], fit_local(*second)["beta"])

    # Local means cannot recover arbitrary signs; bypass the public branch guard.
    signed = beta.copy()
    signed[0] *= -1
    signed_p = np.asarray(probability_qnode(zero, signed))
    assert total_variation(conditional_probabilities(zero, beta), signed_p / signed_p.sum()) > 0.01
    np.testing.assert_allclose(np.sin(signed) ** 2, np.sin(beta) ** 2)
    try:
        conditional_probabilities(zero, signed)
    except ValueError as error:
        assert "0 <= beta" in str(error)
    else:
        raise AssertionError("Signed beta must not silently pass the branch guard")

    result = run_demo()
    metrics = result["metrics"]
    assert result["fit"]["counts"].min() > 100
    assert metrics["max_beta_error"] < 0.08
    assert metrics["all_zero_tvd_learned"] < 0.08
    assert metrics["all_zero_tvd_learned"] < metrics["all_zero_tvd_initial"]
    for prefix in ("mixed_heldout_nll", "all_zero_heldout_nll"):
        assert metrics[f"{prefix}_learned"] < metrics[f"{prefix}_initial"]
        assert abs(metrics[f"{prefix}_learned"] - metrics[f"{prefix}_oracle"]) < 0.05
    repeated_fit = fit_local(result["x_train"], result["y_train"])
    np.testing.assert_array_equal(repeated_fit["beta"], result["fit"]["beta"])
    generated_p = empirical_probabilities(result["y_generated"])
    assert total_variation(result["p_learned"], generated_p) < 0.15
    for function in (shallow_layers, probability_circuit, sample_circuit, fit_local):
        assert f"def {function.__name__}(" in inspect.getsource(function)

    import matplotlib.pyplot as plt

    figure, _ = qml.draw_mpl(probability_qnode, decimals=2)(zero, result["fit"]["beta"])
    figure.canvas.draw()
    pixels = np.asarray(figure.canvas.buffer_rgba())
    assert pixels[..., :3].std() > 1
    plt.close(figure)
    return result, time.perf_counter() - started


if __name__ == "__main__":
    demo, elapsed = self_check()
    print("PASS: six-qubit local-decoupling method illustration; no advantage claim")
    print(f"PennyLane {qml.__version__}; NumPy {np.__version__}")
    print("Selected samples per wire:", demo["fit"]["counts"].tolist())
    print("Target beta:", np.round(demo["target_beta"], 6).tolist())
    print("Learned beta:", np.round(demo["fit"]["beta"], 6).tolist())
    for key, value in demo["metrics"].items():
        print(f"{key}: {value:.6f}")
    print(f"Self-check time, excluding imports: {elapsed:.3f} s")

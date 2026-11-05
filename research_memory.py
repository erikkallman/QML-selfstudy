"""One-mode simulation of learning a random displacement process with a quantum memory.

Primary source: Liu et al., https://arxiv.org/html/2502.07770v2, Appendix B.2, Eq. S9.
See ../research-tutorial-methods.md for the units, the process, and the scope.
Only PennyLane and NumPy are needed. The figures are in research_memory_figures.py.

Plain NumPy is imported as onp, as in tutorials.py, because the chapter shows
the source of these functions next to code that uses PennyLane's numpy as np.
"""

from functools import partial
import time

import numpy as onp
import pennylane as qml


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


def rms_error(noise_power, b, shots):
    """RMS error of characteristic_estimate at beta = ib, from the exact characteristic function."""
    return onp.sqrt((onp.exp(2 * noise_power * b ** 2) - abs(characteristic_truth(b)) ** 2) / shots)


def sample_ratio(baseline_rms, rms):
    """How many times more samples the baseline needs to reach the same RMS error."""
    return (baseline_rms / rms) ** 2


def many_mode_ratio(noise_power, b, modes):
    """Approximate sample ratio between 0 dB and noise power nu, for queries with |beta_j| = b on every mode.

    The prefactor of the estimator is a product of one factor per mode, so the ratio of the
    samples needed grows as exp(2 (1 - nu) n b^2): exponentially in the number of modes n.
    """
    return onp.exp(2 * (1 - noise_power) * modes * b ** 2)


def quadrature_variances(squeezing_db):
    """Closed-form variances in units where X=(a+a^dagger)/2, so the vacuum has variance 1/4."""
    r = squeezing_db * onp.log(10) / 20
    return {
        "vacuum": 0.25,
        "squeezed_x": onp.exp(-2 * r) / 4, "squeezed_p": onp.exp(2 * r) / 4,
        "two_mode_single": onp.cosh(2 * r) / 4, "two_mode_covariance": onp.sinh(2 * r) / 4,
        "heterodyne": 0.5, "bell": onp.exp(-2 * r) / 2,
    }


def self_check():
    """Check the Gaussian units, the sampling law, the estimator, the RMS comparison, and the variances."""
    started = time.perf_counter()
    for db in [0, 5, 8]:
        mq, vq, mp, vp = gaussian_sensor(.9 + .1j, db)
        onp.testing.assert_allclose([mq, mp], onp.sqrt(2) * onp.array([.9, .1]), atol=1e-12)
        onp.testing.assert_allclose([vq, vp], 10 ** (-db / 10), atol=1e-12)
    latent, observed, nu = displacement_samples(100000, 5, seed=73)
    onp.testing.assert_array_equal(displacement_samples(100000, 5, seed=73)[1], observed)
    onp.testing.assert_allclose([onp.var((observed - latent).real), onp.var((observed - latent).imag)],
                                nu / 2, rtol=.02)
    onp.testing.assert_allclose(characteristic_estimate(observed, 0, nu), 1, atol=1e-12)
    b = onp.array([.3, .7, 1.2])
    assert onp.max(onp.abs(characteristic_estimate(observed, 1j * b, nu) - characteristic_truth(b))) < .015
    assert onp.max(onp.abs(characteristic_estimate(latent, 1j * b, 0) - characteristic_truth(b))) < .015
    for query in [.5, 1, 1.5]:
        assert rms_error(nu, query, 2000) < rms_error(1, query, 2000)
        assert sample_ratio(rms_error(1, query, 2000), rms_error(nu, query, 2000)) > 1
    # One mode: the approximation is within a factor 1.3 of the exact ratio at b = 1.5; modes multiply.
    exact = sample_ratio(rms_error(1, 1.5, 2000), rms_error(nu, 1.5, 2000))
    assert 1 < exact / many_mode_ratio(nu, 1.5, 1) < 1.3
    onp.testing.assert_allclose(many_mode_ratio(nu, 1.5, 3), many_mode_ratio(nu, 1.5, 1) ** 3)
    # PennyLane's x is 2X, and its wire-0 reading is (x_p - x_m)/sqrt2, so its variance is 2 * Var(X_p - X_m).
    for db in [0, 5, 8]:
        _, pennylane_variance, _, _ = gaussian_sensor(0j, db)
        onp.testing.assert_allclose(2 * quadrature_variances(db)["bell"], pennylane_variance, atol=1e-12)
    onp.testing.assert_allclose(quadrature_variances(0)["bell"], quadrature_variances(0)["heterodyne"],
                                atol=1e-12)
    return time.perf_counter() - started


if __name__ == "__main__":
    elapsed = self_check()
    print("PASS: Gaussian units, Bell readouts, sampling law, Fourier estimator, RMS comparison, variances")
    print(f"PennyLane {qml.__version__}; NumPy {onp.__version__}")
    print(f"Self-check time, excluding imports: {elapsed:.3f} s")

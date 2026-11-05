### 2. Estimate the characteristic function

Take $\beta=ib$, as in "The question".
The estimator replaces each unknown $\alpha$ with its sample $\zeta_k$:
$$\hat\lambda(ib)=e^{\nu b^2}\,\frac1N\sum_{k=1}^{N}e^{2ib\operatorname{Re}\zeta_k}.$$
The noise biases the plain mean. Because $\eta$ is Gaussian and independent of $\alpha$,
$$\mathbb{E}\left[e^{2ib\operatorname{Re}\zeta}\right]=\lambda(ib)\,\mathbb{E}\left[e^{2ib\operatorname{Re}\eta}\right]=\lambda(ib)\,e^{-\nu b^2}.$$
The prefactor $e^{\nu b^2}$ removes this bias, so $\mathbb{E}[\hat\lambda(ib)]=\lambda(ib)$: the estimator is unbiased.
This is the paper's Eq. S9, for one mode.
`characteristic_estimate` computes it for any $\beta$, from the samples and $\nu$ only.

The prefactor also scales the statistical error.
We measure it by the RMS error: the square root of the mean squared error over repeated experiments.
Each term in the sum has modulus 1, so for large $b$ the RMS error is about $e^{\nu b^2}/\sqrt N$.
At $b=1.5$, $e^{\nu b^2}$ is 9.5 at 0 dB and 2.0 at 5 dB.
Squeezing lowers $\nu$, and with it this factor.

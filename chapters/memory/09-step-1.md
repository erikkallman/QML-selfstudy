### 1. Simulate one use and draw samples

`gaussian_sensor`, in `research_memory.py`, builds the circuit of "The idea".
Wire 0 is the probe and wire 1 is the memory.
Its inputs are the displacement `alpha` and the squeezing in dB.
It returns the mean and variance of $X$ on wire 0 and of $P$ on wire 1.

PennyLane's Gaussian simulator uses the convention $\hbar=2$, in which its quadrature $x$ equals $2X$ in the units of this chapter.
Its two readings therefore have means $\sqrt2\operatorname{Re}\alpha$ and $\sqrt2\operatorname{Im}\alpha$.
Divided by $\sqrt2$, they give $\zeta$ in the units of $\alpha$, and their variances are divided by 2: `vx / 2` in the code.

The simulator returns means and variances.
`displacement_samples` therefore draws each sample from the normal distribution with those moments.
Each part of the noise $\eta$ has variance $\nu/2$, where $\nu=e^{-2r}=10^{-s/10}$ is the noise power:
1 at 0 dB and 0.32 at 5 dB.
The function also draws the displacements of the chapter's device,
$$\alpha=c+0.12\,(g_1+i\,g_2),$$
where $c$ is $-0.9$ or $+0.9$ with probability 1/2 each, and $g_1$, $g_2$ are independent standard normal variables.

The code generates each $\alpha$, so the code knows it.
`characteristic_estimate` (step 2) never receives $\alpha$. Its inputs are the samples $\zeta$ and $\nu$.

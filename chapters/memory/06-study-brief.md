### The study, in brief

Liu et al. built the scheme with a memory in an optical experiment
([Science, 2025](https://preskill.caltech.edu/pubs/preskill-2025-quantum-learning.pdf);
[arXiv full text](https://arxiv.org/html/2502.07770v2)).
Their device displaces $n$ modes at once, with a joint distribution $p(\alpha)$ on $\mathbb{C}^n$. The team ran two tasks.

- Task 1 learned the characteristic function of a 100-mode device.
  With 4.8 dB of squeezing, they needed about $10^7$ samples (estimated from their data).
  Without squeezing, an extrapolation from smaller devices gives about $7.3\times10^{18}$: 11.8 orders of magnitude more.
  The paper states that this comparison proves no advantage.
  A scheme that knows the family of devices in advance could need fewer samples.
- Task 2 removed that prior knowledge with a hypothesis test.
  A referee chose one of two families of devices, and revealed the query only after all measurements.
  With 120 modes and $10^5$ samples:
  - Proven: every scheme without a memory identifies the family with probability at most $0.5+3.8\times10^{-11}$.
    Random guessing gives 0.5.
  - Measured: the scheme with a memory reached $0.563\pm0.025$, above the bound with 99.3% confidence.
  - Estimated: a scheme without a memory would need about $1.6\times10^{14}$ samples to reach 0.563,
    9.2 orders of magnitude more than $10^5$.

The Study tab gives the two families, the order of each round, and the optical setup.

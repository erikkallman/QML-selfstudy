### 4. From one mode to many

With one mode, the gain from squeezing is a constant factor. The study's devices have $n$ modes.
A query is then a vector $\beta=(\beta_1,\dots,\beta_n)$ with one entry per mode, and the prefactor becomes
$$e^{\nu\lvert\beta\rvert^2}=\prod_{j=1}^{n}e^{\nu\lvert\beta_j\rvert^2},$$
one factor per mode.
If every entry has modulus $b$, the number of samples needed grows about as $e^{2\nu nb^2}$.
The ratio between 0 dB and the chosen squeezing is then about $e^{2(1-\nu)nb^2}$.
Each added mode multiplies it by about $e^{2(1-\nu)b^2}$: 22 at 5 dB and $b=1.5$.
So the gain grows exponentially with $n$.
For Task 2, the paper proves more: every scheme without a memory needs a number of samples that grows exponentially with $n$.

### The two tasks

#### Task 1: how the numbers were found

The team determined the sample complexity by Monte Carlo resampling of their measured data.
At 4.8 dB of squeezing, they estimate about $10^7$ samples for the 100-mode device.
Without squeezing ($r=0$, the scheme without a memory), they measured only smaller numbers of modes.
An exponential fit to those results, extrapolated to 100 modes, gives about $7.3\times10^{18}$ samples.

The authors' lower bound for schemes without a memory (Theorem 3) applies to learning every process in a broad class.
A scheme that uses prior knowledge of the specific family could need fewer samples.
So Task 1 alone proves no advantage, as the paper states.

#### Task 2: the two families

- Family A: $p_A(\alpha)$ is a Gaussian distribution, with characteristic function $\lambda_A(\beta)=e^{-\lvert\beta\rvert^2/2\sigma_A^2}$.
  It is the Gaussian device of "The question", with standard deviation $\sigma=1/(2\sigma_A)$ in each part of each mode.
- Family B: $p_B(\alpha)=p_A(\alpha)\left[1\pm4\epsilon_0\sin\!\left(2\operatorname{Im}(\alpha^\dagger\gamma)\right)\right]$ with $0<\epsilon_0\leq1/4$.
  This is $p_A$ modulated by a sinusoid whose wave vector is set by $\gamma\in\mathbb{C}^n$.
  Its characteristic function has two additional peaks, at $\beta=\gamma$ and $\beta=-\gamma$.
  The paper calls B the three-peak family.

#### Task 2: one round

1. A referee chooses family A or B and samples $\gamma$ from a normal distribution.
2. The team sends $N=10^5$ probes through the process and measures all of them.
3. The referee reveals $\gamma$, but not the family.
4. The team evaluates its estimate $\hat\lambda(\gamma)$ and compares it with a threshold.
   In the noiseless limit, $\lambda_A(\gamma)\approx0$ and $\lvert\lambda_B(\gamma)\rvert\approx2\epsilon_0$.

Because $\gamma$ is revealed only after the measurements, the measurement cannot be designed for the one frequency $\beta=\gamma$.
It must support an estimate of $\lambda(\beta)$ at any $\beta$ the referee could reveal.
This is the order of a learning task, as the timeline in "The question" shows.
With $\gamma$ known in advance, the task would be the estimation of one known parameter, a problem of quantum metrology.
The late query is also what lets the authors' lower bound cover every scheme without a memory.
The results are in "The study, in brief".

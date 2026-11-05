### The idea

#### Learning schemes and measurements

A learning scheme is the whole procedure: what to prepare, what to measure, and how to compute the answers.
The information about $\alpha$ is in the output state of each use, and a scheme must measure that state.
A measurement turns a quantum state into a number. Afterwards only the number remains.
$X$ and $P$ do not commute, so one measurement cannot determine both exactly on the same state.
Two choices therefore decide what a scheme can learn: when it measures, and which systems one measurement acts on.

For the purposes of the study here, a distinction can be made in how different schemes store information:

- A scheme without a quantum memory measures each output as soon as the device produces it, and keeps only the outcome.
  Each measurement acts on one output alone. Earlier outcomes may choose the next measurement >what does this even mean? What did i mean to say here?<.
- A scheme with a quantum memory keeps quantum systems unmeasured for a while,
  as a computer's memory keeps data between two steps of a program.
  Later, one measurement can act on several systems together.
  This is a joint measurement. Learning theory also calls it an entangled measurement.

#### Without a memory: one mode per use

The standard scheme sends one mode through the device at each use, the probe, prepared in the vacuum state.
It then measures $X$ and $P$ of the probe at once, by heterodyne detection:
a 50:50 beamsplitter splits the probe, and homodyne detection measures $X$ on one output and $P$ on the other.
The beamsplitter's second input port admits a mode in the vacuum state, which adds another $1/4$ to each reading.
This added noise is the cost of measuring two non-commuting quadratures at once.
Each sample therefore has noise variance $1/2$ in its real part and $1/2$ in its imaginary part:
$1/4$ from the vacuum noise of the probe and $1/4$ from the second input port.

#### A known query needs no memory

Suppose the learner knew the query in advance, for example $\beta=ib$, which needs only the $X$ part of each displacement.
It could squeeze the probe in $X$ and measure $X$ alone by homodyne detection, with noise variance $e^{-2r}/4$: 0.079 at 5 dB.
That is less noise than the memory scheme below gives, with one mode only.
But these samples cannot answer a query along any other direction.

#### A late query needs every direction

In the learning task, the query arrives after the samples are recorded, so each sample must serve every direction.
A complex sample $\zeta$ gives a value of the wave $e^{\zeta^*\beta-\beta^*\zeta}$ for every $\beta$; a sample of $X$ alone only for imaginary $\beta$.
With one mode, the uncertainty relation forbids low noise in $X$ and $P$ together.
The standard one-mode scheme that covers every direction is heterodyne detection, with noise variance $1/2$ in each part.

#### With a memory: two modes per use

The quantum memory in this case is a second mode, the memory (m), next to the probe (p).
Two modes have observables that neither mode has alone >this needs more elaboration, why do they commute? explain further<:
$X_\text{p}-X_\text{m}$ and $P_\text{p}+P_\text{m}$ commute, although $X$ and $P$ of each mode do not.
So one joint measurement can determine both combinations exactly, and both variances can be small at once.
Separate measurements cannot: measuring $X_\text{p}$ and $X_\text{m}$ gives $X_\text{p}-X_\text{m}$, but loses $P_\text{p}+P_\text{m}$.

Two-mode squeezing with parameter $r$ prepares the probe and the memory in the two-mode squeezed vacuum, where
$$\operatorname{Var}(X_\text{p}-X_\text{m})=\operatorname{Var}(P_\text{p}+P_\text{m})=e^{-2r}/2.$$
For two modes in the vacuum state, both variances are $1/2$.
The two-mode squeezed vacuum is entangled. >is "r" above defined prior ? If not i need to make it clear in this expression<
Each of its modes on its own has variance $\cosh(2r)/4$, above the vacuum value: 0.43 at 5 dB.

Only the probe passes through the device. The memory is stored, unmeasured, until the probe returns >returns where? this is vague<.
A joint measurement of both modes, the Bell measurement, then determines $X_\text{p}-X_\text{m}$ and $P_\text{p}+P_\text{m}$.
The displacement adds $\operatorname{Re}\alpha$ and $\operatorname{Im}\alpha$ to them, so each sample is
$$\zeta=(X_\text{p}-X_\text{m})+i\,(P_\text{p}+P_\text{m})=\alpha+\eta.$$
The noise $\eta$ has variance $e^{-2r}/2$ in each part: 0.16 at 5 dB, against $1/2$ without a memory.
If the memory were measured before the probe returned, only an outcome would remain,
and the scheme would belong to the class without a quantum memory.

#### The two schemes side by side

To provide a simple overview of the differences, and to repeat the differences here:

| Step | Without a quantum memory | With a quantum memory |
|:---|:---|:---|
| Prepare | The probe alone, in the vacuum state | The probe and the memory, in the two-mode squeezed vacuum |
| Use the device | The probe passes through it | The probe passes through it; the memory is stored, unmeasured |
| Measure | The probe alone, by heterodyne detection | The probe and the memory together, by the Bell measurement |
| Noise per part of a sample | $1/2$ | $e^{-2r}/2$, which is 0.16 at 5 dB |

Both schemes keep only numbers and use the same estimator (step 2); only the measurement differs.
At 0 dB ($r=0$) the memory is an independent mode in the vacuum state.
It then plays the role of the vacuum at the second input port of heterodyne detection,
and the scheme with a memory becomes the scheme without one.

So the memory helps only when the query arrives after the samples.
For a query known in advance, one squeezed mode measured by homodyne detection does better.>this can be better described<

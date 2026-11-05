### The question

#### The unknown device

An optical device applies a random displacement $\alpha$ to every mode that passes through it.
At each use, $\alpha$ is a new, independent draw from the same distribution $p(\alpha)$.
The paper calls such a device a random displacement process.
The distribution $p(\alpha)$ describes the device's noise. It is the unknown object to learn.

The displacement is not observed directly.
Each use gives one sample $\zeta$: a measurement result equal to $\alpha$ plus measurement noise.

#### Samples first, queries later

The task has two phases, as training and testing have in machine learning:

1. Use the device $N$ times and record the $N$ samples.
2. Afterwards, answer queries.

A query is a complex number $\beta$, with the request: estimate $\lambda(\beta)$, defined below.
The learner must answer from the stored samples alone once all measurements are completed.

A query plays the role of a test input: the learner must answer any $\beta$ in a given set.

The set is infinite, so the learner cannot design one measurement per query. One data set must serve them all. >these two paragraphs are unclear<

#### The characteristic function > this couuld use illustrations<

The answer to the query $\beta$ is the value of the characteristic function
$$\lambda(\beta)=\mathbb{E}_\alpha\left[e^{\alpha^*\beta-\beta^*\alpha}\right],$$
the Fourier transform of $p(\alpha)$ over phase space.
It determines $p(\alpha)$ uniquely, by Fourier inversion, so learning $\lambda$ means learning the device, which is the goal of the study.

To read the exponent, write $\alpha=a_1+ia_2$ and $\beta=b_1+ib_2$. Then
$$\alpha^*\beta-\beta^*\alpha=2i\,(b_2a_1-b_1a_2).$$
So $e^{\alpha^*\beta-\beta^*\alpha}$ is a plane wave in phase space.
It oscillates along the direction of $-i\beta$, which is $\beta$ rotated by $-90^\circ$, and it is constant along the direction of $\beta$.
One period spans a distance $\pi/\lvert\beta\rvert$ in $\alpha$.
So $\beta$ is a frequency in phase space, not the frequency $\omega$ of the light, which is an important distinction.

#### What a value of $\lambda(\beta)$ tells >all of these need be underlined<

The value $\lambda(\beta)$ is the mean of the wave over the displacements, so $\lvert\lambda(\beta)\rvert\le1$.

- If the displacements spread over much less than one period along $-i\beta$,
  the wave has nearly the same value at every $\alpha$, and $\lvert\lambda(\beta)\rvert$ is close to 1.
- If they spread over many periods, the values cancel in the mean, and $\lambda(\beta)$ is close to 0.

So a query with small $\lvert\beta\rvert$ asks about the coarse shape of $p(\alpha)$,
and a query with large $\lvert\beta\rvert$ asks about its fine structure. Three examples:

- A device that never displaces ($\alpha=0$) has $\lambda(\beta)=1$ for every $\beta$.
- A Gaussian device, whose real and imaginary parts are independent with standard deviation $\sigma$,
  has $\lambda(\beta)=e^{-2\sigma^2\lvert\beta\rvert^2}$. It falls to $e^{-2}=0.14$ at $\lvert\beta\rvert=1/\sigma$.
- The device of this chapter: two Gaussians of standard deviation 0.12, centred at $-0.9$ and $+0.9$ on the real axis.
  Take $\beta=ib$ with $b$ real. We call $b$ the query frequency.
  The wave then depends on $\operatorname{Re}\alpha$ alone, with period $\pi/b$, and
  $$\lambda(ib)=\cos(1.8b)\,e^{-2(0.12)^2b^2}.$$
  At $b=\pi/3.6=0.87$, the distance 1.8 between the centres is half a period.
  The two Gaussians then see opposite values of the wave, and $\lambda(ib)=0$.
  At $b=\pi/1.8=1.75$, the distance is one full period, and $\lambda(ib)=-0.92$.
  The oscillation in $b$ gives the distance between the centres; the slow decay gives their width.
  The Lab plots this function as a black curve.

#### Which part of a sample a query uses

Each query uses the displacements along one direction only.
For $\beta=ib$, $\lambda(ib)$ is the mean of $e^{2ib\operatorname{Re}\alpha}$, so it uses only the $X$ part of each displacement.
For real $\beta$, it uses only the $P$ part.
While the samples are recorded, the learner does not know which direction a later query will use.

#### Success and sample complexity

The learner succeeds if its estimate $\hat\lambda(\beta)$ is within $\epsilon$ of $\lambda(\beta)$ for every query in the set.
The sample complexity is the smallest $N$ that achieves this. It depends on how the samples are collected. > in what way? why?<

#### The task in machine-learning terms

| Machine-learning term | In this case |
|:---|:---|
| Unknown target | The distribution $p(\alpha)$ of the device's displacements |
| Training data | The $N$ samples $\zeta_1,\dots,\zeta_N$, recorded before any query is known |
| Learned model | The estimate $\hat\lambda(\beta)$, computed from the stored samples for any query $\beta$ |
| Test input | A query $\beta$, chosen after the samples are recorded |
| Test error | $\lvert\hat\lambda(\beta)-\lambda(\beta)\rvert$ |
| Sample complexity | The $N$ needed for test error at most $\epsilon$ on every query in the set |
| Where the quantum resource acts | In data collection: the measurement, with or without a quantum memory |

One difference from standard machine learning: the learner also chooses how the data are collected,
that is, which measurement each experiment performs.
The quantum advantage in this case comes entirely from that choice.

| Term | Meaning |
|:---|:---|
| Learning from quantum data | The branch of QML in which the unknown object is a quantum state or process, accessed through repeated experiments. Its theory is quantum learning theory. |
| Learner | The party that runs the experiments and then answers the queries. |
| Query | A complex number $\beta$, put to the learner after the samples are recorded, with the request to estimate $\lambda(\beta)$ from the stored samples. It plays the role of a test input. The paper uses this word (Theorem 3). |
| Sample complexity | The number of samples needed to answer every query in a set to accuracy $\epsilon$. |
| Learning scheme | The whole procedure: what to prepare, what to measure, and how to compute the answers. |
| Quantum memory | Storage of a quantum state, unmeasured, between two steps of an experiment, so that it can be measured jointly with later parts. Here, the memory mode. |
| Joint measurement | One measurement that acts on several systems together. Learning theory also calls it an entangled measurement. |
| Mode | One degree of freedom of the electromagnetic field, quantized as a harmonic oscillator with annihilation operator $a$. |
| Quadratures $X$, $P$ | The cosine and sine amplitudes of the mode's field. As observables, $X=(a+a^\dagger)/2$ and $P=(a-a^\dagger)/(2i)$, with $[X,P]=i/2$. |
| Phase space | The plane with axes $X$ and $P$. The direction at angle $\theta$ belongs to the quadrature $X\cos\theta+P\sin\theta$. |
| Homodyne detection | Measurement of one quadrature, $X\cos\theta+P\sin\theta$, of one mode, with a strong reference laser whose phase sets $\theta$. |
| Vacuum state | The state with zero photons. $\operatorname{Var}(X)=\operatorname{Var}(P)=1/4$. |
| Squeezing | Lowering the variance of one quadrature below $1/4$, while the other grows by the same factor. A single-mode squeezed vacuum has $\operatorname{Var}(X)=e^{-2r}/4$ and $\operatorname{Var}(P)=e^{2r}/4$. |
| Squeezing parameter $r$ | The number that sets the strength of squeezing; $r=0$ means no squeezing. |
| Squeezing in dB | $s=10\log_{10}e^{2r}$, so $e^{-2r}=10^{-s/10}$. |
| Effective squeezing | The squeezing that remains after optical losses. The Lab sets this value. |
| Displacement $\alpha$ | The operation that adds $\operatorname{Re}\alpha$ to $X$ and $\operatorname{Im}\alpha$ to $P$. Its operator is $D(\alpha)=e^{\alpha a^\dagger-\alpha^*a}$. |
| Random displacement process | The paper's name for the device: at each use, $\alpha$ is an independent random variable with distribution $p(\alpha)$. |
| Characteristic function $\lambda(\beta)$ | $\lambda(\beta)=\mathbb{E}_\alpha[e^{\alpha^*\beta-\beta^*\alpha}]$, the Fourier transform of $p(\alpha)$: the mean of a plane wave over the displacements. |
| Phase-space frequency $\beta$ | The variable of the Fourier transform. The wave $e^{\alpha^*\beta-\beta^*\alpha}$ oscillates along the direction of $-i\beta$, with period $\pi/\lvert\beta\rvert$. It is not the frequency $\omega$ of the light. |
| Query frequency $b$ | The real number in $\beta=ib$. The wave then has period $\pi/b$ in $\operatorname{Re}\alpha$. |
| Quantum metrology | The estimation of a parameter known in advance, with quantum resources such as squeezing. Here: the case of a query known before the measurements. |
| Probe | The mode that passes through the device; wire 0 in the circuit. |
| Memory | The mode stored outside the device and measured with the probe at the end; wire 1. |
| Heterodyne detection | Measurement of $X$ and $P$ of one mode at once: a 50:50 beamsplitter with vacuum at its second input port, then homodyne detection of $X$ on one output and $P$ on the other. Noise $1/2$ per part of a sample. |
| Two-mode squeezed vacuum | The entangled state with $\operatorname{Var}(X_\text{p}-X_\text{m})=\operatorname{Var}(P_\text{p}+P_\text{m})=e^{-2r}/2$. |
| Bell measurement | Joint measurement of the commuting observables $X_\text{p}-X_\text{m}$ and $P_\text{p}+P_\text{m}$: a 50:50 beamsplitter, then homodyne detection of $X$ on one output and $P$ on the other. |
| Sample $\zeta$ | The result of one use: $\zeta=(X_\text{p}-X_\text{m})+i(P_\text{p}+P_\text{m})=\alpha+\eta$. |
| Noise $\eta$, noise power $\nu$ | $\eta$ is the measurement noise of one sample. $\nu=e^{-2r}=10^{-s/10}$, and each part of $\eta$ has variance $\nu/2$. |
| Unbiased | Said of an estimator whose mean over repeated experiments equals the true value. |
| RMS error | Root-mean-square error: the square root of the mean squared error over repeated experiments. |

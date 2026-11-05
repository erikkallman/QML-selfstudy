### Background: one mode of light

This section elaborates on some of the basic concepts of the study to make everything more understandable as this chapter progresses.

#### Modes and quadratures

A mode is one degree of freedom of the electromagnetic field, for example one polarization in one time bin.
At a fixed place, the field of one mode oscillates at the light's frequency $\omega$, as the sum of a cosine part and a sine part:
$$E(t)\propto X\cos\omega t+P\sin\omega t.$$
The amplitudes $X$ and $P$ are the mode's quadratures.
The name refers to the quarter period, 90 degrees, between cosine and sine.
In quantum mechanics, $X$ and $P$ are observables: $X=(a+a^\dagger)/2$ and $P=(a-a^\dagger)/(2i)$,
where $a$ is the mode's annihilation operator.
They do not commute: $[X,P]=i/2$. They play the roles of position and momentum of a harmonic oscillator.

#### Phase space and homodyne detection

The plane with axes $X$ and $P$ is the mode's phase space.
The direction at angle $\theta$ belongs to the quadrature $X\cos\theta+P\sin\theta$.
Homodyne detection measures one quadrature: it mixes the light with a strong reference laser, whose phase sets $\theta$.

#### Vacuum noise and squeezing

The vacuum state is the state with zero photons. In it, $\operatorname{Var}(X)=\operatorname{Var}(P)=1/4$.
Their product is then $1/16$, the minimum that the uncertainty relation $\operatorname{Var}(X)\operatorname{Var}(P)\geq1/16$ allows.
So one mode cannot have both variances below $1/4$.

Squeezing lowers the variance of one quadrature and raises the variance of the other by the same factor.
A single-mode squeezed vacuum with squeezing parameter $r$ has
$\operatorname{Var}(X)=e^{-2r}/4$ and $\operatorname{Var}(P)=e^{2r}/4$.
Squeezing is quoted in decibels, $s=10\log_{10}e^{2r}$,
so the squeezed variance falls by the factor $e^{-2r}=10^{-s/10}$: 0.32 at 5 dB.
Row 1 of the noise figure under "The idea" shows both states.

#### Displacements

A displacement by a complex number $\alpha$ adds a classical field of fixed amplitude to the mode.
It adds $\operatorname{Re}\alpha$ to $X$ and $\operatorname{Im}\alpha$ to $P$, so it moves the state by $\alpha$ in phase space.
Its operator is $D(\alpha)=e^{\alpha a^\dagger-\alpha^*a}$, which shifts the annihilation operator: $D(\alpha)^\dagger aD(\alpha)=a+\alpha$.

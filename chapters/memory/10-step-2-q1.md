Show that one term of the sum, with the prefactor, has variance $e^{2\nu b^2}-\lvert\lambda(ib)\rvert^2$. What RMS error follows for $N$ samples?

Let $T=e^{\nu b^2}e^{2ib\operatorname{Re}\zeta}$. Its modulus is $e^{\nu b^2}$, so $\mathbb{E}\lvert T\rvert^2=e^{2\nu b^2}$, and its mean is $\lambda(ib)$. Its variance is $\mathbb{E}\lvert T\rvert^2-\lvert\mathbb{E}T\rvert^2=e^{2\nu b^2}-\lvert\lambda(ib)\rvert^2$. The $N$ terms are independent, so their mean has variance $(e^{2\nu b^2}-\lvert\lambda(ib)\rvert^2)/N$. The RMS error is its square root. `rms_error` in step 3 computes this.

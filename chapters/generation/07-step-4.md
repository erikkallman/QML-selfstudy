### 4. Compute each angle from a bit mean

For each qubit $j$, take the $n_j$ training pairs whose input isolates it.
Compute the mean of its output bit over these pairs. Call it $\bar y_j$.
Solve $\bar y_j=\sin^2\beta_j$ for the angle:
$$\hat\beta_j=\tfrac12\arccos(1-2\bar y_j).$$
For example, $\bar y_j=1/2$ gives $\hat\beta_j=\pi/4$.
This is the paper's Eq. (S.2.1).
The paper's Definition 16 writes the rotation as $R_Z(\theta)=e^{-i\theta Z/2}$, so its $\theta$ equals our $2\beta$.

Inserting the six estimates into the circuit completes the training.
There is no loss function, no gradient, and no repeated update.
If no training pair isolates a qubit, `fit_local` stops with an error that names the qubit.

$\bar y_j$ has variance $\sin^2\beta_j\cos^2\beta_j/n_j$, and $d\hat\beta_j/d\bar y_j=1/(2\sin\beta_j\cos\beta_j)$.
By the delta method, each fitted angle therefore has standard error $1/(2\sqrt{n_j})$, independent of $\beta_j$.
The approximation fails for angles close to 0 or $\pi/2$, where that derivative diverges.
At 12,000 training pairs, 565 pairs isolate qubit 1, so its standard error is about 0.021 radians.
The largest error over the six angles is 0.023 radians.

Now the angle restriction. $\sin^2\beta$ has the same value for $\beta$ and $-\beta$,
so a bit mean cannot distinguish the two signs.
The two signs can still give different distributions of whole bitstrings.
Flipping the sign of $\beta_0$ alone changes the distribution at $x=000000$ by a TVD of 0.28.
Restricting every angle to $0\le\beta_j\le\pi/2$ makes the answer unique.

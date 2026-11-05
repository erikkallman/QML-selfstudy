### 3. Isolate one qubit

Look at qubit 1. Its neighbors are qubits 0, 2, and 4.
Pick the training pairs where $x_1=0$ and $x_0=x_2=x_4=1$.
Qubit 1 then starts in $\lvert+\rangle$ and all its neighbors start in $\lvert0\rangle$.
We say that this input isolates qubit 1.

The neighbors remain in $\lvert0\rangle$ up to a phase >up to a phase? means what here?<, so every CZ gate on qubit 1 acts as the identity.
Qubit 1 is then acted on by three gates only: Hadamard, $R_Z(2\beta_1)$, Hadamard.
Its output bit follows
$$P(y_1=1)=\sin^2\beta_1.$$
No other angle enters this probability.

Training needs, for every qubit, training pairs whose input isolates it.
The paper calls an input distribution with this property locally decoupling.
Our mixture has it. A qubit with $d$ neighbors is isolated by a fraction
$\tfrac13\left(0.6\cdot0.4^d+0.2\cdot0.8^d\right)$ of the training pairs:
7.5% for the qubits with two neighbors (0, 2, 3, 5) and 4.7% for the qubits with three (1, 4).
The all-zero third of the mixture isolates no qubit.
`local_event_mask` finds, for every qubit, the training pairs whose input isolates it. It reads only the inputs, never the angles.

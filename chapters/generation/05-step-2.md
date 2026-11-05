### 2. Read the circuit layer by layer

The drawing below shows the target circuit for input $x=000000$.
It has the four layers from the introduction. Read it from left to right.

1. Prepare: input bit $x_j=0$ applies a Hadamard gate, which prepares qubit $j$ in $\lvert+\rangle$.
   Input bit $x_j=1$ leaves the qubit in $\lvert0\rangle$.
2. Rotate: $R_Z(2\beta_j)=e^{-i\beta_jZ}$ multiplies $\lvert0\rangle$ by $e^{-i\beta_j}$ and $\lvert1\rangle$ by $e^{i\beta_j}$.
   The drawing shows the value $2\beta_j$ in each $R_Z$ box.
3. Entangle: a CZ gate acts on each of the 7 edges of the grid.
   A CZ gate acts as the identity when either of its qubits is in $\lvert0\rangle$.
4. Measure: a Hadamard on every qubit, then a computational-basis measurement.
   Together they measure in the $X$ basis, which maps the relative phase between $\lvert0\rangle$ and $\lvert1\rangle$ onto the outcome probabilities.

We restrict every angle to $0\le\beta_j\le\pi/2$. Step 4 explains why.

The graph under the drawing shows which qubits share a CZ gate.
It highlights qubit 1 and its three neighbors.

### The question

A generative model is a parametrized probability distribution that is fitted to training samples
and can then produce new samples. A language model is an example: it fits a distribution over word sequences.

A quantum circuit defines such a distribution.
Each run ends with a computational-basis measurement of every qubit, which gives a bitstring $y$ such as `010011`.
By the Born rule, a circuit that prepares the state $\lvert\psi\rangle$ gives $y$ with probability $\lvert\langle y\vert\psi\rangle\rvert^2$.
If the gate angles are parameters, the circuit is a generative model:
training fits the angles, and each run produces one sample.

Two known results make a useful quantum generative model hard to obtain.

- For some circuit families, no known classical algorithm produces samples with the circuit's probabilities
  in a time that grows only polynomially with the number of qubits.
  Complexity theory gives reasons to expect that no such algorithm exists.
- Training large circuits by gradient descent can fail.
  The variance of the loss gradient can decrease exponentially with the number of qubits (barren plateaus),
  or the loss can have many suboptimal local minima.

The study asks: is there a circuit family that a classical computer can train efficiently from data,
but whose samples a classical computer cannot produce efficiently?

### The idea

The study uses a circuit of constant depth on a grid of qubits, with four layers:

1. Input bit $x_j$ sets the initial state of qubit $j$: $x_j=0$ gives $\lvert+\rangle$, $x_j=1$ gives $\lvert0\rangle$.
2. Each qubit $j$ undergoes the rotation $R_Z(2\beta_j)$. The angles $\beta_j$ are the model's parameters.
3. A CZ gate acts on every edge of the grid. CZ gates entangle neighboring qubits that start in $\lvert+\rangle$.
4. Every qubit is measured in the $X$ basis.

A CZ gate acts as the identity if either of its qubits is in $\lvert0\rangle$.
So if $x_j=0$ and $x_k=1$ for every neighbor $k$ of qubit $j$, the output bit $y_j$ depends only on $\beta_j$:
$P(y_j=1)=\sin^2\beta_j$.
The mean of $y_j$ over the training pairs with this input pattern then determines $\beta_j$ (step 4).
No gradient descent is needed.

With input $x=000000$, every qubit starts in $\lvert+\rangle$ and every CZ gate entangles its two qubits.
The output bits are then correlated across the whole grid.
For large grids, this is the case that the study argues a classical computer cannot sample efficiently.
The diagram shows the training steps.

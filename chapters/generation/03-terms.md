| Term | Meaning |
|:---|:---|
| Generative model | A parametrized probability distribution, fitted to training samples, from which new samples can be drawn. |
| Bitstring | A sequence of bits, such as `010011`. Six qubits give $2^6=64$ possible bitstrings. |
| Conditional distribution $p(y\mid x)$ | The probability of output bitstring $y$, given input bitstring $x$. |
| Training pair $(x,y)$ | One input bitstring and the output bitstring that the target circuit produced for it. |
| Target circuit | The circuit with chosen angles that produced the training pairs. |
| Fitted circuit | The same circuit with the angles that we estimate. |
| Sample | One bitstring from one run of a circuit. |
| Training | Estimating the angles from training pairs. The paper calls this "learning". |
| Generation | Running the fitted circuit to produce new samples. The paper calls this "inference". |
| Graph | The fixed set of qubit pairs (edges) that receive a CZ gate. Our grid has 7 edges. |
| Neighbors | The qubits that share an edge with a given qubit. |
| CZ gate | The two-qubit gate $\operatorname{diag}(1,1,1,-1)$: it multiplies the $\lvert11\rangle$ component by $-1$. It entangles two qubits that start in $\lvert+\rangle$, and acts as the identity when either qubit is in $\lvert0\rangle$. |
| Angle $\beta_j$ | The adjustable parameter of qubit $j$. The code applies the phase rotation $R_Z(2\beta_j)=e^{-i\beta_jZ}$. |
| $X$-basis measurement | A Hadamard gate followed by a computational-basis measurement. It maps the relative phase between $\lvert0\rangle$ and $\lvert1\rangle$ onto the outcome probabilities. |
| Initial state | Input bit $x_j=0$ prepares qubit $j$ in $\lvert+\rangle$; input bit $x_j=1$ leaves it in $\lvert0\rangle$, so its CZ gates act as the identity. |
| Isolated qubit | Qubit $j$ is isolated by input $x$ if $x_j=0$ and $x_k=1$ for every neighbor $k$. |
| Local decoupling | The paper's name for a property of the input distribution: every qubit is isolated with probability at least inverse-polynomial in the number of qubits. The training rule needs this property. |
| Barren plateau | A loss landscape in which the variance of the gradient decreases exponentially with the number of qubits, so gradient descent makes no progress. |
| IDQNN | Instantaneously deep quantum neural network: the paper's name for its constant-depth circuit family (Definition 16). |
| Shallow qubit | One qubit of the IDQNN. On hardware, it corresponds to one physical qubit at one time step of a deep circuit. |
| Linear XEB | Linear cross-entropy benchmark: $F_\text{XEB}=2^n\,\overline{p_\text{ideal}(y)}-1$, with the mean taken over the samples. 0 for uniformly random bitstrings; about 1 for ideal samples of a random circuit. |
| Clifford circuit | A circuit of Clifford gates; here H, CZ, and $R_Z$ with angles that are multiples of $\pi/2$. By the Gottesman-Knill theorem, a classical computer simulates it efficiently. |
| Total variation distance (TVD) | Half the sum of the absolute differences between two distributions. 0 means they are identical. |
| Negative log-likelihood (NLL) | The average of $-\log p(y\mid x)$ over test pairs, in nats. Lower is better. |
| Hard to sample classically | Proven in the paper for exact samples: no classical algorithm with polynomial running time produces them, unless the non-uniform polynomial hierarchy collapses. For approximate samples, the claim rests on further conjectures. At a fixed size, it is an estimate of the classical computing cost. |

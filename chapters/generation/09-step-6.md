### 6. Try one change at a time in the Lab

- Set the training pairs to 2,000, then to 20,000.
  The number of isolating pairs per qubit rises from about 90–170 to about 930–1,520.
  The largest angle error falls from 0.055 to 0.016 radians, and the TVD at 000000 from 0.055 to 0.010.
- Keep the training pairs fixed and raise the number of generated samples.
  The dots settle onto the fitted curve. The angles do not change.
- Choose a qubit and the input "Isolate selected qubit".
  That qubit's output bit is then 1 with probability $\sin^2\hat\beta_j$, independent of the other qubits.
- Choose the input "All one". Every qubit starts in $\lvert0\rangle$, so every CZ gate acts as the identity,
  and the final Hadamards give each bit probability 1/2: all 64 bitstrings have probability $1/64$.
  The output distribution then does not depend on the angles.

What the chapter shows: when the circuit's graph is known, single-bit means determine its angles, although its output bits are correlated.
What it does not show: a quantum advantage. Six qubits are easy to simulate, and we compare with no classical generative model.

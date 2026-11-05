Why does an input of 1 on each neighbor isolate qubit 1?

An input of 1 leaves that neighbor in $\lvert0\rangle$, and its rotation only multiplies $\lvert0\rangle$ by a phase factor, which changes no probability. A CZ gate multiplies the $\lvert11\rangle$ component of the two-qubit state by $-1$ and leaves the other components unchanged. With one qubit in $\lvert0\rangle$, the $\lvert11\rangle$ component has zero amplitude, so the gate acts as the identity. Qubit 1's output then depends on its own angle only.

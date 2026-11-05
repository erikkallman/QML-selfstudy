### 1. Know what the generator must reproduce

Our code builds the training data from a target circuit with six chosen angles,
`TARGET_BETA` $=[0.24, 0.51, 0.73, 0.92, 1.17, 1.36]$ radians.
Each training pair holds an input bitstring $x$ and an output bitstring $y$, with six bits each.
The same input gives different outputs on different runs.
For a fixed input, the probabilities of the outputs form the conditional distribution $p(y\mid x)$.

Our goal: find angles for a second circuit, the fitted circuit, so that it has the same distribution for every input.

The fitted circuit must reproduce the joint distribution of the six output bits,
not only the six marginal distributions. Two bits give an example:

- $P(00)=P(11)=1/2$. The two bits are always equal.
- $P(01)=P(10)=1/2$. The two bits are always different.

Both distributions have the same marginals, $P(y_1=1)=P(y_2=1)=1/2$, but different joint distributions.

Six output bits allow $2^6=64$ bitstrings.
`conditional_probabilities` computes all 64 probabilities exactly.
We use it only to score results. The training step never calls it.

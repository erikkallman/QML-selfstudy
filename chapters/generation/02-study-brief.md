### The study, in brief

Huang et al., Google Quantum AI, arXiv preprint, September 2025 ([full text](https://arxiv.org/html/2509.09033v1)).
The authors call their circuits instantaneously deep quantum neural networks (IDQNNs): the four layers of "The idea", on a grid.
Their results, labelled by kind:

- Measured: a Google superconducting processor ran the circuit with up to 816 shallow qubits,
  as 68 physical qubits over 12 time steps, at input $000\ldots0$ only.
  A score called linear XEB compared its samples with the ideal circuit.
  The authors do not yet expect 816 shallow qubits to be beyond classical simulation.
- Simulated: classical generative models, transformers and XGBoost, were trained on the same data.
  As the circuits grew, their XEB fell much faster than the hardware's.
- Inferred, not run: a beyond-classical estimate at 34,304 shallow qubits.
  It compares a proxy for the circuit's XEB, taken from an earlier experiment,
  with the best XEB that the Frontier supercomputer could reach with $10^{30}$ operations.
- Proven, under an assumption: a classical algorithm that samples these circuits exactly, in polynomial time,
  would make the polynomial hierarchy, a sequence of complexity classes, collapse.
  Complexity theorists consider that unlikely. For samples that are only approximately right,
  the claim rests on further conjectures.

The Study tab gives each result in detail.

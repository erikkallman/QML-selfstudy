### Where this case sits in QML

Quantum machine learning has two branches.

- Quantum models for classical data: a circuit with trainable parameters is fitted to classical data.
  The earlier chapters cover this branch.
- Learning from quantum data, the subject of quantum learning theory: the unknown object is itself quantum, a state or a process.
  A learner accesses it through repeated experiments.
  Afterwards it receives questions about the object, called queries, and must answer each one to an accuracy $\epsilon$.
  The number of experiments it needs is the sample complexity.

This case belongs to the second branch.
Its quantum resource is a quantum memory: the storage of a quantum state, unmeasured, between two steps of an experiment.

In this branch, some advantages are proven without assumptions from complexity theory.
For several tasks, a learner with a quantum memory needs exponentially fewer experiments, in the size of the system,
than any learner without one ([Chen, Cotler, Huang, and Li, 2021](https://arxiv.org/abs/2111.05881)).
An experiment on up to 40 superconducting qubits showed such an advantage
([Huang et al., Science, 2022](https://arxiv.org/abs/2112.00778)).
For quantum models on classical data, known advantages rest on such assumptions
(for example, that certain circuits are hard to simulate classically) or remain unproven.

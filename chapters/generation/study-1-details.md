Huang et al., Google Quantum AI, arXiv preprint, September 2025:
[full text](https://arxiv.org/html/2509.09033v1); the appendices cited below are in the
[PDF](https://arxiv.org/pdf/2509.09033v1).

#### Definition

The paper defines generative quantum advantage (Definition 2):
a quantum computer learns to generate the desired outputs substantially better than any classical computer.
"Better" means fewer training samples, higher accuracy, faster learning or generation,
or outputs that a classical computer cannot practically produce.
The definition covers both learning from data and generating new samples.

#### Model

The authors call their circuits instantaneously deep quantum neural networks (IDQNNs; Definition 16).
An IDQNN has exactly the four layers of "The idea" in the Tutorial tab, so its depth is constant in the number of qubits.
The paper proves (Lemma 2) that sampling an IDQNN gives the same output distribution as running a deep circuit on fewer qubits.
In that mapping, one direction of the grid is time.
Each shallow qubit of the IDQNN corresponds to one physical qubit at one time step of the deep circuit.
An input bit of 0 corresponds to a gate that carries the qubit's state to the next time step.
An input bit of 1 corresponds to a mid-circuit measurement and reset of that physical qubit.

#### Training, on a classical computer

Each angle is computed from the mean of one output bit,
with the formula $\hat\beta_j=\tfrac12\arccos(1-2\bar y_j)$ (Eq. S.2.1, Appendix C.2.a).
The training data come from the same circuit family, with angles that the authors chose.
The training inputs are a mixture: one third all zeros,
one third with each bit 1 with probability 0.4, and one third with probability 0.8.
For the hardware runs, the team learned each angle set from 200,000 training pairs.
In simulations of larger circuits, about $10^6$ training pairs brought the gate errors of the learned model below $10^{-3}$,
the best two-qubit gate error of current hardware (Fig. 2c).

#### Hardware run (measured)

A Google superconducting processor ran the deep form of the circuit:
up to 68 physical qubits over 12 time steps, which equals $68\times12=816$ shallow qubits.
To avoid mid-circuit measurements, the team ran only the input $x=000\ldots0$.
The paper states that the more input bits are 0, the harder classical sampling becomes, and that this input is the hardest.
The score is the linear cross-entropy benchmark of $N$ samples $y_1,\dots,y_N$ from an $n$-qubit circuit:
$$F_\text{XEB}=\frac{2^n}{N}\sum_{k=1}^{N}p_\text{ideal}(y_k)-1,$$
where $p_\text{ideal}$ is the noiseless circuit's output distribution.
Uniformly random bitstrings give $F_\text{XEB}=0$. For random circuits, ideal samples give $F_\text{XEB}\approx1$.
At sizes where $p_\text{ideal}$ is too costly to compute, the team also ran Clifford versions of the circuits,
with each $2\beta_j$ rounded to a multiple of $\pi/2$.
By the Gottesman-Knill theorem, a classical computer computes the ideal probability of any bitstring of such a circuit efficiently.
At sizes where both scores are available, the paper reports close agreement between the Clifford XEB and the XEB of the original circuits.

#### Classical models (simulated)

Transformers with $10^6$ to $10^8$ parameters, and separately XGBoost classifiers,
were trained on the same data to predict the output bits one at a time.
The training data contain many pairs with $x=000\ldots0$ itself.
These are direct samples of the target distribution at that input, which favors the classical models.
The team drew 200,000 samples from each model and scored them with KL divergence and XEB.
At the smallest sizes, the classical models matched the target distribution closely (Fig. 2d).
As the size grew, their XEB fell much faster than the hardware's (Fig. 2d).
The authors report them as substantially worse than the quantum hardware, even with its noise.

#### Beyond-classical estimate (inferred, not run)

The authors do not expect 816 shallow qubits to be beyond classical simulation.
For a larger case, they took the 67-qubit random circuits of an earlier Google experiment (Morvan et al., the paper's Ref. 30)
and rewrote them as an IDQNN with 34,304 shallow qubits.
They simulated only the training step on that model.
For generation, they used the XEB that the earlier experiment measured as a proxy for the learned model's XEB.
They compared it with the estimated best XEB that the Frontier supercomputer could reach with $10^{30}$ floating-point operations,
about 18,800 years of Frontier time (Fig. 2e).
They call 34,304 an upper bound on the qubits needed, because better mappings may exist.

#### Hardness, proven under an assumption

Sampling an IDQNN equals sampling a deep circuit (Lemma 2, proven).
Proposition 4 then shows: if a classical algorithm with polynomial running time could sample exactly from such deep circuits,
the non-uniform polynomial hierarchy would collapse to a finite level.
The polynomial hierarchy is a sequence of complexity classes that generalizes P and NP;
its collapse is widely considered unlikely.
Hardness for samples that are only approximately right needs further conjectures, which the paper cites but does not prove.

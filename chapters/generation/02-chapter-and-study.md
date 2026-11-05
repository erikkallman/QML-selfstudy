### This chapter and the study

| | The study | This chapter |
|:---|:---|:---|
| Size | 816 shallow qubits, run as a deep circuit on 68 physical qubits over 12 time steps | 6 qubits on a 2-by-3 grid, simulated directly |
| Hardware | Superconducting processor, with noise | Noiseless PennyLane simulator |
| Circuit | IDQNN (Definition 16): initial states from $x$, $R_Z$, CZ on the grid edges, $X$-basis measurement | The same four layers |
| Input bit 1 | Initial state $\lvert0\rangle$; on hardware, a mid-circuit measurement and reset | Initial state $\lvert0\rangle$ |
| Training data | Pairs from the same circuit family, with angles the authors chose | The same, with six angles that we chose |
| Training inputs | One third all zeros, one third 40% ones, one third 80% ones | The same mixture |
| Training rule | Eq. (S.2.1) | The same formula |
| Training pairs | 200,000 per angle set | 2,000 to 20,000 (Lab slider) |
| Score | Linear XEB against the ideal circuit | TVD and held-out NLL, computed exactly |
| Classical models | XGBoost and transformers | Left out |
| Classical simulation | Not expected to be hard at 816 shallow qubits; inferred hard at 34,304 | Easy: all 64 probabilities computed exactly |

This chapter therefore demonstrates the training rule on a circuit with correlated output bits.
It does not show a quantum advantage, and it compares with no classical generative model.

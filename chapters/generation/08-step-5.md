### 5. Generate new bitstrings and score them

Now run the fitted circuit at input $x=000000$.
All six qubits start in $\lvert+\rangle$, and all 7 CZ gates entangle their qubits, so the six output bits are correlated.
In the study, this is the only input run on hardware, and the one the authors call hardest to simulate classically.

Read the first Lab plot:

- The black curve is the target circuit's probability for each of the 64 bitstrings.
- The colored curve is the fitted circuit's probability. The gap between the two curves is the model error.
- The dots are frequencies in a finite set of new samples. They scatter around the colored curve.
  This scatter is sampling error.
- In the second plot, each row is one new six-bit sample.

Two scores measure the fit:

- Total variation distance (TVD) is half the sum of the absolute differences between two distributions,
  over all 64 bitstrings. 0 means they are identical.
  At the default settings, the TVD at input 000000 falls from 0.241 for an untrained circuit
  (every angle 0.15) to 0.016 for the fitted circuit.
- Held-out negative log-likelihood (NLL) averages $-\log p(y\mid x)$ over 4,096 test pairs that training never saw.
  Lower is better. The untrained circuit scores 5.110 nats, the fitted circuit 3.939, and the target circuit itself 3.938.
  Uniformly random bitstrings would score $\log 64=4.159$.

The study scores with linear XEB instead.
At 816 shallow qubits, the distribution has $2^{816}$ entries, so TVD and exact NLL cannot be computed.

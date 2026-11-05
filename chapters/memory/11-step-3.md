### 3. Compare with the exact answer

We built the device, so its characteristic function is known exactly:
$$\lambda(ib)=\cos(1.8b)\,e^{-2(0.12)^2b^2}.$$
"The question" explains what this function tells about the device.
`characteristic_truth` computes it. Only the scores and the black curve in the Lab use it; the estimator never does.

At the chosen $b$, the gap between the estimate and the black curve is the test error of one experiment.
The RMS error is its typical size over repeated experiments.
`rms_error` computes it with the formula of the first question in step 2.
It needs the exact $\lambda$, which an experiment does not have.

To halve the RMS error, the number of samples must grow four times.
So the squared ratio of two RMS errors is the ratio of the samples needed for the same error.
`sample_ratio` gives how many times more samples the 0 dB baseline needs than the chosen squeezing.
That ratio compares the sample complexity of the two settings. At 5 dB and $b=1.5$ it is about 26.

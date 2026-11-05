### How the experiment implements the scheme

The experiment builds the circuit of "The idea" from optical components.
The figure groups the components under the gates of that circuit.
Each fact below names its source in the arXiv version.

- S, two-mode squeezing: two optical parametric oscillators (OPOs) emit continuous-wave squeezed light at 1550 nm.
  Each OPO is an optical cavity with a nonlinear crystal (PPKTP), pumped at 775 nm (Supplementary Section A.1).
  The two outputs are single-mode squeezed vacua with orthogonal polarizations.
  Phase locks set one to be squeezed in $X$ and the other in $P$ (Supplementary Section A.2).
  A polarizing beamsplitter (PBS) combines them into one beam.
  A half-wave plate (HWP) then mixes the two polarizations 50:50 (Fig. S1).
  The result is a two-mode squeezed vacuum in the two polarization modes of one beam.
  The vertical polarization (V) is the probe, and the horizontal polarization (H) is the memory (Supplementary Section A).
  So the memory travels in the same beam as the probe.
  It is stored only for the time the probe takes to pass the device, so no separate storage device is needed.
- D, the device: a laser beam, the displacement beam, passes an intensity modulator (IM) and a phase modulator (PM) (Fig. S1).
  The IM sets $\operatorname{Re}\alpha$ and the PM sets $\operatorname{Im}\alpha$ (Supplementary Section A.4).
  The IM also displaces the beam in $P$. The team corrects this crosstalk
  by subtracting it from the displacement that the PM sets (Supplementary Section A.4).
  An arbitrary waveform generator drives both modulators and so implements the random displacement process (Fig. S1).
  For mode $j$, each drive waveform is proportional to the mode function $f_j(t)$ (defined below).
  The amplitudes of the two waveforms set the displacement $\alpha_j$ at the 3.8 MHz sideband frequency (Supplementary Section A.4).
  The displacement beam is a weak coherent state in V polarization (Supplementary Section A.4).
  It enters the squeezed beam through a 99:1 tapping mirror, a highly reflective mirror (Supplementary Sections A and A.4).
  Because it is V-polarized, it displaces the probe and not the memory (Supplementary Section A).
- BS and the two detectors, the Bell measurement: a second HWP, at −22.5°, reverses the polarization mixing of the first HWP.
  It mixes H and V 50:50, as the beamsplitter BS does in the circuit.
  Its outputs are two displaced single-mode squeezed vacua, in H and V.
  The displacement is split evenly between them (Supplementary Section A).
  A PBS then separates H and V.
  The local oscillator (LO), a strong coherent beam with circular polarization, enters at the same PBS.
  Each squeezed mode leaves the PBS together with the orthogonal polarization component of the LO.
  Each pair passes a HWP at 22.5° and a PBS, whose two outputs go to the two photodiodes of a balanced homodyne detector.
  The circular polarization gives the two LO components a relative phase of $\pi/2$.
  So one detector measures $X$ and the other $P$, each the squeezed quadrature of its mode (Supplementary Section A).

A digitizer records the outputs of both detectors as time traces (Fig. S1; Supplementary Section A.3).
Each mode is a temporal mode: one 1 µs time bin of the beam, weighted by a mode function $f_j(t)$ (Supplementary Section A.3).
The mode function is a 3.8 MHz sinusoid under a Gaussian envelope with a full width at half maximum of 320 ns
(main text; Supplementary Section A.3).
For mode $j$, the team multiplies each trace by $f_j(t)$ and integrates (Supplementary Eq. S1).
The two values give the entry $\zeta_j$ of the sample, as the Bell measurement in "The idea" does (Supplementary Section B.2).
One sample therefore takes $n$ time bins: $n=100$ in Task 1 and $n=120$ in Task 2.

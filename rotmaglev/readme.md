# Rotational Magnetic Levitation: A Folded/SHS Framework with Practitioner Playbook

**Goal.** Provide an experiment-ready guide to rotational magnetic levitation (RML) with a concise theoretical scaffold based on Floquet averaging, Stable Hamiltonian Structures (SHS), and folded symplectic normal forms. The document is split into:

1) **Quick-start for practitioners** (setup, tuning protocol, measurements, troubleshooting).  
2) **Design of experiments** (DoE matrices, factor sweeps, recommended plots).  
3) **Theory to practice** (intuitions → formulas → predictions).  
4) **Appendix** (derivations: Floquet averaging, SHS on energy shells, fold normal form, scaling relations).

---

## 1. Quick‑Start for Practitioners

### 1.1 Hardware & Materials
- **Rotor magnet (Rm):** Diametrically magnetized cylinder or sphere, mounted on a high‑speed motor with RPM readout; radial magnetization helps produce a strong transverse rotating field.  
- **Floater magnet (Fm):** Smaller permanent magnet (sphere or short cylinder) serving as the levitated object.  
- **Bias magnet (Bm):** Small static magnet above rotor to supply a controllable **vertical field component** \(B_{r,z}\). Mount it on a micrometer stage for millimeter‑level positioning.
- **Alignment frame:** 3‑axis translation stages for rotor–floater separation \(d\) and for Bm.  
- **Damping option:** An adjustable aluminum plate or a viscous bath (water/glycerin) placed below the floater to provide tunable damping during capture.  
- **Sensing:** High‑speed camera, IMU on floater (if mass allows), Hall sensors on a ring, and a laser distance sensor (or camera stereo) for \(z\)‑height.

**Recommended starting geometry.** Rotor radius \(R_r\) ≈ 15–25 mm; Floater radius \(R_f\) ≈ 5–10 mm; initial separation \(d_0\) ≈ 10–40 mm (to be swept). Use N42–N52 NdFeB for both.

### 1.2 Setup & Safety
- Enclose rotor with a **clear shield**. Confirm rotor balance up to target RPM (e.g., 12–18k RPM).  
- Fix the **spin axis vertical**; mark the zero of \(B_{r,z}\) (no bias magnet).  
- Confirm polarity and approximate magnitudes with a handheld Gaussmeter.

### 1.3 First Levitation Protocol (Minimal knobs)
1. **Dial a small vertical bias**: place Bm to produce \(B_{r,z}\sim 1–10\%\) of the rotor’s transverse field at the floater.  
2. **Set separation**: start at \(d\approx 25\) mm.  
3. **Spin up**: sweep rotor frequency \(\omega_r\) slowly from low to high.  
4. **Watch for capture** into the **blue phase**: the floater tilts slightly (\(\theta_f\ll 1\,\text{rad}\)), precesses synchronously, and vertical height stabilizes.  
5. **Remove damping** (if used) after capture; it should remain levitated.

**Tell‑tales of success:** small, nearly constant tilt; steady phase lag; height decreases mildly as you increase \(\omega_r\).

**If it fails to capture:** increase \(B_{r,z}\) slightly and/or introduce damping (aluminum plate within 5–10 mm below floater) to grow the basin of attraction.

### 1.4 Knobs & Qualitative Effects
- Increasing **\(\omega_r\)** → tends to **reduce** levitation height and stiffen the orientation (smaller \(\theta_f\)).  
- Increasing **\(B_{r,z}\)** → widens the capture basin, reduces \(\theta_f\), stabilizes the phase‑locked state.  
- Increasing **floater size** \(R_f\)**:** raises the required \(\omega_r\) (inertia \(I_f\propto R_f^5\)).  
- Increasing **remanence** has weaker effects on thresholds; modestly increases height.

### 1.5 Minimal Measurement Set
- Levitation **height** vs **frequency**: \(z(\omega_r)\) or \(d(\omega_r)\).  
- Floater **tilt** \(\theta_f\) and **phase lag** \(\phi\) vs \(\omega_r, B_{r,z}\).  
- **Capture probability** vs \(B_{r,z}\) (with/without damping).

### 1.6 Troubleshooting
- **Jitter/no capture:** Increase \(B_{r,z}\) or add damping during capture. Check rotor wobble.  
- **Sudden drop at high \(\omega_r\):** You hit a mode transition (bifurcation). Back off \(\omega_r\) or change \(d\).  
- **Floater spins uncontrollably:** Excessive \(B_{r,\perp}\) asymmetry; reduce tilt/misalignment of rotor magnetization axis or lower \(\omega_r\).  
- **Sensitivity to hand proximity:** The system is near the fold (\(F_z\approx 0\)); increase \(B_{r,z}\) for margin.

---

## 2. Design of Experiments (DoE)

### 2.1 Factor Plan (core 2×4 sweeps)
- \(\omega_r\): 6–18 krpm, 8–10 evenly spaced levels.  
- \(B_{r,z}\): 0, 0.5, 1, 2, 5 mT (measured at the floater location with rotor off).  
- \(d\): 10–40 mm, step 2.5–5 mm.  
- \(R_f\): 5, 6, 8, 10 mm (constant material).  
Optional: vary remanence by mixing materials or temperature.

### 2.2 Response Variables
- **Levitation height** \(z\), **tilt** \(\theta_f\), **phase lag** \(\phi\), **capture probability**, **time‑to‑capture** (with and without damping), **mode labels** (UD/Side/Mixed/U‑shape), and **drop frequency**.

### 2.3 Recommended Plots
- \(z\) vs \(\omega_r\) at fixed \(B_{r,z}\) (expect decreasing trend).  
- \(\theta_f\), \(\phi\) vs \(\omega_r\) at several \(B_{r,z}\).  
- **Stability map** in the \((\omega_r, d)\) plane for each \(B_{r,z}\).  
- **Capture probability** vs \(B_{r,z}\) with/without damping.  
- **Threshold \(\omega_r\)** vs **\(R_f\)** (log–log slope ≈ \(5/2\) if other scales are fixed; see §4.4).

### 2.4 Protocol Notes
- Randomize run order to avoid thermal drift.  
- Hold rotor–floater lateral offset constant (or record it).  
- If using a viscous bath for damping, note effective buoyancy changes height; report “dry‑equivalent” height via simple Archimedes correction.

---

## 3. Theory → Practice: Intuition, Formulas, Predictions

### 3.1 Intuition in One Paragraph
A fast, nearly transverse rotating magnetic field from the rotor creates a time‑periodic torque on the floater. A small **constant vertical field** \(B_{r,z}\) picks a preferred axis (the “Reeb” direction). Above a critical speed, the floater **phase‑locks** (blue phase): its tilt \(\theta_f\) and phase lag \(\phi\) become (approximately) constant, while it precesses at the drive rate. In this state, the **time‑averaged vertical force** becomes **non‑monotone** in distance, crossing zero with **negative slope** at the levitation height—yielding a restoring force. Damping helps you land there but is not required to maintain it.

### 3.2 Working Formulas for the Blue Phase
Let \(I_f\) be the floater moment of inertia, \(m_f\) its magnetic moment magnitude, and \(B_{r,\perp}\) the transverse amplitude of the rotor field at the floater. In the locked steady state (drive frame)
\[
\phi \approx \frac{\zeta_{\text{rot}}\,\omega_r}{I_f\omega_r^2 - m_f B_{r,z}}, \qquad
\theta_f \approx \frac{m_f B_{r,\perp}}{I_f\omega_r^2 - m_f B_{r,z}}.
\]
**Implications.**
- Increasing **\(\omega_r\)** decreases \(\theta_f\) and \(\phi\).  
- Increasing **\(B_{r,z}\)** decreases \(\theta_f\) and \(\phi\).  
- **Finite inertia** \(I_f\) is essential (drag alone cannot replace it).  
- For a sphere of radius \(R_f\) and density \(\rho\), \(I_f\propto R_f^5\); thus the **threshold speed** grows roughly like \(R_f^{5/2}\) if fields scale weakly with size.

### 3.3 Folded Normal Form for Vertical Equilibrium
Define the **time‑averaged vertical force** \(F_z(d; \omega_r, B_{r,z},\dots)\). Near a stable levitation distance \(d_\star\), expand
\[
F_z(d) \approx K\,(d-d_\star) + \cdots, \quad K<0.
\]
The **fold set** is \(\{F_z=0\}\). When the sign of the reduced two‑form flips across this set (repulsive to attractive), the stable crossing with **negative slope** is the folded symplectic “good” side. Practically: if a gentle tap makes the floater return, you are on the stable side; if it spirals away, you are on the unstable side.

### 3.4 SHS Picture & Reeb‑Locked Orbit
On an energy shell \(M^3=\{H_{\text{eff}}=E\}\), there exists a 1‑form \(\lambda\) (contact‑like) whose **Reeb vector** approximates the locked precession (set by \(B_{r,z}\)). The blue phase is a **closed Reeb‑type orbit**; linearization has one stable direction (vertical) and neutral drift along the orbit. Increasing \(B_{r,z}\) strengthens coorientation and enlarges the **basin of attraction**—matching the observed role of bias and damping during capture.

### 3.5 Practitioner Predictions (Testable Now)
1. **\(\theta_f(\omega_r, B_{r,z})\)** follows the rational form above; fit experiments to estimate \(I_f\) and effective field amplitudes.  
2. **Levitation height shrinks** monotonically with \(\omega_r\) at fixed \(B_{r,z}\).  
3. **Hysteresis** under slow cycles in \((\omega_r, B_{r,z})\) that encircle the fold; geometric phase in the locked \(\phi\).  
4. **Capture probability** increases with \(B_{r,z}\) and with damping during approach, but the steady state persists **after** damping is removed.  
5. **Nano‑regime**: intrinsic spin angular momentum can substitute for drive‑induced twist, allowing stabilization in static fields (qualitative crossover experiment).

---

## 4. Experiment Recipes

### 4.1 Mapping the Reeb Direction (Bias‑Sweep)
- Fix \(d\). For each \(B_{r,z}\) level, sweep \(\omega_r\) upward; record \(\theta_f,\phi,z\).  
- **Expected:** decreasing \(\theta_f,\phi\) with both \(\omega_r\) and \(B_{r,z}\); widening capture basin vs \(B_{r,z}\).

### 4.2 Height–Frequency Curves (Core Plot)
- For 2–3 values of \(B_{r,z}\), measure \(z(\omega_r)\).  
- **Expected:** \(z\) strictly decreases; inflection indicates proximity to a mode transition.

### 4.3 Basin Mapping with Damping
- Place aluminum plate at several gaps (2–20 mm). From randomized initial conditions, measure **capture probability** into blue phase.  
- **Expected:** strong improvement at small gaps; once captured, remove plate → levitation persists.

### 4.4 Size Scaling Test
- Repeat §4.2 for \(R_f=5,6,8,10\) mm. Estimate the minimum \(\omega_r\) for stable blue‑phase capture at each size.  
- **Expected:** \(\omega_{r,\min}\propto R_f^{5/2}\) (holding field geometry roughly constant). Deviations quantify field‑geometry scaling.

### 4.5 Hysteresis/Monodromy Loop
- Perform slow loops in parameter space: increase \(\omega_r\) while decreasing \(B_{r,z}\), then reverse. Track \(z, \phi\).  
- **Expected:** loop area ≠ 0 in \((\omega_r,B_{r,z})\) → height and phase do not return identically (contact‑geometric phase).

---

## 5. Data Analysis Checklist
- **Fit** \(\theta_f\) and \(\phi\) to the rational forms in §3.2 to extract \(I_f\) and effective field coefficients.  
- **Segment** time‑series into modes (UD/Side/Mixed/U) via spectral clustering on (\(z(t),\theta_f(t),\phi(t)\)).  
- **Construct** stability regions in the \((\omega_r,d)\) plane for each \(B_{r,z}\).  
- **Quantify** capture probability vs \(B_{r,z}\) and plate gap; fit with a logistic curve.

---

## 6. Extensions & Variations
- **Non‑axisymmetric rotors:** Purposefully tilt rotor magnetization by \(\alpha\) to control \(B_{r,z}\) without a separate bias magnet.  
- **Multi‑rotor lattices:** Levitate arrays; look for synchronization and collective “blue‑phase crystals.”  
- **Fluid media:** Vary viscosity to map capture‑time vs damping with constant steady‑state height.  
- **Sensing upgrade:** 3D Hall‑sensor ring to reconstruct \(B\) and test the averaged‑field model.

---

## Appendix A: Floquet/Kapitza Averaging Sketch
Let the rotor create a field \(\mathbf{B}_r(t)=B_{r,\perp}(\cos\omega_r t\,\hat x+\sin\omega_r t\,\hat y)+B_{r,z}\,\hat z\). The floater’s dipole \(\mathbf{m}_f\) obeys rigid‑body dynamics with torque \(\boldsymbol\tau = \mathbf{m}_f\times \mathbf{B}_r\) and (optional) rotational drag \( -\zeta_{\text{rot}}\,\boldsymbol\omega_f\). Write the Euler equations on \(SO(3)\) or, after reduction by symmetry, on \(S^2\) for the direction \(\hat m_f\). Averaging over \(2\pi/\omega_r\) yields an effective potential term of order \(B_{r,\perp}^2/\omega_r^2\) plus a gyroscopic correction proportional to \(I_f\omega_r\). In the **locked** regime, \(\hat m_f\) keeps a constant tilt \(\theta_f\) and phase lag \(\phi\), giving the rational formulas of §3.2.


## Appendix B: SHS on the Energy Shell
Take the (averaged) Hamiltonian \(H_{\text{eff}}\) on \(T^*(S^2\times\mathbb{R})\). On a fixed energy level \(M^3\), choose a 1‑form \(\lambda\) such that \(\lambda\wedge d\lambda>0\) and the Hamiltonian vector field restricts to be **conformal** to the Reeb field \(R\) of \(\lambda\) (stable Hamiltonian structure). The small but nonzero \(B_{r,z}\) provides the coorientation and selects the **Reeb direction** (precession axis). The blue phase corresponds to a closed Reeb‑like orbit with linearized Poincaré map having a single stable eigenvalue (vertical displacement) and a neutral rotation along the orbit.


## Appendix C: Folded Symplectic Normal Form (Vertical Motion)
In reduced coordinates \((d,p_d)\) for the vertical degree of freedom, the averaged 2‑form can flip sign across the **fold set** \(\Sigma =\{F_z(d)=0\}\). A local model is
\[\omega = \omega_0 + s\, ds\wedge \lambda,\]
where \(s\) is the signed distance to \(\Sigma\) and \(\lambda\) is the contact 1‑form inherited from precessional motion. Stability of the levitation height corresponds to \(\partial_d F_z|_{d_\star}<0\), i.e., the “good” side of the fold with restoring force toward \(\Sigma\).


## Appendix D: Scaling Relations
- **Inertia:** \(I_f\sim \rho R_f^5\) (sphere: \(\tfrac{8\pi}{15}\rho R_f^5\)). Threshold \(\omega_r\) set by balance \(I_f\omega_r^2\sim m_f B_{r,z}\) → \(\omega_{r,\min}\propto R_f^{5/2}\) if \(m_f\propto R_f^3\) and \(B\) weakly size‑dependent.  
- **Tilt:** \(\theta_f\propto B_{r,\perp}/(I_f\omega_r^2 - m_f B_{r,z})\).  
- **Height trend:** As \(\omega_r\) increases, the effective averaged potential stiffens → \(d_\star\) decreases.


## Appendix E: Suggested Bill of Materials & CAD Notes
- Off‑the‑shelf BLDC with encoder; 3D‑printed chuck with set screws for magnet; V‑groove bearings for alignment; acrylic shield; micrometer stages for \(d\) and Bm; small Gaussmeter; aluminum plate on linear stage. Provide CAD with slotted mounts to tune lateral offset and Bm height precisely.


## Appendix F: Analysis Notebook Outline
- **Inputs:** RPM vs time, \(z(t)\), \(\theta_f(t)\), \(\phi(t)\), \(B_{r,z}\), \(d\), \(R_f\).  
- **Processing:** smoothing, phase extraction, mode classification (spectral clustering), locked‑state parameter estimation.  
- **Fits:** rational \(\theta_f,\phi\) models; logistic for capture vs bias/damping; scaling for \(\omega_{r,\min}(R_f)\).  
- **Outputs:** stability maps, scaling plots, residuals, parameter tables.

---

### One‑Page Executive Summary (for a lab handout)
- Add a **small vertical bias** \(B_{r,z}\). Spin up the rotor slowly. Look for a small, constant \(\theta_f\) and steady \(\phi\). Height drops as \(\omega_r\) rises. Use aluminum plate only for capture. Map \(z(\omega_r)\), \(\theta_f(\omega_r,B_{r,z})\), and capture probability vs \(B_{r,z}\). Fit the simple rational formulas to extract inertial and field scales. The stable point lives on the **fold** \(F_z=0\); negative slope means you’re safe. The SHS/Reeb picture explains why the non‑minimum energy state is robust once locked.


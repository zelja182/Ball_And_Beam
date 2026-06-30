# Ball-and-Beam Simulink Model — Notes and Resources

Notes on the nonlinear plant model (kinematics, gravity branch, upper branch) and external links for further reading and videos.

---

## Model structure (signal flow)

```text
θ (servo)  →  kinematics  →  α (beam angle)
                              ↓
                    ┌─────────┴─────────┐
                    ↓                   ↓
              lower branch         upper branch
              g·sin(α)             r·α̇²
                    └─────────┬─────────┘
                              ↓
                         sum → gain → ∫∫ → r (ball position)
```

| Simulink part | Thesis equation | Role |
|---------------|-------------------|------|
| Left (θ → sin → 30/261) | (3.1.6) α = (l₁/L) sin θ + C | Kinematics: servo → beam angle |
| Bottom (sin α → ×9.81) | (3.1.12) gravity part | Ball on a **fixed** tilt |
| Upper (dα/dt → square → × r) | Not in (3.1.12) | Extra term when beam **moves** |
| Gain −7/5 + integrators | (3.1.12) factor (I/R² + m) = (7/5)m | Acceleration → position |

Parameters used in the model: l₁ = 30 mm, L = 261 mm, (I/R² + m) = (7/5)m for a solid sphere.

---

## Bottom branch — equations (3.1.6) and (3.1.12)

**Kinematics:**

α = (l₁/L) sin θ + C

**Static / slow beam (gravity only):**

(I/R² + m) ẍ = −mg sin α

For a solid sphere: I/R² = (2/5)m, so I/R² + m = (7/5)m.

When the beam is only tilted and not rotating (α̇ = 0), only the bottom branch matters.

---

## Upper branch — r·α̇² (what it is physically)

Upper branch computes:

r · (dα/dt)² = r · α̇²

where **r** is ball position along the beam and **α̇** is beam angular velocity.

**Meaning:** When the beam **rotates**, a ball at distance **r** from the pivot is not in the simple “ball on a slope” case. There is an extra inertial (centrifugal) term along the beam. The faster the beam spins and the farther the ball is from the pivot, the larger this effect.

**Intuition:**

- Beam still (α̇ = 0) → upper branch = 0 → only g sin α (eq. 3.1.12).
- Beam swinging quickly → r·α̇² becomes important (exactly what PID control does).

**Full dynamic equation (conceptually):**

(7/5)m · r̈ = −mg sin α + (term with r·α̇²)

Signs depend on axis conventions in Simulink; structure is: gravity + rotation effect.

The CTMS standard form:

0 = (J/R² + m) r̈ + mg sin α − m r α̇²

Rearranged:

r̈ = (−1/(J/R² + m)) · (mg sin α − m r α̇²)

---

## Best match for this Simulink model — CTMS (University of Michigan)

Control Tutorials for MATLAB and Simulink — same equation including the r·α̇² term.

| Topic | URL |
|-------|-----|
| Full equations + linearization | https://ctms.engin.umich.edu/CTMS/index.php?example=BallBeam&section=SystemModeling |
| Simulink build (similar block layout) | https://ctms.engin.umich.edu/CTMS/index.php?example=BallBeam&section=SimulinkModeling |
| PID / lead compensator | https://ctms.engin.umich.edu/CTMS/index.php?example=BallBeam&section=SimulinkControl |
| System analysis (poles, instability) | https://ctms.engin.umich.edu/CTMS/index.php?example=BallBeam&section=SystemAnalysis |
| Simscape variant | https://ctms.engin.umich.edu/CTMS/?example=BallBeam&section=SimulinkSimscape |

Downloadable Simulink model (`ball.slx`) is linked from the Controller Design page.

Mirror / summary: https://www2.ensc.sfu.ca/people/faculty/saif/ctm/examples/ball/ball.html

---

## YouTube and video links

Linked from CTMS:

| Video | URL | Content |
|-------|-----|---------|
| Modeling intro | https://www.youtube.com/watch?v=vwso-xHLNGc | General modeling (CTMS series) |
| Modeling challenges | https://www.youtube.com/watch?v=Ro2uu70o1Fs | Why ball-and-beam is hard to control |
| Time response / instability | https://www.youtube.com/watch?v=F4w0rslb04E | Open-loop response |

MathWorks (Simulink, not ball-specific):

| Video | URL |
|-------|-----|
| Getting Started with Simulink | https://www.mathworks.com/videos/getting-started-with-simulink-69027.html |
| Simulink Control Design overview | https://www.mathworks.com/videos/simulink-control-design-overview-61203.html |

Related demo:

| Video | URL | Note |
|-------|-----|------|
| Ball on seesaw — MATLAB animation | https://www.youtube.com/watch?v=eB3Jgighqe4 | Position control on inclined surface (related, not identical) |

MathWorks ball-on-beam example (iPID / nonlinear control):

https://www.mathworks.com/help/slcontrol/ug/ipid-model-free-control-using-ulm.html

---

## Understanding the upper branch (r·α̇²) — written resources

| Resource | URL | Why useful |
|----------|-----|------------|
| Ball on rotating beam (Physics SE) | https://physics.stackexchange.com/questions/694341/ball-on-a-rotating-beam-equations-of-motion | Lagrangian derivation; shows mp·θ̇² term |
| LACCEI paper (PDF) | https://laccei.org/LACCEI2014-Guayaquil/RefereedPapers/RP176.pdf | Lagrange vs Newton; missing centrifugal terms if rotating frame ignored |
| Georgia Tech — ball and beam | https://pvela.gatech.edu/classes/doku.php?id=ece6554:project_ballbeam | Clean Lagrangian → ẍ − θ̇² x + g sin θ = 0 |
| OpenStax — fictitious forces | https://openstax.org/books/college-physics-2e/pages/6-4-fictitious-forces-and-non-inertial-frames-the-coriolis-force | Merry-go-round intuition for rotating-frame effects |
| Engineering Stack Exchange — linearization | https://engineering.stackexchange.com/questions/45235/modelling-of-ball-and-beam-system | When α̇ terms are dropped in linear models |
| Utah — ball and beam lab (PDF) | https://my.ece.utah.edu/~bodson/fun/bbeam.pdf | Manual control + PD design |
| Oklahoma State — lab handout (PDF) | https://thl.okstate.edu/Handout_BallBeamOpt.pdf | Nonlinear Simulink + LQR workflow |

Kinetic-energy intuition: the term ½ m r² α̇² in total kinetic energy leads to the r·α̇² term in the equation of motion (ball “orbiting” the pivot as the beam rotates).

---

## Simpler model (thesis eq. 3.1.12 only — no upper branch)

Quanser SRV02 lab often uses only:

ẍ = (5/7) g sin α

(no r·α̇²) when beam angle is assumed to be controlled quickly:

https://www.se.rit.edu/~se463/ResearchProject/Quanser/SRV02_Exp3_Ball%20&%20Beam.pdf

That matches the **bottom branch only**. The full Simulink model is the more complete nonlinear plant.

---

## Suggested reading / viewing order

1. CTMS **System Modeling** — full equation; see when r·α̇² is removed at linearization.
2. CTMS **Simulink Modeling** — compare block-by-block with your diagram.
3. Physics Stack Exchange or LACCEI PDF — why r·α̇² appears.
4. YouTube **Modeling challenges** — why control is difficult.

---

## Link to system identification work in this project

Grey-box and black-box identification in `System_Identification/` model **PWM → beam angle θ** (servo dynamics), not the full ball plant above.

Full control chain:

```text
PWM → servo θ → kinematics → α → ball dynamics → r
         ↑                           ↑
   (identified TF / NLARX)     (this Simulink model)
```

For PID on hardware, distance sensor ≈ ball position **r**; actuator commands beam angle via servo.

---

*Saved for thesis reference. External URLs were valid when this note was created; check links if pages move.*

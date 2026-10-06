# SLAM study curriculum

Repository edition of the 30-week plan created on 6 October 2026. Imported from the saved plan-generation source; document navigation and Word controls are replaced with Markdown. Resource links are preserved from that plan, not revalidated during setup.

Visual SLAM and VIO Study Plan

A practical curriculum for Yusuf Huseyin Durkaya

30 weeks · 12 hours per week · approximately 360 hours

Version 1  |  6 October 2026

Build the ability to formulate, implement, test, and explain a small monocular visual–inertial estimation system in Python. This curriculum addresses the interview feedback on algorithm ownership, Python, optimization, pose representations, monocular vision, camera–IMU fusion, mobile sensors, and recent visual SLAM experience.

Weeks are units of completed work, not fixed deadlines. Repeat a week when its completion criterion is not met. The schedule is an estimate for study alongside employment, not a guarantee of senior-level mastery.

The assistant tracks dates and completed work in [progress.md](progress.md).


## How to use this curriculum

Start with [Week 1](../exercises/week01/README.md). You implement algorithms and
explain your reasoning in conversation. The assistant writes, adds, maintains,
and runs tests, and handles all documentation, reports, and progress updates.
You are not assigned test writing or Markdown edits. Running existing tests
is optional.

This division of responsibilities applies to every week below. References to
testing, recording findings, documenting assumptions, or producing reports are
assistant responsibilities; discuss the technical reasoning in chat. Sensor
recording and algorithm implementation remain hands-on learning activities.
The assistant records only observed evidence and verifies understanding before
marking a completion criterion met.

## Contents

- [Python and geometry](#python-and-geometry)
- [Probability and optimization](#probability-and-optimization)
- [Monocular visual odometry](#monocular-visual-odometry)
- [Pose graphs and loops](#pose-graphs-and-loops)
- [Camera and IMU estimation](#camera-and-imu-estimation)
- [Mobile acquisition and validation](#mobile-acquisition-and-validation)
- [Research and interview readiness](#research-and-interview-readiness)
- [Evaluation standards](#evaluation-standards)
- [Interview assessment](#interview-assessment)
- [Resource directory](#resource-directory)

## Working method

The plan combines the mathematical implementation detail of the web answer with the staged validation and mobile-data work of the earlier answer. It adds explicit probability foundations, dataset splits, numerical checks, initialization requirements, and interview evidence. A 12-week schedule is too compressed for the full scope; mobile recording alone also does not establish reliable mobile VIO experience.


| Weeks | Focus | Result |
| --- | --- | --- |
| 1–4 | Python and geometry | Tested geometry library and simulator |
| 5–8 | Probability and optimization | Pose optimizer and bundle adjustment |
| 9–12 | Monocular VO | Tracking, mapping, local BA and evaluation |
| 13–14 | Pose graphs and loops | Metric graph and scale-correction experiments |
| 15–23 | Camera–IMU estimation | Propagation through validated real-data VIO |
| 24–26 | Mobile data | Recorder, calibration and phone experiments |
| 27–30 | Research and readiness | Algorithm experiment and interview portfolio |


### Repository and implementation ownership

Use one repository named visual-inertial-estimation-lab. Separate your educational implementations from library-based references. Suggested folders: geometry, optimization, vision, backend, imu, vio, datasets, experiments, reports, tests, and reference. Keep large datasets outside version control and document how to obtain them.

Use a stable Python version supported by your dependencies, and record the exact working versions. Core tools: NumPy, SciPy, OpenCV, Matplotlib, pytest, Git, and later GTSAM. Avoid upgrading the environment throughout the curriculum without a reason.


| Implement personally | Use libraries where appropriate |
| --- | --- |
| SO(3), SE(3), projection, residuals and local updates | Linear algebra decompositions and image decoding |
| Jacobian checks and selected analytical derivatives | Feature extraction, five-point and PnP hypothesis solvers |
| Small GN/LM, bundle adjustment and pose graph | Sparse linear solvers and production reference optimizers |
| IMU propagation and preintegration components | Reference IMU factors and established evaluation utilities |
| Experiment design and failure analysis | Plotting, test runners and packaging tools |

Personal implementation means you can reconstruct and explain the method; it does not mean inventing a novel algorithm or replacing every numerical library. Use AI for hints and review, but reproduce the central derivation or implementation independently before considering it learned.


### Weekly routine


| Session | Hours | Work |
| --- | --- | --- |
| Monday | 2 | Read and derive equations |
| Tuesday | 2 | Implement a minimal example |
| Thursday | 2 | Investigate failures using assistant-provided tests |
| Saturday | 4 | Integrate, experiment and plot |
| Sunday | 2 | Explain the method and discuss findings; assistant documents them |

Every week ends with your working implementation and a five-minute explanation without reading the code. The assistant supplies tests, verifies results, and writes the report covering the objective, assumptions, method, result, failure, and next action.


### Technical qualifications

- SLAM has multiple architectures; VO plus loop closure is not a complete definition.
- An SE(3) pose graph cannot correct arbitrary monocular scale drift. Understand Sim(3) and when scale must be estimated.
- An IMU does not guarantee metric-scale observability under all motions. Excitation and initialization matter.
- Recorded timestamps do not prove camera–IMU synchronization.
- Recent commits establish recent activity. Deliberate comparison with recent research establishes current technical knowledge.


## Python and geometry


### Week 1: Diagnose foundations and establish the project

**Study:** Python Tutorial chapters 4–8 and 12 [R1]: functions, data structures, modules, I/O, exceptions and environments. Review dimensions, rank, null spaces, dot/cross products, QR, SVD, least squares, derivatives, the chain rule, covariance and Gaussian distributions.

- Read a timestamped CSV and reject malformed or non-monotonic records.
- Transform an array of 3D points using a rotation and translation.
- Solve an overdetermined linear system; the assistant supplies tests for dimensions and invalid input.

**Completion criterion:** Recreate all three tasks in a fresh file and explain every array shape. If rank, covariance or the chain rule remains unfamiliar, insert a prerequisite week before advancing.

**Explain aloud:** Why is solving a linear system preferable to explicitly forming a matrix inverse?


### Week 2: Scientific Python and a synthetic camera

**Study:** NumPy quickstart [R2]: broadcasting, indexing, shapes, copies versus views, and linear algebra. Practice dataclasses, type annotations, generators and context managers. The assistant handles pytest.

- Build a pinhole-camera simulator with landmarks, known camera poses, configurable pixel noise and outliers, and a fixed random seed.
- Reject points behind the camera and save visible observations and a plot.
- Compare loop-based and vectorized projection; measure speed and check numerical equivalence.

**Completion criterion:** One command generates, projects, perturbs and plots a scene. Invalid depth is handled explicitly.

**Explain aloud:** What does each array axis represent, and when does NumPy copy memory rather than return a view?


### Week 3: Rotations

**Study:** SO(3) in Eade [R3]; use Solà [R4] for clarification and derivative reference.

- Implement hat, vee, Rodrigues/so3_exp, so3_log, quaternion multiplication, normalization, inversion, and conversions to/from rotation matrices.
- Test identity, tiny angles, ordinary angles and rotations near 180 degrees.
- Compare with SciPy only after your implementation works. Near 180 degrees compare reconstructed rotations, not necessarily identical axis-angle vectors.

**Completion criterion:** Tests pass and you can explain quaternion sign ambiguity, gimbal lock, noncommutativity, and three rotational degrees of freedom versus four quaternion coefficients.

**Explain aloud:** Why do q and −q describe the same rotation, and why is simple component-wise quaternion optimization problematic without a constraint or local parameterization?


### Week 4: Poses and local perturbations

**Study:** SE(3), adjoints, exponential/log maps and local coordinates in [R3–R4]. Adopt the conventions below and keep them in the repository.

- T_AB maps coordinates from B into A. T_WC is a camera pose; projection uses P_C = inverse(T_WC) P_W.
- Internal quaternions use wxyz. Distances are metres, angles radians and time seconds. Convert explicitly at library boundaries.
- Use translation-first increments delta_xi = [delta_rho, delta_phi] and right updates T <- T Exp(delta_xi).
- Implement SE(3) composition, inversion, exp/log, adjoint and point transforms. Account for rotation–translation coupling in the exponential.
- Implement central-difference Jacobian checking and derive a point-transform Jacobian under the chosen convention.

**Completion criterion:** Analytical and numerical derivatives agree. Explain what changes under left updates and why formulas from other conventions cannot be copied unchanged.

**Explain aloud:** How do camera pose, world-to-camera transform and body-to-camera extrinsics differ?


## Probability and optimization


### Week 5: From noise to an objective

**Study:** Maximum likelihood, MAP, priors, covariance, information and whitening. Read the introductory factor-graph explanation [R5].

- Start from cost = sum r_i transpose Sigma_i inverse r_i. Then apply a robust loss to each whitened squared residual norm.
- Simulate two sensors measuring one quantity with different noise levels. Compare equal weighting with covariance-based weighting.
- Whiten both residuals and Jacobians using the same square-root information convention.

**Completion criterion:** Demonstrate the effect of uncertainty weighting and distinguish likelihood, prior and posterior.

**Explain aloud:** Why should a less certain measurement contribute less information?


### Week 6: Gauss Newton and Levenberg Marquardt

**Study:** Linearization, normal equations, damping, conditioning and termination. Compare your implementation with SciPy least_squares [R6].

- Implement a nonlinear curve fit, then Gauss–Newton and LM.
- Implement step acceptance/rejection and log objective, step norm, gradient norm, damping and accepted/rejected steps.
- Test a good initialization and a poor one that challenges undamped Gauss–Newton.

**Completion criterion:** Your solver agrees with the reference on a well-conditioned problem and you can explain the poor-initialization behavior.

**Explain aloud:** Why does a decreasing cost not prove that the state estimate is correct?


### Week 7: Optimize one camera pose

**Study:** Pinhole projection derivatives and pose derivatives under the Week 4 right-update convention.

- Hold landmarks fixed; implement pose-only reprojection minimization, whitening, robust weighting and positive-depth checks.
- Run noise-free, one-pixel Gaussian noise, ten-percent outlier and poor-initialization experiments.
- Numerically verify analytical derivatives and inspect residuals before and after optimization.

**Completion criterion:** Recover the known pose from nearby initialization in the noise-free case. Robust estimation should improve the deliberately contaminated example; it need not win every experiment.

**Explain aloud:** Where do the projection Jacobian, pose Jacobian and residual sign enter the update?


### Week 8: Bundle adjustment and the Schur complement

**Study:** Multiple View Geometry chapters 4 and 6, and the bundle-adjustment portions of chapter 18 [R7]. If the book is unavailable, use [R5] and [R8] for the corresponding practical work.

- Jointly optimize 10 poses and 100 landmarks. Image: 640 x 480; fx = fy = 400; principal point (320, 240); seed 7.
- Place landmarks about 4–8 metres in front of cameras; camera translations span about one metre with overlapping views.
- Use one-pixel observation noise, initial rotation perturbations around 0.03 rad, camera translation perturbations around 0.05 m, and landmark perturbations around 0.1 m. Run noise-free and noisy tests separately.
- Fix the first pose and constrain one baseline length to remove gauge freedom in this synthetic exercise. That known baseline is not available to real monocular estimation.
- Implement dense and Schur-complement solutions to the same linearized system.

**Completion criterion:** Dense and Schur updates agree. Explain eliminated variables, sparsity and monocular gauge freedom.

**Explain aloud:** Why is fixing the first pose alone insufficient to determine monocular scale?


## Monocular visual odometry

Use EuRoC [R9], initially camera 0 only. Develop on MH_01_easy and MH_02_easy, validate on MH_03_medium, and reserve MH_04_difficult and MH_05_difficult for final evaluation. Inspect held-out file formats and calibration if needed, but do not tune on their trajectory results. If you do, reclassify those sequences honestly.


### Week 9: Epipolar geometry

**Study:** Multiple View Geometry chapter 9 and sections 11.1–11.6 and 11.9 [R7]. Study homogeneous coordinates, pixel versus normalized coordinates, F versus E, rank constraints, RANSAC and Sampson error.

- Implement normalized eight-point estimation on synthetic correspondences and compare with OpenCV [R8].
- Use E = transpose(K2) F K1 when camera intrinsics differ.
- Understand the five-point solver conceptually; use a library implementation rather than implementing its polynomial solver.

**Completion criterion:** Recover consistent synthetic epipolar geometry and identify a degenerate example.

**Explain aloud:** Why do additional correspondences not eliminate geometric degeneracy?


### Week 10: Initialization and triangulation

**Study:** Essential decomposition, cheirality, triangulation, reprojection refinement and parallax; chapter 12 in [R7].

- Implement candidate-pose selection by positive depth, linear triangulation and reprojection refinement.
- Start with at least 100 initialization inliers, median triangulation angle above 1 degree, positive depth in both cameras and reprojection error below 3 pixels.
- Store thresholds in configuration. Test translation, pure rotation, planar scenes and distant points.

**Completion criterion:** Initialize suitable scenes and postpone initialization when useful depth cannot be recovered. Never accept confident arbitrary structure from pure rotation.

**Explain aloud:** Why is translation direction recoverable while absolute scale remains ambiguous?


### Week 11: Tracking against a map

**Study:** ORB descriptors, persistent landmark associations, PnP and pose refinement using [R8].

- Create persistent feature/landmark IDs and 2D–3D correspondences. Add PnP RANSAC, pose refinement and tracking states.
- Initial settings: around 1,000 image features, descriptor ratio 0.75, PnP reprojection threshold 3 pixels, tracking lost below 30 PnP inliers.
- Treat settings as experimental starting points, not universal constants.

**Completion criterion:** Track a short real sequence against existing landmarks without inventing an independent translation scale at every image pair.

**Explain aloud:** What changes when estimating a pose against a map instead of chaining independent two-view motions?


### Week 12: Local mapping and local bundle adjustment

**Study:** Keyframes, triangulation, bad-point removal, local BA and boundary constraints.

- Use a five-keyframe optimization window. Insert a keyframe when tracked landmarks fall below 70% of the previous keyframe count or median parallax exceeds 1.5 degrees, provided sufficient correspondences remain.
- Keep a fixed boundary pose and an inherited scale constraint so the local optimization is well posed.
- Compare BA enabled versus disabled. Save trajectory and tracking statistics.

**Completion criterion:** Complete a continuous 60-second MH_01_easy segment, then attempt full development sequences. If reprojection error improves but trajectory worsens, investigate gauge handling, associations and map deformation.

**Explain aloud:** Which parts of this system are odometry, local mapping and optimization?


## Pose graphs and loops


### Week 13: Pose graph optimization

**Study:** Relative-pose factors and graph optimization [R5]. For T_i = T_Wi, the predicted relative transform is inverse(T_i) T_j.

- Create a metric synthetic trajectory with 50 poses, noisy relative edges and one valid loop edge.
- Implement SE(3) residuals, numerical Jacobians, weighting and a fixed first pose. Optimize with and without the loop.
- Repeat in GTSAM; inject one incorrect loop and inspect the damage.

**Completion criterion:** Explain why one loop constraint moves multiple poses and how an incorrect constraint deforms the trajectory.

**Explain aloud:** What convention does each edge measurement use, and how is it compared with the prediction?


### Week 14: Loop detection and scale

**Study:** Candidate retrieval versus geometric verification; SE(3) versus Sim(3).

- Search older keyframes using descriptors and exclude the 30 most recent frames.
- Verify a candidate with 2D–3D PnP for a consistent map, or 3D–3D similarity estimation for independently scaled submaps. Require positive depths, enough inliers and spatially distributed matches.
- Construct two synthetic submaps at different scales. Estimate Sim(3) alignment and demonstrate the limitation of SE(3)-only alignment.

**Completion criterion:** Accept a genuine revisit, reject a visually similar false candidate, and explain when scale correction is required. A full monocular Sim(3) correction backend is an extension, not this week’s required output.

**Explain aloud:** Why is visual similarity alone insufficient evidence of a valid loop?


## Camera and IMU estimation

Primary readings: OpenVINS discrete propagation [R10], Forster preintegration [R11], GTSAM preintegrated measurements [R12], and VINS-Mono [R13]. OpenVINS supplies a filtering and uncertainty perspective; the main project is optimization-based. A full MSCKF implementation is outside the required scope.


### Week 15: IMU measurement models and propagation

**Study:** Define the body as the IMU frame. R_WB maps body vectors to world. Gyroscope: omega_m = omega + b_g + n_g. Accelerometer: a_m = transpose(R_WB)(a_W - g_W) + b_a + n_a.

- Use g_W = [0, 0, -9.81] with world z upward. Implement orientation, velocity and position propagation using actual timestamps.
- Test stationary motion, constant angular velocity and known acceleration.

**Completion criterion:** Correctly initialized stationary simulation remains stationary.

**Explain aloud:** Why does an accelerometer at rest generally measure a nonzero vector?


### Week 16: Biases covariance and filtering

**Study:** Error-state propagation in [R10]. Adopt ordering [delta_theta, delta_p, delta_v, delta_bg, delta_ba].

- Add gyro/accelerometer bias, white measurement noise and bias random walk. Derive covariance propagation.
- Compare predicted uncertainty against Monte Carlo simulation. Implement a one-dimensional position/velocity Kalman filter for intuition.
- Document continuous-time noise density versus discrete sample standard deviation and convert consistently.

**Completion criterion:** Covariance stays symmetric and positive semidefinite within numerical tolerance; simulation shows the expected uncertainty scale and growth.

**Explain aloud:** How does an error-state filter treat orientation differently from an ordinary additive state?


### Week 17: Preintegrated rotation velocity and position

**Study:** Preintegration definitions and motivation in [R11].

- Implement delta_R, delta_v and delta_p between camera timestamps at a fixed bias linearization point.
- Handle interval boundaries explicitly, interpolating IMU measurements when camera timestamps fall between samples.
- Compare state reconstruction from preintegration with direct integration under identical discretization.

**Completion criterion:** Both integration paths agree under the same assumptions.

**Explain aloud:** What work does preintegration avoid repeating during optimization?


### Week 18: Bias correction and preintegration uncertainty

**Study:** Bias linearization, uncertainty and inertial residuals in [R11–R12].

- Add first-order bias correction Jacobians, preintegration covariance, IMU residuals and bias-evolution residuals.
- Compare bias correction with full reintegration for both small and large bias changes.
- Reconcile frames, gravity, integration methods and noise conventions before comparing against GTSAM.

**Completion criterion:** Small-bias corrections agree with reintegration; document where approximation error becomes significant. Do not expect bitwise identity across different integrators.

**Explain aloud:** When should preintegration be recomputed instead of applying a first-order correction?


### Week 19: Joint estimation on synthetic data

**Study:** At each keyframe use state {R_WB, p_WB, v_W, b_g, b_a}, plus landmarks and known camera–IMU extrinsics.

- If T_BC maps camera to body, use T_WC = T_WB T_BC.
- Combine visual, inertial and bias-evolution residuals plus appropriate priors in a five-keyframe batch.
- Build your educational estimator and a separate GTSAM reference with equivalent assumptions.

**Completion criterion:** Both recover a controlled synthetic trajectory from perturbed initialization. Ground-truth initialization is allowed only as a labelled diagnostic in this exercise.

**Explain aloud:** Which variables and residuals connect the cameras to the inertial trajectory?


### Week 20: Initialization and observability

**Study:** Study VINS-Mono initialization [R13] and the relationship between excitation, scale, gravity, bias and velocity.

- Detect a stationary interval when available; estimate gyro bias and an initial gravity direction, acknowledging accelerometer-bias ambiguity.
- Initialize a visual map up to scale, then align visual and inertial information to estimate scale, velocities and gravity; refine jointly.
- Reject insufficient excitation or poor conditioning. Test stationary-only, constant-velocity and varied rotation/acceleration trajectories.

**Completion criterion:** Initialize a suitably excited synthetic case and reject or flag weak cases.

**Explain aloud:** Why are absolute position and global yaw unobservable in ordinary VIO? Why cannot stationary data fully separate gravity from accelerometer bias?


### Week 21: Marginalization

**Study:** Schur-complement priors and the role of linearization. Read first-estimate Jacobian discussion [R14] for consistency context.

- Partition a linearized system into removed and retained variables and derive the marginalized prior.
- Verify first on a linear Gaussian example, then marginalize an old estimator keyframe.
- Record the prior’s linearization point and explain how nonlinear relinearization changes the problem.

**Completion criterion:** The retained-state solution matches the full solution in the linear example. Do not claim consistency preservation merely because matrix elimination works.

**Explain aloud:** Why does a marginalization prior depend on a linearization point?


### Week 22: Real EuRoC camera and IMU data

**Study:** Connect camera 0 and IMU from MH_01_easy [R9].

- Check timestamp units/order, IMU coverage, distortion, extrinsic direction, noise conventions and estimated-body versus ground-truth-body frames.
- Start with 20 seconds, extend to 60 seconds, then attempt the full sequence. Document initialization duration.
- Do not supply ground-truth scale, velocity or bias to an independently reported benchmark run.

**Completion criterion:** Complete a 60-second run without numerical divergence and save trajectory, residual, bias and timing plots. If only the GTSAM reference succeeds, state that distinction and keep debugging.

**Explain aloud:** Which frame and clock mismatches can look like an estimator failure?


### Week 23: Controlled failure experiments

**Study:** Compare visual-only, your VIO and one established monocular–inertial reference such as VINS-Mono.

- Run correct timing, artificial IMU offsets of ±5 and ±10 ms, reduced image rate, increased IMU noise, incorrect extrinsic rotation and weak excitation.
- Keep unrelated settings fixed and record residual as well as trajectory behavior.
- Write three evidence-based explanations connecting changed assumptions to observed failures.

**Completion criterion:** Three failure analyses are supported by plots and reproducible runs. VIO need not win every experiment; explain the outcomes honestly.

**Explain aloud:** How would you distinguish timing error, bias error and poor visual associations?


## Mobile acquisition and validation

Assume an Android phone. With iPhone access only, substitute AVFoundation/Core Motion after consulting their documentation; preserve the data-quality requirements. With no phone, use a mobile visual–inertial dataset but leave personal acquisition incomplete. Offline processing and on-device deployment are separate achievements.


### Week 24: Build a phone recorder

**Study:** Android SensorEvent, CaptureResult and CameraCharacteristics [R15–R17], especially timestamp semantics and camera metadata.

- Record images, gyro and accelerometer readings with acquisition timestamps; sensor types, units and accuracy; image size, exposure, focal settings and available metadata.
- Record actual sample intervals and dropped frames. Use a fixed camera configuration and disable stabilization where supported; document uncontrolled settings.
- Keep callback execution time separate from acquisition time.

**Completion criterion:** Replay a five-minute recording deterministically and explain the relationship or remaining uncertainty between camera and IMU clocks.

**Explain aloud:** Why is timestamping a callback not equivalent to timestamping the physical measurement?


### Week 25: Calibration and recording quality

**Study:** Kalibr camera–IMU workflow [R18] and its sensor/model assumptions.

- Record a stationary noise-inspection sequence, a target sequence with varied orientations and image coverage, and excited rotational/translational motion.
- Report intrinsics, extrinsics, time offset, residuals and uncertainty or limitations. Compare repeated calibration results.
- Validate on a separate recording and identify rolling shutter, blur, autofocus or timing violations.

**Completion criterion:** Calibration is checked on independent data. Successful tool execution alone is not acceptance.

**Explain aloud:** What evidence shows that a calibration transfers to another recording?


### Week 26: Run and assess phone data

**Study:** Apply the estimator to three short routes and interpret evidence without inventing ground truth.

- Record slow textured-room motion, a route returning near its start, and faster rotation or lower-light motion.
- Report tracking survival, initialization time, processing time, residuals and return-to-start discrepancy.
- Treat a closed route as a consistency check, not full trajectory ground truth. Do not report ATE without a defensible reference.

**Completion criterion:** A report connects mobile acquisition behavior to estimator performance.

**Explain aloud:** What does offline phone processing establish, and what would actual on-device execution add?

Optional four-week extension: run and profile an estimator on the phone. Include sustained latency, memory, frame backlog and thermal behavior. The core curriculum does not claim this deployment experience.


## Research and interview readiness


### Week 27: Read systems with a question

**Study:** ORB-SLAM3 [R19] tracking and mapping; VINS-Mono [R13] initialization and marginalization; OpenVINS [R20] filtering and observability; DPVO [R21] learned and geometric components.

- Compare inputs, state, frontend, backend, initialization, failure modes and compute assumptions.
- Select one paper from the preceding 12 months when you reach this week. Choose a paper addressing an observed failure and verify its sensor/hardware assumptions.
- Trace one measurement into a state update in a reference implementation. Running every system is unnecessary.

**Completion criterion:** Explain the comparison and trace one code path, rather than only summarizing abstracts.

**Explain aloud:** Which component is learned, which is geometric, and what practical assumption limits deployment?


### Week 28: Make one algorithmic change

**Study:** Default experiment: parallax-based versus fixed-interval keyframe selection.

- Keep all other components fixed. Explore thresholds on development data, select using validation, then freeze the configuration.
- Measure trajectory error, survival, keyframe count, BA runtime and total processing time.
- Run five repetitions when randomness affects the result. Include negative results.

**Completion criterion:** Explain hypothesis, implementation, trade-off and measured outcome. An unsupported improvement claim does not pass.

**Explain aloud:** How do you know the result is caused by the proposed change?


### Week 29: Reproducibility and performance

**Study:** Packaging, profiling and experiment reproduction.

- Provide commands to install the environment, obtain datasets legally, run tests, execute configured experiments and regenerate reports.
- Profile first; fix one measured bottleneck through vectorization, fewer allocations or a better data structure. Confirm numerical equivalence.
- Evaluate held-out sequences with frozen settings and preserve failures.

**Completion criterion:** A clean installation reproduces synthetic results and at least one real-data report without manual source editing.

**Explain aloud:** What changed in runtime, and what evidence shows the numerical behavior stayed the same?


### Week 30: Interview examination and ownership audit

**Study:** Prepare a technical walkthrough and review prior project ownership.

- Prepare 20 minutes: problem/sensors/assumptions 3 min; state/measurements 5 min; optimization/implementation 5 min; evaluation/failure 4 min; contribution/limitations 3 min.
- For every past SLAM role, distinguish code you wrote, components you modified, library/colleague work, mathematical decisions, measured results and limitations.
- Complete the assessment below. Adjust CV wording only where needed to reflect evidence accurately.

**Completion criterion:** Explain implementation and ownership without hiding behind library names or broad claims.

**Explain aloud:** Which mathematical decision was yours, and which experiment supports it?


## Evaluation standards

Use evo [R22], but verify one small example manually. Never compare results until timestamps, frames, sequence intervals, sensor modes and alignment are matched.


| Report field | Required record |
| --- | --- |
| Data | Sequence, sensor subset and start/end timestamps |
| Configuration | Code revision, dependency versions, seed and parameters |
| Initialization | Method, duration, failures and external information |
| Frames | Estimated and reference frames; extrinsic conversion |
| Error | ATE and relative pose error with units |
| Alignment | Exact rotation, translation and scale treatment |
| Survival | Tracked fraction, losses, restarts and gaps |
| Performance | Hardware, resolution, mean and p95 processing time |
| Health | Features, reprojection residuals, biases and solver failures |
| Limitations | Failed sequences and unmodelled assumptions |

- Monocular VO: use one global Sim(3) alignment for scale-free comparison and report the fitted scale.
- Metric VIO: use rigid alignment without scale correction for the primary result. Label any scale-corrected diagnostic separately.
- Do not align short segments independently and call the result full-trajectory accuracy. Do not join unexplained restarts.
- Use the same interval, coordinate frame and sensor configuration when comparing systems.


| Synthetic check | Initial target |
| --- | --- |
| Orthogonality and pose inverse | About 1e-10 error for ordinary double-precision cases |
| Analytical versus numerical Jacobian | Normalized difference below 1e-5 away from singularities |
| Dense versus Schur increment | Relative difference below 1e-6 on a well-conditioned example |
| Noise-free reconstruction | Near-zero residual and correct state after gauge handling |
| Covariance | Symmetric and positive semidefinite within numerical tolerance |

Sweep finite-difference steps from about 1e-4 to 1e-7. One convenient epsilon passing one example is insufficient. These thresholds are controlled-example checks, not universal benchmark requirements. Establish dataset, initialization, alignment and baseline before choosing a real-data accuracy target.


## Interview assessment

Score each competency: 0 cannot explain; 1 can explain with notes; 2 can derive or implement with minor assistance; 3 can derive, implement and diagnose independently. Personal readiness target: at least 2 everywhere and 3 in Python, geometry, optimization and ownership. This is a preparation rubric, not an employer scoring system.


| Competency | Examination task | Score |
| --- | --- | --- |
| Python | In 45 minutes load, validate and interpolate timestamped data; explain behavior on assistant-provided checks |  |
| Rotations | Explain quaternion double cover and derive a local update |  |
| Poses | Compose body, camera and world transforms unambiguously |  |
| Optimization | Derive Gauss–Newton and explain LM damping |  |
| Probability | Convert a Gaussian measurement model into a whitened residual |  |
| Bundle adjustment | Explain gauge freedom and Schur elimination |  |
| Monocular geometry | Explain E recovery, cheirality and scale ambiguity |  |
| SLAM backend | Explain false-loop rejection and SE(3)/Sim(3) |  |
| IMU | Derive propagation from specific force and angular velocity |  |
| VIO | Explain preintegration, bias, initialization and observability |  |
| Mobile | Explain timestamps, calibration and rolling shutter |  |
| Ownership | Identify personal contributions and a measured design decision |  |


### Evidence against each feedback point


| Feedback | Evidence to show |
| --- | --- |
| Mostly modified existing systems | Personal residuals, solvers, estimator components and controlled algorithm experiment |
| Limited Python | Tested package, data pipeline, numerical code and profiling report |
| Weak optimization | Pose refinement, BA, Schur elimination, pose graph and marginalization |
| Weak pose representation | Conventions, geometry code and checked derivatives |
| Limited VIO detail | Propagation, preintegration, bias, initialization and joint estimation |
| Mostly stereo | Camera-only monocular pipeline with explicit scale handling |
| No mobile experience | Recorder, timing analysis, calibration and phone experiments |
| Dated visual SLAM work | Recent implementations and a comparative research report |


## Progress tracker

The assistant maintains [the repository progress tracker](progress.md).

Use status values Not started, In progress, Repeat or Complete. A week is Complete only when its criterion passes. Evidence can be a report filename, experiment ID or repository commit.


## Experiment report template

The assistant keeps one main question per report and uses [the report template](../reports/TEMPLATE.md) for future experiments and [the Week 1 report](../reports/week01.md) now.


## Resource directory

Resource labels in the weekly assignments point here. Links were selected for the curriculum on 6 October 2026. Use the referenced topics rather than reading every book or repository cover to cover.

- **R1: [Python Tutorial](https://docs.python.org/3/tutorial/)** — Chapters 4–8 and 12; later use classes, iterators and generators as needed.
- **R2: [NumPy quickstart](https://numpy.org/doc/stable/user/quickstart.html)** — Arrays, broadcasting, shapes, indexing and linear algebra.
- **R3: [Ethan Eade Lie Groups for 2D and 3D Transformations](https://ethaneade.com/lie.pdf)** — SO(3), SE(3), exponential/log maps and derivatives.
- **R4: [Solà and colleagues A micro Lie theory for state estimation in robotics](https://arxiv.org/abs/1812.01537)** — Local perturbations, adjoints and Jacobian reference.
- **R5: [Factor Graphs and GTSAM](https://gtsam.org/tutorials/intro.html)** — Factors, variables, estimation and graph examples.
- **R6: [SciPy least_squares](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.least_squares.html)** — Reference solver, robust losses and Jacobian options.
- **R7: [Hartley and Zisserman Multiple View Geometry second edition](https://www.robots.ox.ac.uk/~vgg/hzbook/)** — Author page with contents and sample chapters; full book may require library access or purchase.
- **R8: [OpenCV camera calibration and 3D reconstruction](https://docs.opencv.org/4.x/d9/d0c/group__calib3d.html)** — Projection, essential matrices, triangulation and PnP.
- **R9: [ETH Autonomous Systems Lab datasets](https://projects.asl.ethz.ch/datasets/)** — Locate EuRoC and its documentation, calibration and ground truth.
- **R10: [OpenVINS discrete propagation](https://docs.openvins.com/propagation_discrete.html)** — Inertial state and uncertainty propagation.
- **R11: [Forster and colleagues On Manifold Preintegration](https://arxiv.org/abs/1512.02363)** — Preintegration, uncertainty, bias correction and visual–inertial estimation.
- **R12: [GTSAM PreintegratedImuMeasurements](https://borglab.github.io/gtsam/preintegratedimumeasurements/)** — Reference preintegrated measurements and API examples.
- **R13: [VINS Mono](https://github.com/HKUST-Aerial-Robotics/VINS-Mono)** — Reference estimator, initialization and linked paper.
- **R14: [OpenVINS first estimate Jacobians](https://docs.openvins.com/fej.html)** — Linearization and observability consistency.
- **R15: [Android SensorEvent](https://developer.android.com/reference/android/hardware/SensorEvent)** — Sensor measurements and timestamp semantics.
- **R16: [Android CaptureResult](https://developer.android.com/reference/android/hardware/camera2/CaptureResult)** — Capture timestamps, exposure and camera metadata.
- **R17: [Android CameraCharacteristics](https://developer.android.com/reference/android/hardware/camera2/CameraCharacteristics)** — Device capabilities and timestamp source.
- **R18: [Kalibr camera IMU calibration](https://github.com/ethz-asl/kalibr/wiki/camera-imu-calibration)** — Calibration procedure and assumptions.
- **R19: [ORB SLAM3](https://github.com/UZ-SLAMLab/ORB_SLAM3)** — Classical visual and visual–inertial SLAM architecture.
- **R20: [OpenVINS](https://docs.openvins.com/)** — Filtering architecture, derivations and reference code.
- **R21: [DPVO](https://github.com/princeton-vl/DPVO)** — Learned patch-based visual odometry and geometric estimation.
- **R22: [evo trajectory evaluation](https://github.com/MichaelGrupp/evo)** — Trajectory metrics, alignment and plots.

The curriculum is a personal learning plan. Synthetic tolerances, initial feature thresholds and weekly effort estimates are proposed engineering choices; they are not claims of universal algorithm performance.


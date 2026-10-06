# Frames, units, and array shapes

- `T_AB` maps coordinates from frame B into frame A.
- `p_A = R_AB @ p_B + t_AB`; `t_AB` is B's origin expressed in A.
- Individual mathematical points are column vectors. NumPy point batches store
  one point per row, shape `(N, 3)`. Derive the transpose needed for this layout.
- Camera pose is `T_WC`; projection first maps a world point into the camera
  using `inverse(T_WC)`.
- Distances: metres. Angles: radians. Time: seconds. Rotations are right-handed.
- Internal quaternions will use `wxyz` ordering.
- Future local pose increments are translation first `[delta_rho, delta_phi]`,
  with right updates `T <- T Exp(delta_xi)`.
- A position gets rotation and translation; a direction vector gets rotation only.

These are the conventions adopted by the curriculum. Later sensor interfaces
must explicitly convert units, coordinate frames, and quaternion ordering.

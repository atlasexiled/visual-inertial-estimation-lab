# Week 1: Python foundations

Goal: implement and explain three small numerical tasks. Budget about 12 hours;
take longer if needed. The scaffold is ready, but completing this setup does not
complete the week.

You implement and explain; the assistant writes and runs tests, maintains this
checklist, and documents progress. No test writing or Markdown editing is required
from you. Explanations can be given in conversation.

## First session: 60–90 minutes

1. Activate the environment using the root README. The assistant handles setup verification.
2. Open `src/vielab/foundations.py` and read the `load_measurements` contract.
3. Inspect `data/week01/measurements.csv`. Predict the shapes and contents of the
   two arrays that `load_measurements` should return.
4. Implement only `load_measurements`. Start with the valid file, then add checks
   for invalid input. The standard-library `csv` module is sufficient.
5. Ask the assistant to review your loader and run the tests. If you want immediate
   feedback yourself, optionally run `python -m pytest tests/test_week01.py -k load -q`.
6. Discuss any confusing behavior in chat; the assistant records the findings.

Read the Python tutorial chapters 4–8 and 12, listed as R1 in the curriculum:
functions, containers, modules, files, exceptions and virtual environments.
You need not finish all the reading before attempting the valid-file case.

## A. Timestamped CSV

Implement `load_measurements` using its docstring as the contract. Our small
fixture represents generic timestamped 3D measurements in metres, not real IMU
data. Return timestamps `(N,)` and measurements `(N, 3)` as float64 arrays.

Reject bad records with `ValueError`. A useful error message identifies the line
and problem. Do not repair ordering by sorting: out-of-order sensor measurements
should be visible to the caller. A final newline is normal; a blank data record
is invalid. No numeric timestamp may repeat.

Explain: Why are repeated or decreasing timestamps a problem for integration?
Why is shape `(N,)` different from `(N, 1)`?

## B. Transform 3D points

Read [the conventions](../../docs/conventions.md). Implement `transform_points`.
Use NumPy operations; derive the batch equation from the column-vector equation
in the docstring. Validate dimensions before relying on broadcasting.

Sanity check: rotating `[1, 0, 0]` by +90 degrees about z and then translating by
`[10, 20, 30]` should give `[10, 21, 30]`. A reflection is not a valid rotation,
even though its columns are orthonormal.

Ask for a review, or optionally run `python -m pytest tests/test_week01.py -k transform -q`.

Explain: In which frame is the translation expressed? Why does reversing the
operation order change the result? Does a direction vector get translated?

## C. Least squares

Implement `solve_least_squares`. Fit a line `y = slope * t + intercept` using
`t = [0, 1, 2, 3]`, `y = [1, 2, 2, 4]`, and design matrix columns `[t, 1]`.
The expected coefficients are `[0.9, 0.9]`. The residual is nonzero: the line
cannot pass through every observation. Check that `A.T @ (A @ x - b)` is near
zero; the least-squares residual is orthogonal to A's columns.

Use `np.linalg.lstsq(A, b, rcond=None)`. Inspect its returned rank rather than
discarding all outputs except the solution. Learn what rank means and why a
rank-deficient system does not identify a unique solution under this contract.

Ask for a review, or optionally run `python -m pytest tests/test_week01.py -k least_squares -q`.

Explain: Why avoid `inverse(A.T @ A) @ A.T @ b`? What do QR and SVD provide?

## Remaining weekly sessions

| Session | Work |
| --- | --- |
| Reading, 2 hours | Python topics above; dimensions, transpose, rank and null space |
| Implementation, 2 hours | CSV parsing and point transformation |
| Review and debugging, 2 hours | Discuss assistant-run checks for invalid data, rotations, dimensions, and least squares |
| Integration, 4 hours | Finish functions; investigate failures; review QR/SVD, derivatives, chain rule, covariance |
| Review, 2 hours | Reproduce functions in a fresh ignored `outputs/` file; explain aloud; assistant records findings |

## Completion checklist

Maintained by the assistant based on code review, test results, and conversation.

- [ ] Assistant verifies the implementation with passing tests.
- [ ] Discuss one edge case and understand the bug it could expose.
- [ ] Recreate all three tasks in a fresh file without copying or AI completion.
- [ ] Explain the input/output shapes and why explicit matrix inverses are avoided.
- [ ] Explain rank, covariance, and the chain rule with a small example each.
- [ ] Assistant records actual results and any observed failures in the Week 1 report.
- [ ] Assistant updates progress after the implementation and learning criteria are met.

If rank, covariance, or the chain rule remains unclear, use a prerequisite week
before moving to Week 2. Ask for a hint or a code review when needed; the core
function bodies are intentionally yours to write.

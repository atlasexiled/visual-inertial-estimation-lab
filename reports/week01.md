# Week 1 report

Maintained by the assistant from code review, observed runs, and conversation.
The learner is not expected to edit this file.

## Status

In progress. Learning criteria have not yet been verified.

## Objective and assumptions

Implement timestamped CSV validation, batched 3D point transformation, and
full-column-rank overdetermined least squares. Shapes, units, and input
restrictions are specified in the function docstrings and assignment.

## Verification recorded so far

- Setup checks: 2 passed in the most recent setup verification.
- Test discovery: all 45 tests collected after disabling unrelated ROS launch plugins.
- CSV loader current implementation: all 28 loader tests pass. Added checks
  covering irregular intervals, negative coordinates, a missing final newline,
  and invalid records after a valid first measurement. These verify that
  validation actually reaches the data rather than failing at the header.
- Point transformation, least squares, and independent understanding: pending review.

## CSV implementation review

The learner uses a file context manager, the standard CSV reader, separate
timestamp/value lists, and explicit float64 conversion. These establish the
intended basic loading structure.

The learner added separate header validation. At the learner's explicit request,
the assistant completed field-count checks, finite-number checks, nonnegative
and strictly increasing timestamp validation, and empty-data rejection. Header
handling now also permits surrounding whitespace and rejects empty files with
ValueError. Removed the unreachable placeholder exception. Validation errors
for data records identify the CSV line.

Implementation is verified against all 28 loader tests. Independent reproduction
and understanding remain unverified; this is an assisted implementation.

## Setup issue and resolution

Pytest loaded ROS launch-testing plugins through the shell's `PYTHONPATH` and
failed to import `yaml`. The project configuration now disables `launch_testing`
and `launch_ros`; setup checks and collection then succeeded.

## Discussion and learning evidence

Pending conversation about timestamp ordering, array shapes, coordinate frames,
rank, least squares, covariance, and the chain rule. The assistant will record
what is demonstrated without treating test results alone as evidence of mastery.

## Next step

Learner reads the completed loader when ready. Discuss any unclear checks before
moving to point transformations; no documentation or test writing is assigned
to the learner. Week 1 remains in progress.

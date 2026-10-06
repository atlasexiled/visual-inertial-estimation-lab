"""Week 1 exercises. Implement each function using its documented contract."""

import csv
from pathlib import Path

import numpy as np
from numpy.typing import ArrayLike, NDArray


def load_measurements(path: str | Path) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Read CSV columns timestamp_s,x,y,z, in exactly that order.

    Return float64 arrays with shapes (N,) and (N, 3), with N >= 1.
    Timestamps must be finite, nonnegative and strictly increasing. Values
    must be finite. Reject wrong headers, missing/extra columns, nonnumeric
    entries, blank records and empty data with ValueError. Never sort or
    silently discard invalid records. Surrounding field whitespace is allowed.
    Preserve ordinary file errors such as FileNotFoundError.
    """

    timestamps: list[float] = []
    values: list[list[float]] = []

    with open(path, newline="") as file:
        data = csv.reader(file)

        # Read the header separately; an empty file has no first record.
        header = next(data, None)
        if header is None:
            raise ValueError("CSV file is empty")
        if [field.strip() for field in header] != ["timestamp_s", "x", "y", "z"]:
            raise ValueError("Invalid CSV header")

        for row in data:
            line = data.line_num
            # Check before indexing: slices silently accept too few fields.
            if len(row) != 4:
                raise ValueError(f"Line {line}: expected exactly four fields")

            try:
                timestamp = float(row[0])
                values_row = [float(x) for x in row[1:4]]
            except ValueError as error:
                raise ValueError(f"Line {line}: all fields must be numeric") from error

            # float() accepts NaN and infinity, so conversion is not enough.
            if not np.isfinite(timestamp) or not np.all(np.isfinite(values_row)):
                raise ValueError(f"Line {line}: all fields must be finite")
            if timestamp < 0:
                raise ValueError(f"Line {line}: timestamp must be nonnegative")
            if timestamps and timestamp <= timestamps[-1]:
                raise ValueError(f"Line {line}: timestamps must be strictly increasing")

            # Append only after every check passes, preserving row alignment.
            timestamps.append(timestamp)
            values.append(values_row)

    if not timestamps:
        raise ValueError("CSV must contain at least one measurement")

    return np.array(timestamps, dtype=np.float64), np.array(values, dtype=np.float64)


def transform_points(points_b: ArrayLike, rotation_ab: ArrayLike, translation_ab: ArrayLike) -> NDArray[np.float64]:
    """Map points from frame B to frame A: p_A = R_AB @ p_B + t_AB.

    Accept finite numeric array-like inputs with shapes (N, 3), (3, 3),
    and (3,). Return float64 shape (N, 3); an empty (0, 3) batch is valid.
    Each input row stores one point, although the equation uses column vectors.
    Do not mutate inputs. Reject wrong shapes or nonfinite entries with
    ValueError. Require R.T @ R approximately I and det(R) approximately +1,
    using absolute tolerance 1e-10 and relative tolerance zero.
    """
    raise NotImplementedError("Week 1B: implement batched point transformation")


def solve_least_squares(a: ArrayLike, b: ArrayLike) -> NDArray[np.float64]:
    """Minimize ||A x - b||_2 for a full-column-rank overdetermined system.

    Accept finite numeric array-like inputs A of shape (M, N), b of shape
    (M,), with M > N >= 1. Return float64 shape (N,). Do not mutate inputs.
    Reject invalid shapes, nonfinite entries, or rank < N with ValueError.
    Use np.linalg.lstsq with rcond=None; use its reported rank to detect
    rank deficiency. Do not explicitly form an inverse or normal equations.
    """
    raise NotImplementedError("Week 1C: implement validated least squares")

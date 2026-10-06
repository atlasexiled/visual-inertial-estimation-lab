"""Setup checks independent of unfinished learner implementations."""

from pathlib import Path

import numpy as np

from vielab import foundations


def test_import_and_numpy():
    assert callable(foundations.load_measurements)
    assert callable(foundations.transform_points)
    assert callable(foundations.solve_least_squares)
    np.testing.assert_array_equal(np.eye(3) @ [1, 2, 3], [1, 2, 3])


def test_fixture_exists():
    path = Path(__file__).resolve().parents[1] / "data/week01/measurements.csv"
    assert path.read_text().splitlines()[0] == "timestamp_s,x,y,z"

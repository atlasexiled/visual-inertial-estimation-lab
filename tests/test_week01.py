"""Acceptance tests: initially fail until you implement the three exercises."""

from pathlib import Path

import numpy as np
import pytest
from numpy.testing import assert_allclose, assert_array_equal

from vielab.foundations import load_measurements, solve_least_squares, transform_points


def test_load_fixture():
    path = Path(__file__).resolve().parents[1] / "data/week01/measurements.csv"
    times, values = load_measurements(path)
    assert times.shape == (4,)
    assert values.shape == (4, 3)
    assert times.dtype == values.dtype == np.dtype("float64")
    assert_allclose(times, [0, 0.01, 0.02, 0.03])
    assert_allclose(values, [[1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 2, 3]])


def test_load_single_row_and_whitespace(tmp_path):
    path = tmp_path / "single.csv"
    path.write_text(" timestamp_s , x , y , z \n 0.1 , 1 , -2 , 3 \n")
    times, values = load_measurements(str(path))
    assert times.shape == (1,)
    assert values.shape == (1, 3)
    assert_allclose(values, [[1, -2, 3]])


@pytest.mark.parametrize("content", [
    "", "timestamp_s,x,y,z\n", "time,x,y,z\n0,1,2,3\n",
    "timestamp_s,y,x,z\n0,1,2,3\n", "timestamp_s,x,y,z\n0,1,2\n",
    "timestamp_s,x,y,z\n0,1,2,3,4\n", "timestamp_s,x,y,z\n0,bad,2,3\n",
    "timestamp_s,x,y,z\n0,,2,3\n", "timestamp_s,x,y,z\n0,nan,2,3\n",
    "timestamp_s,x,y,z\n0,1,inf,3\n", "timestamp_s,x,y,z\nnan,1,2,3\n",
    "timestamp_s,x,y,z\ninf,1,2,3\n", "timestamp_s,x,y,z\n-1,1,2,3\n",
    "timestamp_s,x,y,z\n0,1,2,3\n0,4,5,6\n",
    "timestamp_s,x,y,z\n1,1,2,3\n0,4,5,6\n",
    "timestamp_s,x,y,z\n0,1,2,3\n\n",
])
def test_load_rejects_invalid_records(tmp_path, content):
    path = tmp_path / "bad.csv"
    path.write_text(content)
    with pytest.raises(ValueError):
        load_measurements(path)


def test_load_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_measurements(tmp_path / "missing.csv")


def test_load_irregular_intervals_and_negative_coordinates(tmp_path):
    path = tmp_path / "irregular.csv"
    path.write_text("timestamp_s,x,y,z\n0,-1,2,3\n0.01,4,-5,6\n0.025,7,8,-9")
    times, values = load_measurements(path)
    assert_allclose(times, [0, 0.01, 0.025])
    assert_allclose(values, [[-1, 2, 3], [4, -5, 6], [7, 8, -9]])


@pytest.mark.parametrize("bad_row", [
    "", "1,2,3", "1,2,3,4,5", "1,2,bad,4", "1,2,3,-inf",
    "1,2,3,1e309", "0,2,3,4", "-0.1,2,3,4",
])
def test_load_rejects_bad_record_after_valid_record(tmp_path, bad_row):
    path = tmp_path / "later_error.csv"
    path.write_text(f"timestamp_s,x,y,z\n0,1,2,3\n{bad_row}\n")
    with pytest.raises(ValueError, match="Line 3:"):
        load_measurements(path)


def test_transform_known_rotation_translation():
    # +90 degrees about z, with a nonzero translation to expose order mistakes.
    rotation = [[0, -1, 0], [1, 0, 0], [0, 0, 1]]
    actual = transform_points([[1, 0, 0], [0, 1, 0]], rotation, [10, 20, 30])
    assert actual.shape == (2, 3)
    assert actual.dtype == np.dtype("float64")
    assert_allclose(actual, [[10, 21, 30], [9, 20, 30]], atol=1e-12, rtol=0)


def test_transform_identity_empty_and_no_mutation():
    points = np.array([[1., 2., 3.], [-4., 5., 6.]])
    rotation, translation = np.eye(3), np.zeros(3)
    originals = [x.copy() for x in (points, rotation, translation)]
    assert_array_equal(transform_points(points, rotation, translation), points)
    for actual, original in zip((points, rotation, translation), originals):
        assert_array_equal(actual, original)
    assert transform_points(np.empty((0, 3)), rotation, translation).shape == (0, 3)


def test_transform_inverse_round_trip():
    rotation = np.array([[0., 0., 1.], [0., 1., 0.], [-1., 0., 0.]])
    translation = np.array([2., -3., 4.])
    points = np.random.default_rng(7).normal(size=(8, 3))
    mapped = transform_points(points, rotation, translation)
    recovered = transform_points(mapped, rotation.T, -rotation.T @ translation)
    assert_allclose(recovered, points, atol=1e-12, rtol=0)


@pytest.mark.parametrize("points,rotation,translation", [
    ([1, 2, 3], np.eye(3), [0, 0, 0]),
    ([[1, 2]], np.eye(3), [0, 0, 0]),
    ([[1, 2, 3]], np.eye(2), [0, 0, 0]),
    ([[1, 2, 3]], np.eye(3), [[0], [0], [0]]),
    ([[1, 2, 3]], np.eye(3), [0, 0]),
    ([[1, 2, 3]], np.diag([1, 1, -1]), [0, 0, 0]),
    ([[1, 2, 3]], 2 * np.eye(3), [0, 0, 0]),
    ([[1, 2, np.nan]], np.eye(3), [0, 0, 0]),
    ([[1, 2, 3]], np.eye(3), [0, np.inf, 0]),
    ([[1, 2, 3]], np.full((3, 3), np.nan), [0, 0, 0]),
])
def test_transform_invalid_inputs(points, rotation, translation):
    with pytest.raises(ValueError):
        transform_points(points, rotation, translation)


def test_least_squares_exact_and_no_mutation():
    a = np.array([[1., 0.], [0., 1.], [1., 1.], [2., -1.]])
    b = a @ np.array([2., -3.])
    a_before, b_before = a.copy(), b.copy()
    result = solve_least_squares(a, b)
    assert result.shape == (2,)
    assert result.dtype == np.dtype("float64")
    assert_allclose(result, [2, -3], atol=1e-12, rtol=0)
    assert_array_equal(a, a_before)
    assert_array_equal(b, b_before)


def test_least_squares_inconsistent_data():
    a = np.column_stack((np.arange(4), np.ones(4)))
    b = np.array([1., 2., 2., 4.])
    result = solve_least_squares(a.tolist(), b.tolist())
    assert_allclose(result, [0.9, 0.9], atol=1e-12, rtol=0)
    residual = a @ result - b
    assert np.linalg.norm(residual) > 0.1
    assert_allclose(a.T @ residual, [0, 0], atol=1e-12, rtol=0)


@pytest.mark.parametrize("a,b", [
    ([[1, 2], [2, 4], [3, 6]], [1, 2, 3]),  # rank deficient
    (np.eye(2), [1, 2]),  # square, outside this exercise's contract
    ([[1, 2, 3], [4, 5, 6]], [1, 2]),  # underdetermined
    ([[1], [2], [3]], [1, 2]),
    ([[1], [2], [3]], [[1], [2], [3]]),
    ([1, 2, 3], [1, 2, 3]),
    (np.empty((3, 0)), [1, 2, 3]),
    ([[1], [np.nan]], [1, 2]),
    ([[1], [2]], [1, np.inf]),
])
def test_least_squares_invalid_inputs(a, b):
    with pytest.raises(ValueError):
        solve_least_squares(a, b)

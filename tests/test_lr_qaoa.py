"""Tests for :class:`LRQAOA`."""

from typing import Any

import numpy as np
import pytest

from qrisp_optimization import LRQAOA, QAOARequirements
from qrisp_optimization.problems import MaxCutProblem

from helpers import binary_qarg_factory


class RecordingProblem(QAOARequirements[Any]):
    """Problem that records the order and angles of the applied layers."""

    def __init__(self) -> None:
        self.calls: list[tuple[str, float | None]] = []

    def cl_cost_function(self, x: Any) -> float:  # noqa: ANN401
        return 0.0

    def state_prep(self, qarg: Any) -> Any:  # noqa: ANN401
        self.calls.append(("prep", None))
        return qarg

    def cost_layer(self, qarg: Any, gamma: float) -> Any:  # noqa: ANN401
        self.calls.append(("cost", gamma))
        return qarg

    def mixer_layer(self, qarg: Any, beta: float) -> Any:  # noqa: ANN401
        self.calls.append(("mixer", beta))
        return qarg


# linear_ramp

@pytest.mark.parametrize(
    ("start", "stop", "steps", "expected"),
    [
        (0.0, 1.0, 5, [0.0, 0.25, 0.5, 0.75, 1.0]),
        (2.0, 0.0, 3, [2.0, 1.0, 0.0]),
        (0.5, 0.5, 2, [0.5, 0.5]),
        (0.3, 1.0, 1, [0.3]),
        (0.0, 1.0, 0, []),
    ],
)
def test_linear_ramp_is_evenly_spaced(
    start: float, stop: float, steps: int, expected: list[float],
) -> None:
    algorithm = LRQAOA(RecordingProblem(), qarg=object)

    np.testing.assert_allclose(algorithm.linear_ramp(start, stop, steps), expected)


# ansatz

def test_ansatz_ramps_gamma_up_and_beta_magnitude_down() -> None:
    problem = RecordingProblem()
    LRQAOA(problem, qarg=object).ansatz(depth=3, d_gamma=0.6, d_beta=0.4)

    # mixer angles are negated, see LRQAOA.ansatz
    assert problem.calls == pytest.approx([
        ("prep", None),
        ("cost", 0.0), ("mixer", -0.4),
        ("cost", 0.3), ("mixer", -0.2),
        ("cost", 0.6), ("mixer", 0.0),
    ])


def test_ansatz_returns_the_qarg_created_by_the_factory() -> None:
    qarg = object()

    assert LRQAOA(RecordingProblem(), qarg=lambda: qarg).ansatz(2, 0.6, 0.4) is qarg


def test_ansatz_builds_on_a_fresh_qarg_each_call(maxcut: MaxCutProblem) -> None:
    algorithm = LRQAOA(maxcut, binary_qarg_factory(maxcut.n))

    first = algorithm.ansatz(depth=3, d_gamma=0.6, d_beta=0.6)
    second = algorithm.ansatz(depth=3, d_gamma=0.6, d_beta=0.6)

    assert first is not second
    assert first.get_measurement() == pytest.approx(second.get_measurement())


def test_ansatz_produces_normalized_distribution_on_maxcut(maxcut: MaxCutProblem) -> None:
    algorithm = LRQAOA(maxcut, binary_qarg_factory(maxcut.n))

    meas = algorithm.ansatz(depth=3, d_gamma=0.6, d_beta=0.6).get_measurement()

    assert sum(meas.values()) == pytest.approx(1.0)


def test_ansatz_beats_random_guessing_on_maxcut(maxcut: MaxCutProblem) -> None:
    algorithm = LRQAOA(maxcut, binary_qarg_factory(maxcut.n))

    meas = algorithm.ansatz(depth=8, d_gamma=0.6, d_beta=0.6).get_measurement()

    expectation = sum(p * maxcut.cl_cost_function(x) for x, p in meas.items())
    mean_cost = np.mean([maxcut.cl_cost_function(x) for x in maxcut.next()])
    assert expectation < mean_cost

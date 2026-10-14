"""Tests for :class:`QAOA`."""

from typing import Any

import numpy as np
import pytest

from qrisp_optimization import QAOA, Bruteforce, QAOARequirements
from qrisp_optimization.metrics import exp_val
from qrisp_optimization.problems import MaxCutProblem, QUBOProblem

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


# ansatz


def test_ansatz_applies_prep_then_alternating_layers() -> None:
    problem = RecordingProblem()
    # theta = [beta_1, beta_2, gamma_1, gamma_2]
    QAOA(problem, qarg=object).ansatz(np.array([0.1, 0.2, 0.3, 0.4]))

    assert problem.calls == [
        ("prep", None),
        ("cost", 0.3),
        ("mixer", 0.1),
        ("cost", 0.4),
        ("mixer", 0.2),
    ]


def test_ansatz_with_empty_theta_only_prepares_state() -> None:
    problem = RecordingProblem()
    QAOA(problem, qarg=object).ansatz(np.array([]))

    assert problem.calls == [("prep", None)]


def test_ansatz_builds_on_a_fresh_qarg_each_call(maxcut: MaxCutProblem) -> None:
    algorithm = QAOA(maxcut, binary_qarg_factory(maxcut.n))
    theta = np.array([0.3, 0.7])

    first = algorithm.ansatz(theta)
    second = algorithm.ansatz(theta)

    assert first is not second
    assert first.get_measurement() == pytest.approx(second.get_measurement())


def test_ansatz_with_zero_angles_is_uniform(maxcut: MaxCutProblem) -> None:
    meas = QAOA(maxcut, binary_qarg_factory(maxcut.n)).ansatz(np.zeros(4)).get_measurement()

    assert len(meas) == 2**maxcut.n
    assert all(p == pytest.approx(2**-maxcut.n) for p in meas.values())


# optimize


def test_optimize_returns_angles_of_same_shape(maxcut: MaxCutProblem) -> None:
    theta = QAOA(maxcut, binary_qarg_factory(maxcut.n)).optimize(np.full(4, 0.5), max_iter=6)

    assert isinstance(theta, np.ndarray)
    assert theta.shape == (4,)


@pytest.mark.parametrize("problem_name", ["qubo", "maxcut"])
def test_optimize_lowers_expectation_and_favours_optimum(
    request: pytest.FixtureRequest,
    problem_name: str,
) -> None:
    problem: QUBOProblem | MaxCutProblem = request.getfixturevalue(problem_name)
    algorithm = QAOA(problem, binary_qarg_factory(problem.n))
    theta0 = np.full(4, 0.5)

    theta = algorithm.optimize(theta0)

    assert exp_val(algorithm.ansatz(theta), problem) < exp_val(algorithm.ansatz(theta0), problem)
    optimal = {tuple(x) for x in Bruteforce(problem).solve()}
    meas = algorithm.ansatz(theta).get_measurement()
    p_optimal = sum(p for x, p in meas.items() if tuple(x) in optimal)
    assert p_optimal > len(optimal) / 2**problem.n  # better than random guessing


def test_optimize_uses_custom_metric(maxcut: MaxCutProblem) -> None:
    calls: list[tuple[Any, Any]] = []

    def metric(qarg: Any, problem: Any) -> float:  # noqa: ANN401
        calls.append((qarg, problem))
        return 0.0

    QAOA(maxcut, binary_qarg_factory(maxcut.n)).optimize(np.full(2, 0.5), metric=metric, max_iter=4)

    assert calls
    assert all(problem is maxcut for _, problem in calls)


def test_optimize_minimizes_the_metric() -> None:
    target = np.array([0.3, -0.2, 1.1, 0.4])

    def metric(qarg: Any, problem: Any) -> float:  # noqa: ANN401
        return float(np.sum((qarg - target) ** 2))

    # identity "ansatz": the qarg handed to the metric is theta itself
    algorithm = QAOA(RecordingProblem(), qarg=object)
    algorithm.ansatz = lambda theta: theta  # type: ignore[method-assign]

    theta = algorithm.optimize(np.zeros(4), metric=metric, max_iter=500)

    np.testing.assert_allclose(theta, target, atol=1e-3)


def test_optimize_respects_max_iter(maxcut: MaxCutProblem) -> None:
    evaluations = 0

    def metric(qarg: Any, problem: Any) -> float:  # noqa: ANN401
        nonlocal evaluations
        evaluations += 1
        return float(evaluations)

    QAOA(maxcut, binary_qarg_factory(maxcut.n)).optimize(np.full(2, 0.5), metric=metric, max_iter=7)

    assert evaluations <= 7


def test_optimize_options_override_max_iter(maxcut: MaxCutProblem) -> None:
    evaluations = 0

    def metric(qarg: Any, problem: Any) -> float:  # noqa: ANN401
        nonlocal evaluations
        evaluations += 1
        return float(evaluations)

    QAOA(maxcut, binary_qarg_factory(maxcut.n)).optimize(
        np.full(2, 0.5),
        metric=metric,
        max_iter=50,
        options={"maxiter": 4},
    )

    assert evaluations <= 4


def test_optimize_with_other_scipy_method(maxcut: MaxCutProblem) -> None:
    theta = QAOA(maxcut, binary_qarg_factory(maxcut.n)).optimize(
        np.full(2, 0.5),
        method="Nelder-Mead",
        max_iter=5,
    )

    assert theta.shape == (2,)

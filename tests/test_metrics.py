"""Tests for :mod:`qrisp_optimization.metrics`."""

import numpy as np
import pytest

from qrisp_optimization.metrics import exp_val
from qrisp_optimization.problems import MaxCutProblem

from helpers import binary_qarg_factory


class FakeQarg:
    """Stand-in for a quantum argument with a fixed measurement distribution."""

    def __init__(self, meas: dict[tuple[int, ...], float]) -> None:
        self.meas = meas

    def get_measurement(self) -> dict[tuple[int, ...], float]:
        return self.meas


def test_exp_val_weights_costs_by_probability(maxcut: MaxCutProblem) -> None:
    # costs: 0, -4 and -2
    qarg = FakeQarg({(0, 0, 0, 0): 0.5, (0, 1, 0, 1): 0.25, (1, 0, 0, 0): 0.25})

    assert exp_val(qarg, maxcut) == pytest.approx(0.5 * 0 + 0.25 * -4 + 0.25 * -2)


def test_exp_val_of_deterministic_outcome_is_its_cost(maxcut: MaxCutProblem) -> None:
    assert exp_val(FakeQarg({(1, 0, 1, 0): 1.0}), maxcut) == pytest.approx(-4.0)


def test_exp_val_returns_float(maxcut: MaxCutProblem) -> None:
    assert isinstance(exp_val(FakeQarg({(1, 0, 1, 0): 1.0}), maxcut), float)


def test_exp_val_on_uniform_superposition_is_mean_cost(maxcut: MaxCutProblem) -> None:
    qarg = binary_qarg_factory(maxcut.n)()
    maxcut.state_prep(qarg)

    mean_cost = np.mean([maxcut.cl_cost_function(x) for x in maxcut.next()])

    assert exp_val(qarg, maxcut) == pytest.approx(mean_cost, abs=1e-6)

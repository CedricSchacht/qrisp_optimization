"""Tests for :class:`Bruteforce`."""

from collections.abc import Generator

import numpy as np
import pytest
from numpy.typing import NDArray

from qrisp_optimization import Bruteforce, BruteforceRequirements
from qrisp_optimization.problems import MaxCutProblem, QUBOProblem

from helpers import all_assignments


class TableProblem(BruteforceRequirements[NDArray[np.int_]]):
    """Problem whose candidates and costs are given as an explicit table."""

    def __init__(self, costs: list[float]) -> None:
        self.costs = costs

    def cl_cost_function(self, x: NDArray[np.int_]) -> float:
        return self.costs[int(x[0])]

    def next(self) -> Generator[NDArray[np.int_]]:
        for i in range(len(self.costs)):
            yield np.array([i])


def solve(costs: list[float], tol: float = 1e-8) -> list[int]:
    return [int(x[0]) for x in Bruteforce(TableProblem(costs), tol=tol).solve()]


def test_returns_unique_minimum() -> None:
    assert solve([3.0, -1.0, 2.0, 0.0]) == [1]


def test_returns_all_ties_in_enumeration_order() -> None:
    assert solve([0.0, -2.0, 5.0, -2.0, -2.0]) == [1, 3, 4]


def test_later_better_candidate_discards_earlier_ties() -> None:
    assert solve([-1.0, -1.0, -3.0]) == [2]


def test_costs_within_tolerance_count_as_ties() -> None:
    assert solve([-1.0, -1.0 + 1e-10, -1.0 - 1e-10]) == [0, 1, 2]


def test_costs_outside_tolerance_are_distinct() -> None:
    assert solve([-1.0, -1.05], tol=0.01) == [1]
    assert solve([-1.0, -1.05], tol=0.1) == [0, 1]


def test_single_candidate() -> None:
    assert solve([7.0]) == [0]


def test_qubo_matches_exhaustive_minimum(qubo: QUBOProblem) -> None:
    costs = {tuple(x): qubo.cl_cost_function(x) for x in all_assignments(qubo.n)}
    best = min(costs.values())

    solutions = Bruteforce(qubo).solve()

    assert sorted(tuple(x) for x in solutions) == sorted(k for k, c in costs.items() if c == best)


def test_maxcut_finds_both_alternating_cuts_of_a_square(maxcut: MaxCutProblem) -> None:
    solutions = Bruteforce(maxcut).solve()

    assert [x.tolist() for x in solutions] == [[0, 1, 0, 1], [1, 0, 1, 0]]
    assert maxcut.cl_cost_function(solutions[0]) == pytest.approx(-4.0)

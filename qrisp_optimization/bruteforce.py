"""Exhaustive-search solver used as a classical reference."""

from typing import TypeVar

import numpy as np
from numpy.typing import NDArray

from qrisp_optimization.bruteforce_requirements import BruteforceRequirements

T = TypeVar("T", bound=NDArray[np.generic])

class Bruteforce[T: NDArray[np.generic]]:
    """Find all optimal solutions of a problem by evaluating every candidate.

    Parameters
    ----------
    problem : BruteforceRequirements[T]
        Problem providing a candidate enumerator and a classical cost function.
    tol : float, optional
        Absolute tolerance under which two costs are considered equal.
        Default is ``1e-8``.
    """

    def __init__(self, problem: BruteforceRequirements[T], tol: float = 1e-8) -> None:
        self.problem: BruteforceRequirements[T] = problem
        self.tol = tol

    def solve(self) -> list[T]:
        """Enumerate all candidates and return those with minimal cost.

        Returns
        -------
        list[T]
            All candidates whose cost lies within ``tol`` of the minimum,
            in the order produced by ``problem.next()``.
        """
        best_cost = np.inf
        best_solutions: list[T] = []

        for x in self.problem.next():
            cost = self.problem.cl_cost_function(x)

            if best_cost == np.inf or cost < best_cost - self.tol:
                best_cost = cost
                best_solutions = [x]
            elif np.isclose(cost, best_cost, atol=self.tol, rtol=0.0):
                best_solutions.append(x)

        return best_solutions

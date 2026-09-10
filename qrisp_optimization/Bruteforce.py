from typing import Generic, TypeVar, List
import numpy as np
from numpy.typing import NDArray
from qrisp_optimization.Bruteforce_Requirements import Bruteforce_Requirements

T = TypeVar("T", bound=NDArray[np.generic])

class Bruteforce(Generic[T]):
    def __init__(self, problem: Bruteforce_Requirements[T], tol: float = 1e-8):
        self.problem: Bruteforce_Requirements[T] = problem
        self.tol = tol

    def solve(self) -> List[T]:
        best_cost = np.inf
        best_solutions: List[T] = []

        for x in self.problem.next():
            cost = self.problem.cl_cost_function(x)

            # use == for np.inf, not "is"
            if best_cost == np.inf or cost < best_cost - self.tol:
                best_cost = cost
                best_solutions = [x]
            elif np.isclose(cost, best_cost, atol=self.tol, rtol=0.0):
                best_solutions.append(x)

        return best_solutions
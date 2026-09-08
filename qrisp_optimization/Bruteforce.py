import numpy as np
from qrisp_optimization.Bruteforce_Requirements import Bruteforce_Requirements

class Bruteforce:
    def __init__(self, problem: Bruteforce_Requirements):
        self.problem: Bruteforce_Requirements = problem

    def solve(self) -> list[np.ndarray]:
        best_cost = float("inf")
        best_solutions: list[np.ndarray] = []

        while True:
            x = self.problem.next()
            if x is None:
                break

            cost = self.problem.cl_cost_function(x)

            if cost < best_cost:
                best_cost = cost
                best_solutions = [x]
            elif cost == best_cost:
                best_solutions.append(x)

        return best_solutions
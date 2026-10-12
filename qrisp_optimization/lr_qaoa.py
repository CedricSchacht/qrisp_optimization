import numpy as np
from qrisp import QuantumArray, QuantumVariable

from qrisp_optimization.qaoa_requirements import QAOARequirements


class LRQAOA[T]:
    def __init__(self, problem: QAOARequirements[T], qarg: QuantumVariable | QuantumArray) -> None:
        self.problem: QAOARequirements[T] = problem
        self.qarg: QuantumVariable | QuantumArray = qarg

    def linear_ramp(self, start: float, stop: float, steps: int) -> np.ndarray:
        raise NotImplementedError()

    def ansatz(
        self,
        depth: int,
        d_gamma: float,
        d_beta: float,
    ) -> QuantumVariable | QuantumArray:

        gammas = self.linear_ramp(0.0, d_gamma, depth)
        betas = self.linear_ramp(d_beta, 0.0, depth)

        self.problem.state_prep(self.qarg)
        for gamma, beta in zip(gammas, betas, strict=False):
            self.problem.cost_layer(self.qarg, gamma)
            self.problem.mixer_layer(self.qarg, beta)

        return self.qarg

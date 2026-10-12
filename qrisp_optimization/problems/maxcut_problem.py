import numpy as np
from numpy.typing import NDArray
from qrisp import QuantumArray

from qrisp_optimization.qaoa_requirements import QAOARequirements

type BinaryIntArray = NDArray[np.int_]

class MaxCutProblem(QAOARequirements[BinaryIntArray]):
    def __init__(self, Q: NDArray[np.float32]) -> None:  # noqa: N803
        print("This is currently just a dummy class without correct implementation")
        self.Q = Q
        self.n = Q.shape[0]

    # needed for QAOA
    def cl_cost_function(self, x: BinaryIntArray) -> float:
        return float(x.T @ self.Q @ x)

    # needed for QAOA
    def state_prep(self, qarg: QuantumArray) -> QuantumArray:
        return qarg

    # needed for QAOA
    def cost_layer(self, qarg: QuantumArray, gamma: float) -> QuantumArray:
        return qarg

    # needed for QAOA
    def mixer_layer(self, qarg: QuantumArray, beta: float) -> QuantumArray:
        return qarg

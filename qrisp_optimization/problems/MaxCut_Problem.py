from typing import Generator
from typing import Self
from numpy.typing import NDArray
import numpy as np

from qrisp_optimization.QAOA_Requirements import QAOA_Requirements
from qrisp import QuantumArray


class MaxCut_Problem(QAOA_Requirements):
    def __init__(self, Q: NDArray[np.float_]):
        print("This is currently just a dummy class without correct implementation")
        self.Q = Q
        self.n = Q.shape[0]

    # needed for QAOA
    def cl_cost_function(self, x: NDArray[np.int_]) -> float:
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
from qrisp_optimization.QAOA_Requirements import QAOA_Requirements
from qrisp_optimization.Bruteforce_Requirements import Bruteforce_Requirements
from qrisp.qaoa import RX_mixer
from qrisp import h, QuantumArray
import numpy as np
import networkx as nx

class QUBO_Problem(QAOA_Requirements, Bruteforce_Requirements):
    def __init__(self, Q: np.ndarray):
        self.Q = Q
        self.n = Q.shape[0]
        self._current = None 

    @staticmethod
    def from_networkx(G: nx.Graph) -> Self:
        # TODO
        ...

    # needed for QAOA and Brutefroce
    def cl_cost_function(self, x: np.ndarray) -> float:
        return float(x.T @ self.Q @ x)

    # needed for Bruteforce only
    def next(self) -> np.ndarray:
        if self._current is None:
            self._current = np.zeros(self.n, dtype=int)
            return self._current.copy()

        i = self.n - 1
        while i >= 0:
            if self._current[i] == 0:
                self._current[i] = 1
                self._current[i+1:] = 0
                return self._current.copy()
            i -= 1

        return None

    # needed for QAOA only
    def state_prep(self, qarg: QuantumArray) -> QuantumArray:
        for qv in qarg:
            h(qv)
        return qarg

    # needed for QAOA only
    def cost_layer(self, qarg: QuantumArray, gamma: float) -> QuantumArray:
        # TODO ...
        return qarg

    # needed for QAOA only
    def mixer_layer(self, qarg: QuantumArray, beta: float) -> QuantumArray:
        for qv in qarg:
            RX_mixer(qv, beta)
        return qarg
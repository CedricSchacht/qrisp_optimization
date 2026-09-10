from typing import Generator
from typing import Self
from numpy.typing import NDArray
import numpy as np
import networkx as nx

from qrisp_optimization.QAOA_Requirements import QAOA_Requirements
from qrisp_optimization.Bruteforce_Requirements import Bruteforce_Requirements
from qrisp.qaoa import RX_mixer, create_QUBO_cost_operator
from qrisp import h, QuantumArray


class QUBO_Problem(QAOA_Requirements, Bruteforce_Requirements[NDArray[np.int_]]):
    def __init__(self, Q: NDArray[np.float_]):
        self.Q = Q
        self.n = Q.shape[0]

    # alternative constructor
    @staticmethod
    def from_networkx(G: nx.Graph) -> Self:
        # TODO: build Q from G and return QUBO_Problem(Q)
        ...

    # needed for QAOA and Bruteforce
    def cl_cost_function(self, x: NDArray[np.int_]) -> float:
        return float(x.T @ self.Q @ x)

    # needed for Bruteforce only
    def next(self) -> Generator[NDArray[np.int_], None, None]:
        def gen() -> NDArray[np.int_]:
            current = np.zeros(self.n, dtype=int)
            yield current.copy()

            i = self.n - 1
            while i >= 0:
                if current[i] == 0:
                    current[i] = 1
                    current[i+1:] = 0
                    yield current.copy()
                    i = self.n - 1
                else:
                    i -= 1

        return gen()

    # needed for QAOA only
    def state_prep(self, qarg: QuantumArray) -> QuantumArray:
        for qv in qarg:
            h(qv)
        return qarg

    # needed for QAOA only
    def cost_layer(self, qarg: QuantumArray, gamma: float) -> QuantumArray:
        cost_op = create_QUBO_cost_operator(self.Q) # when refactoring QRISP move the code here instead of alling the function
        cost_op(qarg, gamma)
        return qarg

    # needed for QAOA only
    def mixer_layer(self, qarg: QuantumArray, beta: float) -> QuantumArray:
        for qv in qarg:
            RX_mixer(qv, beta)
        return qarg
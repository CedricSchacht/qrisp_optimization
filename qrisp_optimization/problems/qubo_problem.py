from collections.abc import Generator

import networkx as nx
import numpy as np
from numpy.typing import NDArray
from qrisp import QuantumArray, h
from qrisp.qaoa import RX_mixer, create_QUBO_cost_operator

from qrisp_optimization.bruteforce_requirements import BruteforceRequirements
from qrisp_optimization.qaoa_requirements import QAOARequirements

type BinaryIntArray = NDArray[np.int_]

class QUBOProblem(
    QAOARequirements[BinaryIntArray],
    BruteforceRequirements[BinaryIntArray]
):
    def __init__(self, Q: NDArray[np.float32]) -> None:  # noqa: N803
        self.Q: NDArray[np.float32] = Q
        self.n: int = Q.shape[0]

    # alternative constructor
    @staticmethod
    def from_networkx[T](G: nx.Graph[T]) -> QUBOProblem:  # noqa: N803
        # TODO: build Q from G and return QUBO_Problem(Q)
        raise NotImplementedError()

    # needed for QAOA and Bruteforce
    def cl_cost_function(self, x: BinaryIntArray) -> float:
        return float(x.T @ self.Q @ x)

    # needed for Bruteforce only
    def next(self) -> Generator[BinaryIntArray]:
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

    # needed for QAOA only
    def state_prep(self, qarg: QuantumArray) -> QuantumArray:
        for qv in qarg:
            h(qv)
        return qarg

    # needed for QAOA only
    def cost_layer(self, qarg: QuantumArray, gamma: float) -> QuantumArray:
        # when refactoring QRISP move the code here instead of alling the function
        cost_op = create_QUBO_cost_operator(self.Q)
        cost_op(qarg, gamma)
        return qarg

    # needed for QAOA only
    def mixer_layer(self, qarg: QuantumArray, beta: float) -> QuantumArray:
        for qv in qarg:
            RX_mixer(qv, beta)
        return qarg

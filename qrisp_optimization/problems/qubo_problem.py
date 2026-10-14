"""Quadratic Unconstrained Binary Optimization (QUBO) problem."""

from collections.abc import Generator

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
    """QUBO problem ``min_x x^T Q x`` over binary vectors ``x``.

    Solvable by both QAOA-type solvers and :class:`Bruteforce`.

    Parameters
    ----------
    Q : NDArray[np.float32]
        Square ``n x n`` QUBO matrix.
    """

    def __init__(self, Q: NDArray[np.float32]) -> None:  # noqa: N803
        self.Q: NDArray[np.float32] = Q
        self.n: int = Q.shape[0]

    # needed for QAOA and Bruteforce
    def cl_cost_function(self, x: BinaryIntArray) -> float:
        """Evaluate the QUBO objective ``x^T Q x``.

        Parameters
        ----------
        x : BinaryIntArray
            Binary vector of length ``n``.

        Returns
        -------
        float
            Cost of ``x``.
        """
        return float(x.T @ self.Q @ x)

    # needed for Bruteforce only
    def next(self) -> Generator[BinaryIntArray]:
        """Enumerate all ``2**n`` binary vectors in lexicographic order.

        Yields
        ------
        BinaryIntArray
            A fresh copy of each binary vector of length ``n``, starting with
            all zeros and ending with all ones.
        """
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
        """Prepare the uniform superposition by applying Hadamard to every qubit.

        Parameters
        ----------
        qarg : QuantumArray
            Array of binary quantum variables, one per QUBO variable.

        Returns
        -------
        QuantumArray
            ``qarg`` in uniform superposition.
        """
        for qv in qarg:
            h(qv)
        return qarg

    # needed for QAOA only
    def cost_layer(self, qarg: QuantumArray, gamma: float) -> QuantumArray:
        """Apply the QUBO phase-separating operator ``exp(-i gamma H_Q)``.

        Parameters
        ----------
        qarg : QuantumArray
            Array of binary quantum variables, one per QUBO variable.
        gamma : float
            Cost-layer angle.

        Returns
        -------
        QuantumArray
            ``qarg`` after applying the cost layer.
        """
        # when refactoring QRISP move the code here instead of alling the function
        cost_op = create_QUBO_cost_operator(self.Q)
        cost_op(qarg, gamma)
        return qarg

    # needed for QAOA only
    def mixer_layer(self, qarg: QuantumArray, beta: float) -> QuantumArray:
        """Apply the transverse-field ``RX`` mixer to every qubit.

        Parameters
        ----------
        qarg : QuantumArray
            Array of binary quantum variables, one per QUBO variable.
        beta : float
            Mixer-layer angle.

        Returns
        -------
        QuantumArray
            ``qarg`` after applying the mixer layer.
        """
        for qv in qarg:
            RX_mixer(qv, beta)
        return qarg

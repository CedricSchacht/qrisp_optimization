"""MaxCut problem (placeholder implementation)."""

import numpy as np
from numpy.typing import NDArray
from qrisp import QuantumArray

from qrisp_optimization.qaoa_requirements import QAOARequirements

type BinaryIntArray = NDArray[np.int_]

class MaxCutProblem(QAOARequirements[BinaryIntArray]):
    """MaxCut problem for QAOA.

    This is currently a dummy class: the quantum layers are identity
    operations and the cost function is a QUBO placeholder.

    Parameters
    ----------
    Q : NDArray[np.float32]
        Square ``n x n`` matrix describing the problem.
    """

    def __init__(self, Q: NDArray[np.float32]) -> None:  # noqa: N803
        print("This is currently just a dummy class without correct implementation")
        self.Q = Q
        self.n = Q.shape[0]

    # needed for QAOA
    def cl_cost_function(self, x: BinaryIntArray) -> float:
        """Evaluate ``x^T Q x`` for a binary assignment.

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

    # needed for QAOA
    def state_prep(self, qarg: QuantumArray) -> QuantumArray:
        """Prepare the initial state (currently a no-op).

        Parameters
        ----------
        qarg : QuantumArray
            Quantum argument to prepare.

        Returns
        -------
        QuantumArray
            ``qarg`` unchanged.
        """
        return qarg

    # needed for QAOA
    def cost_layer(self, qarg: QuantumArray, gamma: float) -> QuantumArray:
        """Apply the cost layer (currently a no-op).

        Parameters
        ----------
        qarg : QuantumArray
            Quantum argument to act on.
        gamma : float
            Cost-layer angle.

        Returns
        -------
        QuantumArray
            ``qarg`` unchanged.
        """
        return qarg

    # needed for QAOA
    def mixer_layer(self, qarg: QuantumArray, beta: float) -> QuantumArray:
        """Apply the mixer layer (currently a no-op).

        Parameters
        ----------
        qarg : QuantumArray
            Quantum argument to act on.
        beta : float
            Mixer-layer angle.

        Returns
        -------
        QuantumArray
            ``qarg`` unchanged.
        """
        return qarg

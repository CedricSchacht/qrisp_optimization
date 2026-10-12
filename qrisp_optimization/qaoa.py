"""Standard Quantum Approximate Optimization Algorithm (QAOA)."""

import numpy as np
from qrisp import QuantumArray, QuantumVariable

from qrisp_optimization.qaoa_requirements import QAOARequirements


class QAOA[T]:
    """QAOA solver for any problem implementing :class:`QAOARequirements`.

    Parameters
    ----------
    problem : QAOARequirements[T]
        Problem providing state preparation, cost layer and mixer layer.
    qarg : QuantumVariable | QuantumArray
        Quantum argument on which the ansatz is built.
    """

    def __init__(self, problem: QAOARequirements[T], qarg: QuantumVariable | QuantumArray) -> None:
        self.problem: QAOARequirements[T] = problem
        self.qarg: QuantumVariable | QuantumArray = qarg

    def ansatz(
        self,
        theta: np.ndarray
    ) -> QuantumVariable | QuantumArray:
        """Build the depth-``p`` QAOA ansatz on ``qarg``.

        Applies the problem's state preparation followed by ``p`` alternating
        cost and mixer layers.

        Parameters
        ----------
        theta : np.ndarray
            Variational angles of length ``2 * p``. The first ``p`` entries are
            the mixer angles ``beta``, the last ``p`` entries are the cost
            angles ``gamma``.

        Returns
        -------
        QuantumVariable | QuantumArray
            ``qarg`` after applying the ansatz.
        """

        p = len(theta) // 2
        gammas, betas = theta[p:], theta[:p]

        self.problem.state_prep(self.qarg)
        for gamma, beta in zip(gammas, betas, strict=False):
            self.problem.cost_layer(self.qarg, gamma)
            self.problem.mixer_layer(self.qarg, beta)

        return self.qarg

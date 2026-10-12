"""Linear-Ramp QAOA (LR-QAOA), a parameter-free QAOA variant."""

import numpy as np
from qrisp import QuantumArray, QuantumVariable

from qrisp_optimization.qaoa_requirements import QAOARequirements


class LRQAOA[T]:
    """LR-QAOA solver for any problem implementing :class:`QAOARequirements`.

    Instead of optimizing the angles variationally, the cost angles ramp
    linearly up and the mixer angles ramp linearly down over the layers,
    mimicking an adiabatic schedule.

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

    def linear_ramp(self, start: float, stop: float, steps: int) -> np.ndarray:
        """Compute a linear schedule of angles.

        Not yet implemented.

        Parameters
        ----------
        start : float
            Value at the first layer.
        stop : float
            Value at the last layer.
        steps : int
            Number of layers.

        Returns
        -------
        np.ndarray
            Array of ``steps`` linearly spaced values from ``start`` to ``stop``.

        Raises
        ------
        NotImplementedError
            Always, until implemented.
        """
        raise NotImplementedError()

    def ansatz(
        self,
        depth: int,
        d_gamma: float,
        d_beta: float,
    ) -> QuantumVariable | QuantumArray:
        """Build the LR-QAOA ansatz on ``qarg``.

        Parameters
        ----------
        depth : int
            Number of QAOA layers ``p``.
        d_gamma : float
            Final cost angle; ``gamma`` ramps from ``0`` to ``d_gamma``.
        d_beta : float
            Initial mixer angle; ``beta`` ramps from ``d_beta`` to ``0``.

        Returns
        -------
        QuantumVariable | QuantumArray
            ``qarg`` after applying the ansatz.
        """

        gammas = self.linear_ramp(0.0, d_gamma, depth)
        betas = self.linear_ramp(d_beta, 0.0, depth)

        self.problem.state_prep(self.qarg)
        for gamma, beta in zip(gammas, betas, strict=False):
            self.problem.cost_layer(self.qarg, gamma)
            self.problem.mixer_layer(self.qarg, beta)

        return self.qarg

"""Linear-Ramp QAOA (LR-QAOA), a parameter-free QAOA variant."""

from collections.abc import Callable

import numpy as np
from qrisp import QuantumArray, QuantumVariable

from qrisp_optimization.qaoa_requirements import QAOARequirements


class LRQAOA[T]:
    """LR-QAOA solver for any problem implementing `QAOARequirements`.

    Instead of optimizing the angles variationally, the cost angles ramp
    linearly up and the mixer angles ramp linearly down over the layers,
    mimicking an adiabatic schedule.

    Parameters
    ----------
    problem : QAOARequirements[T]
        Problem providing state preparation, cost layer and mixer layer.
    qarg : Callable[[], QuantumVariable | QuantumArray]
        Factory creating a fresh quantum argument; every call to
        [`ansatz`][qrisp_optimization.LRQAOA.ansatz] builds on a new one.
    """

    def __init__(
        self, problem: QAOARequirements[T], qarg: Callable[[], QuantumVariable | QuantumArray]
    ) -> None:
        self.problem: QAOARequirements[T] = problem
        self.qarg: Callable[[], QuantumVariable | QuantumArray] = qarg

    def linear_ramp(self, start: float, stop: float, steps: int) -> np.ndarray:
        """Compute a linear schedule of angles.

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
        """
        return np.linspace(start, stop, steps)

    def ansatz(
        self,
        depth: int,
        d_gamma: float,
        d_beta: float,
    ) -> QuantumVariable | QuantumArray:
        """Build the LR-QAOA ansatz on a fresh quantum argument.

        Parameters
        ----------
        depth : int
            Number of QAOA layers ``p``.
        d_gamma : float
            Final cost angle; ``gamma`` ramps from ``0`` to ``d_gamma``.
        d_beta : float
            Initial mixer strength; the mixer angle ramps from ``-d_beta`` to ``0``.

        Returns
        -------
        QuantumVariable | QuantumArray
            A new quantum argument from ``qarg()`` after applying the ansatz.

        Notes
        -----
        The mixer layers apply ``exp(-i beta X)``, for which the initial uniform
        superposition is the *highest*-energy state. The mixer angles are
        therefore negated, so that a positive ``d_beta`` anneals towards the
        minimum of the cost rather than the maximum.
        """
        gammas = self.linear_ramp(0.0, d_gamma, depth)
        betas = -self.linear_ramp(d_beta, 0.0, depth)
        qarg = self.qarg()

        self.problem.state_prep(qarg)
        for gamma, beta in zip(gammas, betas, strict=False):
            self.problem.cost_layer(qarg, gamma)
            self.problem.mixer_layer(qarg, beta)

        return qarg

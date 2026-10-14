"""Standard Quantum Approximate Optimization Algorithm (QAOA)."""

from collections.abc import Callable
from typing import Any

import numpy as np
from qrisp import QuantumArray, QuantumVariable
from scipy.optimize import minimize

from qrisp_optimization.metrics import exp_val
from qrisp_optimization.qaoa_requirements import QAOARequirements


class QAOA[T]:
    """QAOA solver for any problem implementing :class:`QAOARequirements`.

    Parameters
    ----------
    problem : QAOARequirements[T]
        Problem providing state preparation, cost layer and mixer layer.
    qarg : Callable[[], QuantumVariable | QuantumArray]
        Factory creating a fresh quantum argument; every call to
        :meth:`ansatz` builds on a new one.
    """

    def __init__(
        self,
        problem: QAOARequirements[T],
        qarg: Callable[[], QuantumVariable | QuantumArray]
    ) -> None:
        self.problem: QAOARequirements[T] = problem
        self.qarg: Callable[[], QuantumVariable | QuantumArray] = qarg

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
        qarg = self.qarg()

        self.problem.state_prep(qarg)
        for gamma, beta in zip(gammas, betas, strict=False):
            self.problem.cost_layer(qarg, gamma)
            self.problem.mixer_layer(qarg, beta)

        return qarg

    def optimize(
        self,
        theta: np.ndarray,
        metric: Callable[[QuantumVariable | QuantumArray, QAOARequirements[T]], float] = exp_val,
        method: str = "COBYLA",
        max_iter: int = 100,
        options: dict[str, Any] | None = None,
    ) -> np.ndarray:
        """Variationally optimize the QAOA angles.

        Parameters
        ----------
        theta : np.ndarray
            Initial angles of length ``2 * p`` (see :meth:`ansatz`).
        metric : Callable[[QuantumVariable | QuantumArray], float] | None, optional
            Objective to minimize, evaluated on the quantum argument after the
            ansatz is applied. Defaults to the expectation value of the
            problem's ``cl_cost_function`` over the measurement outcomes.
        method : str, optional
            Optimizer passed to :func:`scipy.optimize.minimize`. Default is ``"COBYLA"``.
        max_iter : int, optional
            Maximum number of optimizer iterations. Default is ``100``.
        options : dict[str, Any] | None, optional
            Additional optimizer options; these take precedence over ``max_iter``.

        Returns
        -------
        np.ndarray
            The optimized angles.
        """

        def objective(angles: np.ndarray) -> float:
            return metric(self.ansatz(angles), self.problem)

        result = minimize(
            fun=objective,
            x0=theta,
            method=method,
            options={"maxiter": max_iter, **(options or {})},
        )
        return np.asarray(result.x)

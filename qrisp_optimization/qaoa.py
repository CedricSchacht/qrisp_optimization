"""Standard Quantum Approximate Optimization Algorithm (QAOA)."""

from collections.abc import Callable
from typing import Any

import numpy as np
from qrisp import QuantumArray, QuantumVariable
from scipy.optimize import minimize

from qrisp_optimization.metrics import exp_val
from qrisp_optimization.qaoa_requirements import QAOARequirements


class QAOA[T]:
    """QAOA solver for any problem implementing `QAOARequirements`.

    Parameters
    ----------
    problem : QAOARequirements[T]
        Problem providing state preparation, cost layer and mixer layer.
    qarg : Callable[[], QuantumVariable | QuantumArray]
        Factory creating a fresh quantum argument; every call to
        [`ansatz`][qrisp_optimization.qaoa.QAOA.ansatz] builds on a new one.
    """

    def __init__(
        self, problem: QAOARequirements[T], qarg: Callable[[], QuantumVariable | QuantumArray]
    ) -> None:
        self.problem: QAOARequirements[T] = problem
        self.qarg: Callable[[], QuantumVariable | QuantumArray] = qarg

    def ansatz(self, theta: np.ndarray) -> QuantumVariable | QuantumArray:
        """Build the depth-``p`` QAOA ansatz on a fresh quantum argument.

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
            A new quantum argument from ``qarg()`` after applying the ansatz.
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
            Initial angles of length ``2 * p``
            (see [`ansatz`][qrisp_optimization.qaoa.QAOA.ansatz]).
        metric : Callable[[QuantumVariable | QuantumArray, QAOARequirements[T]], float], optional
            Objective to minimize. Called as ``metric(qarg, problem)`` with the
            quantum argument after the ansatz is applied and this solver's
            problem. Default is [`exp_val`][qrisp_optimization.metrics.exp_val], the
            expectation value of the problem's ``cl_cost_function``.
        method : str, optional
            Optimizer passed to
            [`scipy.optimize.minimize`][scipy.optimize.minimize].
            Default is ``"COBYLA"``.
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

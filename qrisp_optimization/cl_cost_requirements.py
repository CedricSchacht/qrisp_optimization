"""Base interface for problems with a classical cost function."""

from abc import ABC, abstractmethod


class CLCostRequirements[T](ABC):
    """Abstract interface for problems whose solutions can be evaluated classically.

    Shared base of [`QAOARequirements`][qrisp_optimization.QAOARequirements] and
    [`BruteforceRequirements`][qrisp_optimization.BruteforceRequirements], and the only
    part of a problem that metrics such as [`exp_val`][qrisp_optimization.metrics.exp_val] rely on.

    Type Parameters
    ---------------
    T
        Type of a classical solution (e.g. a binary assignment vector).
    """

    @abstractmethod
    def cl_cost_function(self, x: T) -> float:
        """Evaluate the classical cost of a solution.

        Parameters
        ----------
        x : T
            Classical solution, typically obtained by measuring ``qarg``.

        Returns
        -------
        float
            Cost of ``x``. Lower values are better.
        """
        ...

from abc import ABC, abstractmethod


class CLCostRequirements[T](ABC):
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

"""Interface a problem must implement to be solvable by :class:`Bruteforce`."""

from abc import ABC, abstractmethod
from collections.abc import Generator


class BruteforceRequirements[T](ABC):
    """Abstract interface for problems that can be solved by exhaustive search.

    Type Parameters
    ---------------
    T
        Type of a candidate solution (e.g. a binary assignment vector).
    """

    @abstractmethod
    def cl_cost_function(self, x: T) -> float:
        """Evaluate the classical cost of a candidate solution.

        Parameters
        ----------
        x : T
            Candidate solution.

        Returns
        -------
        float
            Cost of ``x``. Lower values are better.
        """
        ...

    @abstractmethod
    def next(self) -> Generator[T]:
        """Enumerate every candidate solution of the search space.

        Yields
        ------
        T
            Each candidate solution exactly once.
        """
        ...

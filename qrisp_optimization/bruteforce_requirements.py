"""Interface a problem must implement to be solvable by :class:`Bruteforce`."""

from abc import ABC, abstractmethod
from collections.abc import Generator

from qrisp_optimization.cl_cost_requriements import CLCostRequirements


class BruteforceRequirements[T](CLCostRequirements[T], ABC):
    """Abstract interface for problems that can be solved by exhaustive search.

    Type Parameters
    ---------------
    T
        Type of a candidate solution (e.g. a binary assignment vector).
    """

    @abstractmethod
    def next(self) -> Generator[T]:
        """Enumerate every candidate solution of the search space.

        Yields
        ------
        T
            Each candidate solution exactly once.
        """
        ...

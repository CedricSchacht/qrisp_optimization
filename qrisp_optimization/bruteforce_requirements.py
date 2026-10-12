from abc import ABC, abstractmethod
from collections.abc import Generator


class BruteforceRequirements[T](ABC):
    @abstractmethod
    def cl_cost_function(self, x: T) -> float:
        ...

    @abstractmethod
    def next(self) -> Generator[T]:
        ...

from abc import ABC, abstractmethod
from typing import Generator, Generic, TypeVar
import numpy as np
from numpy.typing import NDArray

T = TypeVar("T")

class Bruteforce_Requirements(ABC, Generic[T]):
    @abstractmethod
    def cl_cost_function(self, x: T) -> float:
        ...

    @abstractmethod
    def next(self) -> Generator[T, None, None]:
        ...
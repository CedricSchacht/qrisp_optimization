from abc import ABC, abstractmethod

class Bruteforce_Requirements(ABC):
    @abstractmethod
    def cl_cost_function(self, x: any) -> float: ...

    @abstractmethod
    def next(self) -> any: ...

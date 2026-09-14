from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from qrisp import QuantumVariable, QuantumArray

T = TypeVar("T")

class QAOA_Requirements(ABC, Generic[T]):
    @abstractmethod
    def cl_cost_function(self, x: T) -> float: ...

    @abstractmethod
    def state_prep(
        self, 
        qarg: QuantumVariable | QuantumArray
        ) -> QuantumVariable | QuantumArray: ...

    @abstractmethod
    def cost_layer(
        self, 
        qarg: QuantumVariable | QuantumArray, 
        gamma: float
        ) -> QuantumVariable | QuantumArray: ...

    @abstractmethod
    def mixer_layer(
        self, 
        qarg: QuantumVariable | QuantumArray, 
        beta: float
        ) -> QuantumVariable | QuantumArray: ...
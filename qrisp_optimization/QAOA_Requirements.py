from abc import ABC, abstractmethod
from qrisp import QuantumVariable, QuantumArray

class QAOA_Requirements(ABC):
    @abstractmethod
    def cl_cost_function(self, x) -> float: ...

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
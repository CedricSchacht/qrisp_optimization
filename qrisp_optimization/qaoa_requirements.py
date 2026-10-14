"""Interface a problem must implement to be solvable by QAOA-type solvers."""

from abc import ABC, abstractmethod

from qrisp import QuantumArray, QuantumVariable

from qrisp_optimization.cl_cost_requirements import CLCostRequirements


class QAOARequirements[T](CLCostRequirements[T], ABC):
    """Abstract interface for problems solvable by `QAOA` and `LRQAOA`.

    Type Parameters
    ---------------
    T
        Type of a classical solution, i.e. a measurement outcome of ``qarg``.
    """

    @abstractmethod
    def state_prep(self, qarg: QuantumVariable | QuantumArray) -> QuantumVariable | QuantumArray:
        """Prepare the initial state of the QAOA circuit.

        Parameters
        ----------
        qarg : QuantumVariable | QuantumArray
            Quantum argument to prepare in place.

        Returns
        -------
        QuantumVariable | QuantumArray
            The prepared quantum argument.
        """
        ...

    @abstractmethod
    def cost_layer(
        self, qarg: QuantumVariable | QuantumArray, gamma: float
    ) -> QuantumVariable | QuantumArray:
        """Apply one layer of the phase-separating cost operator.

        Parameters
        ----------
        qarg : QuantumVariable | QuantumArray
            Quantum argument to act on in place.
        gamma : float
            Cost-layer angle.

        Returns
        -------
        QuantumVariable | QuantumArray
            The transformed quantum argument.
        """
        ...

    @abstractmethod
    def mixer_layer(
        self, qarg: QuantumVariable | QuantumArray, beta: float
    ) -> QuantumVariable | QuantumArray:
        """Apply one layer of the mixer operator.

        Parameters
        ----------
        qarg : QuantumVariable | QuantumArray
            Quantum argument to act on in place.
        beta : float
            Mixer-layer angle.

        Returns
        -------
        QuantumVariable | QuantumArray
            The transformed quantum argument.
        """
        ...

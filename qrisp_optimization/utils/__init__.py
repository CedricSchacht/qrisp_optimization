"""Temporary helpers that may eventually move into Qrisp itself."""

from qrisp import QuantumVariable

# TODO remove this package once better places are found for the functions


# this could be part of qrisp core (might even be a QuantumBool(numeric=True) kind of syntax?)
class QuantumBinary(QuantumVariable):
    """Single-qubit quantum variable that measures as ``0`` or ``1``.

    This is only needed, since QuantumBool returns True or False,
    while 0 and 1 are needed to use the bitstring
    as an assignment vector in the cl_cost_function of the problem.
    """

    def __init__(self) -> None:
        """Create a single-qubit quantum variable."""
        QuantumVariable.__init__(self, size=1)

    def encoder(self, value: int) -> int:
        """Map a label to its qubit-register integer.

        Parameters
        ----------
        value : int
            Label to encode.

        Returns
        -------
        int
            ``1`` if ``value >= 1``, otherwise ``0``.
        """
        if value >= 1:
            return 1
        else:
            return 0

    def decoder(self, value: int) -> int:
        """Map a measured qubit-register integer to its label.

        Parameters
        ----------
        value : int
            Integer measured from the register.

        Returns
        -------
        int
            ``1`` if ``value >= 1``, otherwise ``0``.
        """
        if value >= 1:
            return 1
        else:
            return 0

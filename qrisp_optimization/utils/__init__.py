from qrisp import QuantumVariable

# TODO remove this package once better places are found for the functions

# this could be part of qrisp core (might even be a QuantumBool(numeric=True) kind of syntax?)
class QuantumBinary(QuantumVariable):
    """
        This is only needed, since QuantumBool returns True or False,
        while 0 and 1 are needed to use the bitstring
        as a asignment vector in the cl_cost_function of the problem
    """
    def __init__(self) -> None:
        QuantumVariable.__init__(self, size=1)

    def encoder(self, value: int) -> int:
        if value >= 1:
            return 1
        else:
            return 0

    def decoder(self, value: int) -> int:
        if value >= 1:
            return 1
        else:
            return 0

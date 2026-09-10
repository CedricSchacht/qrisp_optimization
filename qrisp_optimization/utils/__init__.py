from qrisp import QuantumVariable
from qrisp_optimization import Bruteforce_Requirements

# TODO remove this package once better places are found for the functions

# this could be part of qrisp core
class QuantumBinary(QuantumVariable):
    """
        This is only needed, since QuantumBool returns True or False, while 0 and 1 are needed to use the bitstring as a asignment vector in the cl_cost_function of the problem
    """
    def __init__(self):
        QuantumVariable.__init__(self, size=1)

    def encoder(self, value):
        if value >= 1:
            return 1
        else:
            return 0

    def decoder(self, value):
        if value >= 1:
            return 1
        else:
            return 0

# 
def print_solutions(problem: Bruteforce_Requirements, optimal, meas):
    """
        print the bitstrings with it's classical costs and probabilities given measurements and a list of optimal bitstrings
    """

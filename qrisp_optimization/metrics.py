from qrisp import QuantumArray, QuantumVariable

from qrisp_optimization.cl_cost_requriements import CLCostRequirements


def exp_val[T](qarg: QuantumVariable | QuantumArray, problem: CLCostRequirements[T]) -> float:
    meas = qarg.get_measurement()
    return float(sum(p * problem.cl_cost_function(x) for x, p in meas.items()))


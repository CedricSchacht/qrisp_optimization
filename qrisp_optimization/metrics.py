"""Objectives that reduce a measured quantum argument to a scalar cost.

Every metric has the signature ``metric(qarg, problem) -> float`` and can be
passed to [`QAOA.optimize`][qrisp_optimization.qaoa.QAOA.optimize], which minimizes it.
"""

from qrisp import QuantumArray, QuantumVariable

from qrisp_optimization.cl_cost_requirements import CLCostRequirements


def exp_val[T](qarg: QuantumVariable | QuantumArray, problem: CLCostRequirements[T]) -> float:
    """Compute the expected classical cost over measurements of ``qarg``.

    Parameters
    ----------
    qarg : QuantumVariable | QuantumArray
        Quantum argument to measure.
    problem : CLCostRequirements[T]
        Problem whose ``cl_cost_function`` is evaluated on every outcome.

    Returns
    -------
    float
        ``sum(p(x) * problem.cl_cost_function(x))`` over all measured
        outcomes ``x`` with probability ``p(x)``.
    """
    meas = qarg.get_measurement()
    return float(sum(p * problem.cl_cost_function(x) for x, p in meas.items()))

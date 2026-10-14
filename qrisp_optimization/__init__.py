"""Solver-agnostic optimization framework built on top of Qrisp.

Problems implement small requirement interfaces
([`QAOARequirements`][qrisp_optimization.QAOARequirements],
[`BruteforceRequirements`][qrisp_optimization.BruteforceRequirements], both based on
[`CLCostRequirements`][qrisp_optimization.CLCostRequirements]) and can then be handed to
any solver that consumes that interface ([`QAOA`][qrisp_optimization.QAOA],
[`LRQAOA`][qrisp_optimization.LRQAOA], [`Bruteforce`][qrisp_optimization.Bruteforce]).

The package is organized into:

- `problems`: concrete problems such as
  [`QUBOProblem`][qrisp_optimization.problems.QUBOProblem] and
  [`MaxCutProblem`][qrisp_optimization.problems.MaxCutProblem].
- `metrics`: objectives for [`QAOA.optimize`][qrisp_optimization.qaoa.QAOA.optimize], e.g.
  [`exp_val`][qrisp_optimization.metrics.exp_val].
- `utils`: helpers such as [`QuantumBinary`][qrisp_optimization.utils.QuantumBinary].
"""

from qrisp_optimization import metrics as metrics
from qrisp_optimization import problems as problems
from qrisp_optimization import utils as utils
from qrisp_optimization.bruteforce import Bruteforce as Bruteforce
from qrisp_optimization.bruteforce_requirements import (
    BruteforceRequirements as BruteforceRequirements,
)
from qrisp_optimization.cl_cost_requirements import CLCostRequirements as CLCostRequirements
from qrisp_optimization.lr_qaoa import LRQAOA as LRQAOA
from qrisp_optimization.qaoa import QAOA as QAOA
from qrisp_optimization.qaoa_requirements import QAOARequirements as QAOARequirements

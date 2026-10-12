"""Solver-agnostic optimization framework built on top of Qrisp.

Problems implement small requirement interfaces (:class:`QAOARequirements`,
:class:`BruteforceRequirements`) and can then be handed to any solver that
consumes that interface (:class:`QAOA`, :class:`LRQAOA`, :class:`Bruteforce`).
"""

from qrisp_optimization.bruteforce import Bruteforce as Bruteforce
from qrisp_optimization.bruteforce_requirements import (
    BruteforceRequirements as BruteforceRequirements,
)
from qrisp_optimization.lr_qaoa import LRQAOA as LRQAOA
from qrisp_optimization.qaoa import QAOA as QAOA
from qrisp_optimization.qaoa_requirements import QAOARequirements as QAOARequirements

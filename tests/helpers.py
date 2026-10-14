"""Plain helper functions shared by the tests."""

import itertools
from collections.abc import Callable

import numpy as np
from numpy.typing import NDArray
from qrisp import QuantumArray

from qrisp_optimization.utils import QuantumBinary

type QargFactory = Callable[[], QuantumArray]


def binary_qarg_factory(n: int) -> QargFactory:
    """Return a factory creating a fresh array of ``n`` binary qubits."""
    return lambda: QuantumArray(qtype=QuantumBinary(), shape=n)


def all_assignments(n: int) -> list[NDArray[np.int_]]:
    """All ``2**n`` binary vectors in lexicographic order."""
    return [np.array(bits, dtype=int) for bits in itertools.product((0, 1), repeat=n)]


def statevector(qarg: QuantumArray) -> NDArray[np.complex128]:
    """Statevector of ``qarg``'s session, indexed by assignments ``x``.

    Qrisp orders the basis big-endian over the qubits of the session, so the
    amplitude of ``x`` is at index ``int("".join(map(str, x)), 2)``.
    """
    return np.asarray(qarg.qs.statevector("array"), dtype=np.complex128)


def index_of(x: NDArray[np.int_]) -> int:
    """Statevector index of the assignment ``x`` (see :func:`statevector`)."""
    return int("".join(str(int(b)) for b in x), 2)

"""Tests for :class:`QUBOProblem`."""

import numpy as np
import pytest
from numpy.typing import NDArray

from qrisp_optimization.problems import QUBOProblem

from helpers import all_assignments, binary_qarg_factory, index_of, statevector

# classical cost

def test_cl_cost_function_is_xT_Q_x(qubo: QUBOProblem, qubo_q: NDArray[np.float64]) -> None:  # noqa: N802
    for x in all_assignments(qubo.n):
        assert qubo.cl_cost_function(x) == pytest.approx(float(x @ qubo_q @ x))


def test_cl_cost_function_examples(qubo: QUBOProblem) -> None:
    assert qubo.cl_cost_function(np.array([0, 0, 0, 0])) == 0.0
    assert qubo.cl_cost_function(np.array([1, 0, 0, 0])) == -1.0
    # diagonal -1 - 2 plus coupling 2
    assert qubo.cl_cost_function(np.array([1, 1, 0, 0])) == -1.0
    assert qubo.cl_cost_function(np.array([0, 1, 1, 0])) == -2.5


def test_cl_cost_function_returns_float(qubo: QUBOProblem) -> None:
    assert isinstance(qubo.cl_cost_function(np.array([1, 0, 1, 0])), float)


# Bruteforce requirements

def test_next_enumerates_every_assignment_once_in_lexicographic_order(qubo: QUBOProblem) -> None:
    candidates = list(qubo.next())

    assert [x.tolist() for x in candidates] == [x.tolist() for x in all_assignments(qubo.n)]


def test_next_yields_independent_arrays(qubo: QUBOProblem) -> None:
    first, second, *_ = qubo.next()
    first[:] = 1

    assert second.tolist() == [0, 0, 0, 1]


# QAOA requirements

def test_state_prep_creates_uniform_superposition(qubo: QUBOProblem) -> None:
    qarg = binary_qarg_factory(qubo.n)()

    assert qubo.state_prep(qarg) is qarg
    uniform = np.full(2**qubo.n, 2 ** (-qubo.n / 2))
    np.testing.assert_allclose(statevector(qarg), uniform, atol=1e-6)


@pytest.mark.parametrize("gamma", [0.0, 0.37, -1.2])
def test_cost_layer_applies_exp_minus_i_gamma_cost(qubo: QUBOProblem, gamma: float) -> None:
    qarg = binary_qarg_factory(qubo.n)()
    qubo.state_prep(qarg)

    assert qubo.cost_layer(qarg, gamma) is qarg
    # qrisp's create_QUBO_cost_operator rescales gamma by 1 / sqrt(||Q||_F)
    scaled_gamma = gamma / np.sqrt(np.linalg.norm(qubo.Q))
    sv = statevector(qarg) * 2 ** (qubo.n / 2)
    xs = all_assignments(qubo.n)
    actual = np.array([sv[index_of(x)] for x in xs])
    expected = np.array([np.exp(-1j * scaled_gamma * qubo.cl_cost_function(x)) for x in xs])
    # equal up to a global phase
    np.testing.assert_allclose(actual, actual[0] / expected[0] * expected, atol=1e-6)


@pytest.mark.parametrize("beta", [0.0, 0.4, 1.3])
def test_mixer_layer_applies_rx_on_every_qubit(qubo: QUBOProblem, beta: float) -> None:
    qarg = binary_qarg_factory(qubo.n)()

    assert qubo.mixer_layer(qarg, beta) is qarg
    # exp(-i beta X)|0> = cos(beta)|0> - i sin(beta)|1> on every qubit
    sv = statevector(qarg)
    for x in all_assignments(qubo.n):
        k = int(x.sum())
        expected = np.cos(beta) ** (qubo.n - k) * (-1j * np.sin(beta)) ** k
        assert sv[index_of(x)] == pytest.approx(expected, abs=1e-6)

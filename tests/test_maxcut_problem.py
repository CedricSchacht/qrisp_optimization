"""Tests for :class:`MaxCutProblem`."""

import networkx as nx
import numpy as np
import pytest

from qrisp_optimization.problems import MaxCutProblem

from helpers import all_assignments, binary_qarg_factory, index_of, statevector

# construction


def test_nodes_are_mapped_to_indices_in_graph_order(triangle: nx.Graph[str]) -> None:
    problem = MaxCutProblem(triangle)

    assert problem.nodes == ["a", "b", "c"]
    assert problem.n == 3
    assert sorted(problem.edges) == [(0, 1, 0.7), (0, 2, 2.0), (1, 2, 1.0)]


def test_missing_weight_defaults_to_one(square: nx.Graph[int]) -> None:
    assert all(w == 1.0 for _, _, w in MaxCutProblem(square).edges)


def test_self_loops_are_ignored(square: nx.Graph[int]) -> None:
    square.add_edge(0, 0, weight=5.0)

    problem = MaxCutProblem(square)

    assert len(problem.edges) == 4
    assert problem.cl_cost_function(np.array([1, 0, 0, 0])) == -2.0


def test_isolated_nodes_get_a_qubit() -> None:
    G = nx.Graph()  # noqa: N806
    G.add_nodes_from([0, 1, 2])
    G.add_edge(0, 1)

    problem = MaxCutProblem(G)

    assert problem.n == 3
    assert problem.cl_cost_function(np.array([0, 1, 1])) == -1.0


# classical cost


def test_cl_cost_function_is_negative_cut_weight(triangle: nx.Graph[str]) -> None:
    problem = MaxCutProblem(triangle)

    assert problem.cl_cost_function(np.array([0, 0, 0])) == 0.0
    assert problem.cl_cost_function(np.array([1, 0, 0])) == pytest.approx(-2.7)  # a | b, c
    assert problem.cl_cost_function(np.array([0, 1, 0])) == pytest.approx(-1.7)  # b | a, c
    assert problem.cl_cost_function(np.array([0, 0, 1])) == pytest.approx(-3.0)  # c | a, b


def test_cl_cost_function_is_symmetric_under_flipping_sides(maxcut: MaxCutProblem) -> None:
    for x in all_assignments(maxcut.n):
        assert maxcut.cl_cost_function(x) == maxcut.cl_cost_function(1 - x)


def test_cl_cost_function_returns_float(maxcut: MaxCutProblem) -> None:
    assert isinstance(maxcut.cl_cost_function(np.array([1, 0, 1, 0])), float)


# Bruteforce requirements


def test_next_enumerates_every_assignment_once_in_lexicographic_order(
    maxcut: MaxCutProblem,
) -> None:
    candidates = list(maxcut.next())

    assert [x.tolist() for x in candidates] == [x.tolist() for x in all_assignments(maxcut.n)]


def test_next_yields_independent_arrays(maxcut: MaxCutProblem) -> None:
    first, second, *_ = maxcut.next()
    first[:] = 1

    assert second.tolist() == [0, 0, 0, 1]


# QAOA requirements


def test_state_prep_creates_uniform_superposition(maxcut: MaxCutProblem) -> None:
    qarg = binary_qarg_factory(maxcut.n)()

    assert maxcut.state_prep(qarg) is qarg
    uniform = np.full(2**maxcut.n, 2 ** (-maxcut.n / 2))
    np.testing.assert_allclose(statevector(qarg), uniform, atol=1e-6)


@pytest.mark.parametrize("gamma", [0.0, 0.37, -1.2])
def test_cost_layer_applies_exp_minus_i_gamma_cost(triangle: nx.Graph[str], gamma: float) -> None:
    problem = MaxCutProblem(triangle)
    qarg = binary_qarg_factory(problem.n)()
    problem.state_prep(qarg)

    assert problem.cost_layer(qarg, gamma) is qarg
    sv = statevector(qarg) * 2 ** (problem.n / 2)
    for x in all_assignments(problem.n):
        expected = np.exp(-1j * gamma * problem.cl_cost_function(x))
        assert sv[index_of(x)] == pytest.approx(expected, abs=1e-6)


@pytest.mark.parametrize("beta", [0.0, 0.4, 1.3])
def test_mixer_layer_applies_rx_on_every_qubit(maxcut: MaxCutProblem, beta: float) -> None:
    qarg = binary_qarg_factory(maxcut.n)()

    assert maxcut.mixer_layer(qarg, beta) is qarg
    # exp(-i beta X)|0> = cos(beta)|0> - i sin(beta)|1> on every qubit
    sv = statevector(qarg)
    for x in all_assignments(maxcut.n):
        k = int(x.sum())
        expected = np.cos(beta) ** (maxcut.n - k) * (-1j * np.sin(beta)) ** k
        assert sv[index_of(x)] == pytest.approx(expected, abs=1e-6)

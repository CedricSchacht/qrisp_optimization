"""Shared fixtures for the test suite."""

import networkx as nx
import numpy as np
import pytest
from numpy.typing import NDArray

from qrisp_optimization.problems import MaxCutProblem, QUBOProblem


@pytest.fixture
def qubo_q() -> NDArray[np.float64]:
    """Small 4-variable upper-triangular QUBO matrix with a unique optimum."""
    return np.array([
        [-1.0,  2.0,  0.0, -0.5],
        [ 0.0, -2.0,  1.0,  0.0],
        [ 0.0,  0.0, -1.5,  2.5],
        [ 0.0,  0.0,  0.0,  1.0],
    ])


@pytest.fixture
def qubo(qubo_q: NDArray[np.float64]) -> QUBOProblem:
    """QUBO problem built from :func:`qubo_q`."""
    return QUBOProblem(Q=qubo_q)


@pytest.fixture
def triangle() -> nx.Graph[str]:
    """Weighted triangle with string node labels."""
    G = nx.Graph()  # noqa: N806
    G.add_edge("a", "b", weight=0.7)
    G.add_edge("b", "c")
    G.add_edge("a", "c", weight=2.0)
    return G


@pytest.fixture
def square() -> nx.Graph[int]:
    """Unweighted 4-cycle; its maximum cut has weight 4."""
    return nx.cycle_graph(4)


@pytest.fixture
def maxcut(square: nx.Graph[int]) -> MaxCutProblem:
    """MaxCut problem on :func:`square`."""
    return MaxCutProblem(square)

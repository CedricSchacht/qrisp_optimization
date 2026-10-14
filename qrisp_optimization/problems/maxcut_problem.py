"""Weighted MaxCut problem."""

import itertools
from collections.abc import Generator, Hashable

import networkx as nx
import numpy as np
from numpy.typing import NDArray
from qrisp import QuantumArray, cx, h, p
from qrisp.qaoa import RX_mixer

from qrisp_optimization.bruteforce_requirements import BruteforceRequirements
from qrisp_optimization.qaoa_requirements import QAOARequirements

type BinaryIntArray = NDArray[np.int_]

class MaxCutProblem(
    QAOARequirements[BinaryIntArray],
    BruteforceRequirements[BinaryIntArray]
):
    """Weighted MaxCut problem.

    Solvable by both QAOA-type solvers and :class:`Bruteforce`.

    Partition the nodes of a graph into two sets such that the total weight of
    the edges between the sets is maximal. A solution ``x`` assigns node
    ``nodes[i]`` to side ``x[i]``. Since solvers minimize, the cost is the
    negative cut weight.

    Parameters
    ----------
    G : nx.Graph
        Undirected graph. Edge weights are read from the ``"weight"``
        attribute and default to ``1``. Self-loops are ignored.
    """

    def __init__(self, G: nx.Graph[Hashable]) -> None:  # noqa: N803
        self.G: nx.Graph[Hashable] = G
        self.nodes: list[Hashable] = list(G.nodes)
        self.n: int = len(self.nodes)
        index = {node: i for i, node in enumerate(self.nodes)}
        self.edges: list[tuple[int, int, float]] = [
            (index[u], index[v], float(w))
            for u, v, w in G.edges(data="weight", default=1.0)
            if u != v
        ]

    # needed for QAOA and Bruteforce
    def cl_cost_function(self, x: BinaryIntArray) -> float:
        """Evaluate the negative weight of the cut defined by ``x``.

        Parameters
        ----------
        x : BinaryIntArray
            Binary vector of length ``n``; ``x[i]`` is the side of ``nodes[i]``.

        Returns
        -------
        float
            ``-sum(w_ij for edges (i, j) with x[i] != x[j])``.
        """
        return -float(sum(w for i, j, w in self.edges if x[i] != x[j]))

    # needed for Bruteforce only
    def next(self) -> Generator[BinaryIntArray]:
        """Enumerate all ``2**n`` binary vectors in lexicographic order.

        Yields
        ------
        BinaryIntArray
            Each binary vector of length ``n``, starting with all zeros and
            ending with all ones.
        """
        for bits in itertools.product((0, 1), repeat=self.n):
            yield np.array(bits, dtype=int)

    # needed for QAOA only
    def state_prep(self, qarg: QuantumArray) -> QuantumArray:
        """Prepare the uniform superposition by applying Hadamard to every qubit.

        Parameters
        ----------
        qarg : QuantumArray
            Array of binary quantum variables, one per node.

        Returns
        -------
        QuantumArray
            ``qarg`` in uniform superposition.
        """
        for qv in qarg:
            h(qv)
        return qarg

    # needed for QAOA only
    def cost_layer(self, qarg: QuantumArray, gamma: float) -> QuantumArray:
        """Apply the phase-separating operator ``exp(-i gamma C)`` of the cut cost.

        Each edge ``(i, j)`` contributes a phase ``exp(i gamma w_ij)`` to every
        basis state in which ``i`` and ``j`` lie on different sides of the cut.

        Parameters
        ----------
        qarg : QuantumArray
            Array of binary quantum variables, one per node.
        gamma : float
            Cost-layer angle.

        Returns
        -------
        QuantumArray
            ``qarg`` after applying the cost layer.
        """
        for i, j, w in self.edges:
            # compute x_i XOR x_j into qubit j, phase it, uncompute
            cx(qarg[i], qarg[j])
            p(gamma * w, qarg[j])
            cx(qarg[i], qarg[j])
        return qarg

    # needed for QAOA only
    def mixer_layer(self, qarg: QuantumArray, beta: float) -> QuantumArray:
        """Apply the transverse-field ``RX`` mixer to every qubit.

        Parameters
        ----------
        qarg : QuantumArray
            Array of binary quantum variables, one per node.
        beta : float
            Mixer-layer angle.

        Returns
        -------
        QuantumArray
            ``qarg`` after applying the mixer layer.
        """
        for qv in qarg:
            RX_mixer(qv, beta)
        return qarg

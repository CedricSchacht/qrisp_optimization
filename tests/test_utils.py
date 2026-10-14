"""Tests for :mod:`qrisp_optimization.utils`."""

import pytest
from qrisp import QuantumArray, x

from qrisp_optimization.utils import QuantumBinary


@pytest.mark.parametrize(("value", "expected"), [(0, 0), (1, 1), (5, 1), (-1, 0)])
def test_encoder_and_decoder_map_to_bits(value: int, expected: int) -> None:
    qb = QuantumBinary()

    assert qb.encoder(value) == expected
    assert qb.decoder(value) == expected


def test_measurement_yields_integer_bits() -> None:
    qarg = QuantumArray(qtype=QuantumBinary(), shape=3)
    x(qarg[1])

    ((outcome, prob),) = qarg.get_measurement().items()

    assert list(outcome) == [0, 1, 0]
    assert prob == pytest.approx(1.0)

"""Tests for the Numeric field"""

import pytest

from swissdta.fields import Numeric
from swissdta.records.record import DTARecord

FIELD_LENGTH = 5


class NRecord(DTARecord):
    """Subclass of DTARecord for testing the Numeric field"""
    field = Numeric(length=FIELD_LENGTH)


@pytest.mark.parametrize(('value', 'expected_errors'), (
    (5, tuple()),
    ('5', tuple()),
    (5., ("[field] NOT NUMERICAL: Only digits allowed (got: '5.0')",)),
    ('nope', ("[field] NOT NUMERICAL: Only digits allowed (got: 'nope')",)),
    (1_4_3, tuple()),
    (14_00_0, tuple()),
    (0b11, tuple()),
    (0B11, tuple()),
    (0b11_11, tuple()),
    (0B11_1, tuple()),
    (0o17, tuple()),
    (0O31, tuple()),
    (0o10_42, tuple()),
    (0O23_5, tuple()),
    (0xAF, tuple()),
    (0Xa3, tuple()),
    (0xf4_4c, tuple()),
    (0Xfb_1, tuple()),

))
def test_non_numeric_values(value, expected_errors):
    """Verify that non numeric values are detected"""
    record = NRecord()
    record.field = value
    assert record.validation_errors == expected_errors

"""Tests for the Amount field"""

from decimal import Decimal

import pytest

from swissdta.fields import Amount
from swissdta.records.record import DTARecord

FIELD_LENGTH = 8


class ARecord(DTARecord):
    """Subclass of DTARecord for testing the Numeric field"""
    field = Amount(length=FIELD_LENGTH)


@pytest.mark.parametrize(('value', 'expected_value'), (
    (Decimal('1_4_3'), '143,    '),
    (Decimal('14_00_0'), '14000,  '),
    (Decimal(0b11), '3,      '),
    (Decimal(0B11), '3,      '),
    (Decimal(0b11_11), '15,     '),
    (Decimal(0B11_1), '7,      '),
    (Decimal(0o17), '15,     '),
    (Decimal(0O31), '25,     '),
    (Decimal(0o10_42), '546,    '),
    (Decimal(0O23_5), '157,    '),
    (Decimal(0xAF), '175,    '),
    (Decimal(0Xa3), '163,    '),
    (Decimal(0xf4_4c), '62540,  '),
    (Decimal(0Xfb_1), '4017,   '),
    (Decimal('5.34'), '5,34    ')
))
def test_format_values(value, expected_value):
    record = ARecord()
    record.field = value
    assert record.field == expected_value
    assert not record.validation_warnings
    assert not record.validation_errors


@pytest.mark.parametrize(('value', 'expected_errors'), (
    (Decimal('5'), tuple()),
    (Decimal('5.'), tuple()),
    (Decimal('-5'), ("[field] INVALID: May not be negative",)),
    (Decimal('-5.'), ("[field] INVALID: May not be negative",)),
    (Decimal('0'), ("[field] INVALID: May not be zero",)),
    (Decimal('0.'), ("[field] INVALID: May not be zero",))
))
def test_invalid_values(value, expected_errors):
    """Verify that non positive values are detected"""
    record = ARecord()
    record.field = value
    assert not record.validation_warnings
    assert record.validation_errors == expected_errors

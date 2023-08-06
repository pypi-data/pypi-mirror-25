"""Tests for the Iban field."""

import pytest

from swissdta.fields import Iban
from swissdta.records.record import DTARecord

FIELD_LENGTH = 25


class IbanRecord(DTARecord):
    """Subclass of DTARecord for testing the Iban field."""

    field = Iban(length=FIELD_LENGTH)


@pytest.mark.parametrize(('value', 'expected_errors'), (
    ('CH93 0076 2011 6238 5295 7', tuple()),
    ('LI21 0881 0000 2324 013A A', tuple()),
    ('LI22 0881 0000 2324 013A A', ('[field] IBAN INVALID: Invalid checksum digits',)),
    ('HU42 1177 3016 1111 1018 0000 0000',
     ("[field] TOO LONG: 'HU42117730161111101800000000' can be at most 25 characters",)),
))
def test_invalid_values(value, expected_errors):
    """Verify that invalid ibans are detected."""
    record = IbanRecord()
    record.field = value
    assert not record.validation_warnings
    assert record.validation_errors == expected_errors


@pytest.mark.parametrize(('value', 'expected_value'), (
    ('CH38 0888 8123 4567 8901 2', 'CH3808888123456789012    '),
    ('CH9300762011623852957', 'CH9300762011623852957    '),
))
def test_format_values(value, expected_value):
    """Verify that values are formatted correctly."""
    record = IbanRecord()
    record.field = value
    assert record.field == expected_value
    assert not record.validation_warnings
    assert not record.validation_errors

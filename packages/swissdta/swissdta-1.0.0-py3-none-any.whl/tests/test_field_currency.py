"""Tests for the Currency field."""

import pytest

from swissdta.fields import Currency
from swissdta.records.record import DTARecord

FIELD_LENGTH = 3


class CRecord(DTARecord):
    """Subclass of DTARecord for testing the Currency field."""

    field = Currency(length=FIELD_LENGTH)


@pytest.mark.parametrize(('value', 'expected_errors'), (
    ('CHFF', ("[field] TOO LONG: 'CHFF' can be at most 3 characters",
              "[field] INVALID: Must contain a valid ISO currency code. (got: 'CHFF')")),
    ('CHF', tuple()),
    ('CHH', ("[field] INVALID: Must contain a valid ISO currency code. (got: 'CHH')",)),
))
def test_invalid_values(value, expected_errors):
    """Verify that invalid currencies are detected."""
    record = CRecord()
    record.field = value
    assert not record.validation_warnings
    assert record.validation_errors == expected_errors

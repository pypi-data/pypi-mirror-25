"""Test for the date field."""

from datetime import date

import pytest

from swissdta.fields import Date
from swissdta.records.record import DTARecord


class DRecord(DTARecord):
    """Subclass of DTARecord for testing the Date field."""

    field = Date()


@pytest.mark.parametrize(('value', 'expected_value'), (
    (None, '000000'),
    (date(2017, 10, 12), '171012'),
    (date(2017, 11, 6), '171106'),
    (date(2017, 2, 14), '170214'),
    (date(2017, 1, 3), '170103')
))
def test_format_values(value, expected_value):
    """Verify that date values are formatted correctly."""
    record = DRecord()
    record.field = value
    assert record.field == expected_value
    assert not record.validation_warnings
    assert not record.validation_errors


@pytest.mark.parametrize(('value', 'expected_errors'), (
    (None, tuple()),
    (date(2017, 10, 12), tuple()),
    ('171106', ("[field] INVALID: date must contain a valid date or None (000000).",)),
    (5, ("[field] INVALID: date must contain a valid date or None (000000).",))
))
def test_invalid_dates(value, expected_errors):
    """Verify that invalid date values are detected correctly."""
    record = DRecord()
    record.field = value
    assert record.validation_errors == expected_errors

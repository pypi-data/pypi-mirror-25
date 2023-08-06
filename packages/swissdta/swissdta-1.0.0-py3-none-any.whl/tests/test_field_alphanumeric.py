"""Tests for the Alphanumeric field"""

import pytest

from swissdta.fields import AlphaNumeric
from swissdta.records.record import DTARecord

FIELD_LENGTH = 10


class ANRecord(DTARecord):
    """Subclass of DTARecord for testing the Alphanumeric field"""
    field = AlphaNumeric(length=FIELD_LENGTH, truncate=False)


@pytest.mark.parametrize(('input_text', 'expected_text'), (
    ('Bob', 'Bob'),
    ('Zürich', 'Zuerich'),
    ('Était', 'Etait')
))
def test_characters_conversion(input_text, expected_text):
    """Verify that text is converted correctly"""
    expected_text = expected_text.ljust(10, ' ')
    record = ANRecord()
    record.field = input_text
    assert record.field == expected_text


@pytest.mark.parametrize(('input_value', 'expected_value', 'expected_warnings', 'expected_errors', 'field_params'), (
    ('0123', '0123 ', tuple(), tuple(), {'length': 5, 'truncate': True}),
    ('01234', '01234', tuple(), tuple(), {'length': 5, 'truncate': True}),
    ('012345', '01234', ("[field] WARNING: '012345' over 5 characters long, truncating to '01234'",), tuple(),
     {'length': 5, 'truncate': True}),
    ('0123456789', '01234', ("[field] WARNING: '0123456789' over 5 characters long, truncating to '01234'",),
     tuple(), {'length': 5, 'truncate': True}),
    ('0123', '0123 ', tuple(), tuple(), {'length': 5, 'truncate': False}),
    ('01234', '01234', tuple(), tuple(), {'length': 5, 'truncate': False}),
    ('012345', '012345', tuple(), ("[field] TOO LONG: '012345' can be at most 5 characters",),
     {'length': 5, 'truncate': False}),
    ('0123456789', '0123456789', tuple(),
     ("[field] TOO LONG: '0123456789' can be at most 5 characters",),
     {'length': 5, 'truncate': False})
))
def test_truncate(input_value, expected_value, expected_warnings, expected_errors, field_params):
    """Verify that text is truncated correctly"""
    class TestRecord(DTARecord):
        """Simple Record class for testing"""
        field = AlphaNumeric(**field_params)

    record = TestRecord()
    record.field = input_value
    assert record.field == expected_value
    assert record.validation_warnings == expected_warnings
    assert record.validation_errors == expected_errors

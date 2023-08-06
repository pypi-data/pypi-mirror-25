"""Tests for the util methods."""

import pytest

from swissdta.util import remove_whitespace, is_swiss_iban


@pytest.mark.parametrize(('input_text', 'expected_text'), (
    ('01234567890', '01234567890'),
    (' 01234567890', '01234567890'),
    ('\t01234567890', '01234567890'),
    ('01234567890 ', '01234567890'),
    ('01234567890\n', '01234567890'),
    ('01234\r567890', '01234567890'),
    ('\x0b01234567890', '01234567890'),
    ('01234567890\x0c', '01234567890'),
    ('0 1 234 567   890', '01234567890')
))
def test_remove_whitespace(input_text, expected_text):
    """Verify that whitespaces are removed."""
    assert remove_whitespace(input_text) == expected_text


@pytest.mark.parametrize(('input_value', 'expected_value'), (
    ('CH93 0076 2011 6238 5295 7', True),
    ('HU42 1177 3016 1111 1018 0000 0000', False),
    ('LI21 0881 0000 2324 013A A', True),
))
def test_is_swiss_iban(input_value, expected_value):
    """Verify that CH and LI IBANs are marked True."""
    assert is_swiss_iban(input_value) == expected_value

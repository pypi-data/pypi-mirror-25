"""Tests for the DTA file"""

from datetime import date
from decimal import Decimal

import pytest
from swissdta.records import DTARecord890, DTARecord836
from swissdta.constants import IdentificationPurpose, ChargesRule
from swissdta.file import DTAFile


@pytest.mark.parametrize(('record_data', 'duplicate_record_indexes'), (
    ([{
        'reference': '01234567890',
        'client_account': 'CH38 0888 8123 4567 8901 2',
        'processing_date': date(2017, 7, 24),
        'currency': 'CHF',
        'amount': Decimal(10),
        'client_address': ('Alphabet Inc', 'Brandschenkestrasse 110', '8002 Zürich'),
        'recipient_iban': 'CH9300762011623852957',
        'recipient_name': 'Herr Peter Haller',
        'recipient_address': ('Marktplaz 4', '9400 Rorschach'),
        'identification_purpose': IdentificationPurpose.UNSTRUCTURED,
        'purpose': ('Reference Uniqueness Test', '', ''),
        'charges_rules': ChargesRule.OUR
    }, {
        'reference': '01234567890',
        'client_account': 'CH38 0888 8123 4567 8901 2',
        'processing_date': date(2017, 7, 24),
        'currency': 'CHF',
        'amount': Decimal(10),
        'client_address': ('Alphabet Inc', 'Brandschenkestrasse 110', '8002 Zürich'),
        'recipient_iban': 'CH9300762011623852957',
        'recipient_name': 'Herr Peter Haller',
        'recipient_address': ('Marktplaz 4', '9400 Rorschach'),
        'identification_purpose': IdentificationPurpose.UNSTRUCTURED,
        'purpose': ('Reference Uniqueness Test', '', ''),
        'charges_rules': ChargesRule.OUR
    }], (0, 1)),
    ([{
        'reference': '01234567890',
        'client_account': 'CH38 0888 8123 4567 8901 2',
        'processing_date': date(2017, 7, 24),
        'currency': 'CHF',
        'amount': Decimal(10),
        'client_address': ('Alphabet Inc', 'Brandschenkestrasse 110', '8002 Zürich'),
        'recipient_iban': 'CH9300762011623852957',
        'recipient_name': 'Herr Peter Haller',
        'recipient_address': ('Marktplaz 4', '9400 Rorschach'),
        'identification_purpose': IdentificationPurpose.UNSTRUCTURED,
        'purpose': ('Reference Uniqueness Test', '', ''),
        'charges_rules': ChargesRule.OUR
    }, {
        'reference': '01234567890',
        'client_account': 'CH38 0888 8123 4567 8901 2',
        'processing_date': date(2017, 7, 24),
        'currency': 'CHF',
        'amount': Decimal(10),
        'client_address': ('Alphabet Inc', 'Brandschenkestrasse 110', '8002 Zürich'),
        'recipient_iban': 'CH9300762011623852957',
        'recipient_name': 'Herr Peter Haller',
        'recipient_address': ('Marktplaz 4', '9400 Rorschach'),
        'identification_purpose': IdentificationPurpose.UNSTRUCTURED,
        'purpose': ('Reference Uniqueness Test', '', ''),
        'charges_rules': ChargesRule.OUR
    }, {
        'reference': '01234567890',
        'client_account': 'CH38 0888 8123 4567 8901 2',
        'processing_date': date(2017, 7, 24),
        'currency': 'CHF',
        'amount': Decimal(10),
        'client_address': ('Alphabet Inc', 'Brandschenkestrasse 110', '8002 Zürich'),
        'recipient_iban': 'CH9300762011623852957',
        'recipient_name': 'Herr Peter Haller',
        'recipient_address': ('Marktplaz 4', '9400 Rorschach'),
        'identification_purpose': IdentificationPurpose.UNSTRUCTURED,
        'purpose': ('Reference Uniqueness Test', '', ''),
        'charges_rules': ChargesRule.OUR
    }, {
        'reference': '01234567890',
        'client_account': 'CH38 0888 8123 4567 8901 2',
        'processing_date': date(2017, 7, 24),
        'currency': 'CHF',
        'amount': Decimal(10),
        'client_address': ('Alphabet Inc', 'Brandschenkestrasse 110', '8002 Zürich'),
        'recipient_iban': 'CH9300762011623852957',
        'recipient_name': 'Herr Peter Haller',
        'recipient_address': ('Marktplaz 4', '9400 Rorschach'),
        'identification_purpose': IdentificationPurpose.UNSTRUCTURED,
        'purpose': ('Reference Uniqueness Test', '', ''),
        'charges_rules': ChargesRule.OUR
    }], (0, 1, 2, 3)),
    ([{
        'reference': '01234567890',
        'client_account': 'CH38 0888 8123 4567 8901 2',
        'processing_date': date(2017, 7, 24),
        'currency': 'CHF',
        'amount': Decimal(10),
        'client_address': ('Alphabet Inc', 'Brandschenkestrasse 110', '8002 Zürich'),
        'recipient_iban': 'CH9300762011623852957',
        'recipient_name': 'Herr Peter Haller',
        'recipient_address': ('Marktplaz 4', '9400 Rorschach'),
        'identification_purpose': IdentificationPurpose.UNSTRUCTURED,
        'purpose': ('Reference Uniqueness Test', '', ''),
        'charges_rules': ChargesRule.OUR
    }, {
        'reference': '01234567890',
        'client_account': 'CH38 0888 8123 4567 8901 2',
        'processing_date': date(2017, 7, 24),
        'currency': 'CHF',
        'amount': Decimal(10),
        'client_address': ('Alphabet Inc', 'Brandschenkestrasse 110', '8002 Zürich'),
        'recipient_iban': 'CH9300762011623852957',
        'recipient_name': 'Herr Peter Haller',
        'recipient_address': ('Marktplaz 4', '9400 Rorschach'),
        'identification_purpose': IdentificationPurpose.UNSTRUCTURED,
        'purpose': ('Reference Uniqueness Test', '', ''),
        'charges_rules': ChargesRule.OUR
    }, {
        'reference': '01234567891',
        'client_account': 'CH38 0888 8123 4567 8901 2',
        'processing_date': date(2017, 7, 24),
        'currency': 'CHF',
        'amount': Decimal(10),
        'client_address': ('Alphabet Inc', 'Brandschenkestrasse 110', '8002 Zürich'),
        'recipient_iban': 'CH9300762011623852957',
        'recipient_name': 'Herr Peter Haller',
        'recipient_address': ('Marktplaz 4', '9400 Rorschach'),
        'identification_purpose': IdentificationPurpose.UNSTRUCTURED,
        'purpose': ('Reference Uniqueness Test', '', ''),
        'charges_rules': ChargesRule.OUR
    }, {
        'reference': '01234567890',
        'client_account': 'CH38 0888 8123 4567 8901 2',
        'processing_date': date(2017, 7, 24),
        'currency': 'CHF',
        'amount': Decimal(10),
        'client_address': ('Alphabet Inc', 'Brandschenkestrasse 110', '8002 Zürich'),
        'recipient_iban': 'CH9300762011623852957',
        'recipient_name': 'Herr Peter Haller',
        'recipient_address': ('Marktplaz 4', '9400 Rorschach'),
        'identification_purpose': IdentificationPurpose.UNSTRUCTURED,
        'purpose': ('Reference Uniqueness Test', '', ''),
        'charges_rules': ChargesRule.OUR
    }], (0, 1, 3))
))
def test_references_uniqueness(record_data, duplicate_record_indexes):
    """Verify the uniqueness of reference numbers within a file."""
    dta_file = DTAFile(sender_id='ABC12', client_clearing='8888')
    for record_datum in record_data:
        dta_file.add_836_record(**record_datum)

    dta_file._sort_records()  # pylint: disable=protected-access
    dta_file._set_sequence_numbers()  # pylint: disable=protected-access
    dta_file.validate()

    for idx in duplicate_record_indexes:
        record = dta_file.records[idx]
        assert (f"[reference] DUPLICATE TRANSACTION NUMBER: reference '{record.reference}' is present more than once."
                in record.validation_errors), f"Reference number '{record.reference}' is not unique within the file."


def test_no_records():
    dta_file = DTAFile(sender_id='ABC12', client_clearing='8888')
    assert not dta_file.validate(), "Empty DTA file should be invalid"
    assert not dta_file.records, "Empty DTA should be empty"


def test_add_890_record():
    dta_file = DTAFile(sender_id='ABC12', client_clearing='8888')
    dta_record = DTARecord890()
    with pytest.raises(ValueError) as excinfo:
        dta_file.add_record(dta_record)
        print(dta_file.records)
        assert str(excinfo.value) == ('Adding invalid record: TA 890 record is generated '
                                      'automatically and should not be added.')
    assert not dta_file.records, "The record shouldn't be added"


def test_invalid_record_sequence_nr():
    dta_file = DTAFile(sender_id='ABC12', client_clearing='8888')
    dta_record = DTARecord836()
    dta_record1 = DTARecord836()
    dta_file.add_record(dta_record)
    dta_file.add_record(dta_record1)
    dta_file.records[1].header.sequence_nr = 8
    assert not dta_file.validate(), "The file shouldn't be valid"
    assert ("[sequence_nr] SEQUENCE ERROR: Must be consecutive commencing with 1 in ascending order. "
            "(expected 2, got 8)") in dta_file.records[1].header.validation_errors

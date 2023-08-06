"""Standard header for any DTA record type."""
from datetime import datetime, timedelta

from swissdta.constants import FillSide, PaymentType
from swissdta.fields import AlphaNumeric, Date, Numeric
from swissdta.records.common import ValidationLogMixin


class DTAHeader(ValidationLogMixin):
    """Standard header for any DTA record type.

    Attributes:
        processing_date: Requested processing date; This field
            must be completed with the requested processing date
            for TA 826 and TA 827. Enter zeros for other types of
            transaction, as the value-date is mentioned in field 32A.
        recipient_clearing: Bank clearing no. of the beneficiary's bank
            For TA 827 bank payments, this field must contain
            the bank clearing no. of the beneficiary's
            bank if payment is made to a clearing bank.

            For TA 827 payments made to a postal account
            or for postal orders instructions (TA
            827 too), this field must remain blanks.

            For all other transaction types (TA 826, 830, 832,
            836, 837, 890), this field must remain blanks.
        creation_date: Date when data file was created.
            Must be the same for all data records.
        client_clearing: Bank clearing no. of the ordering party's
            bank. For TA 890 (Total record), this field must be
            completed with blanks. The BC no. is to be entered without
            punctuation.
        sender_id: Identification must be included as a means
            of identifying the sender of the data file. The same
            identification must be included for all records.
        sequence_nr: All records for each data file must
            be numbered sequentially starting with 00001.
        transaction_type: Record transaction type
        payment_type: Indicate salary and pension payments
            TA 827, 836 and 837 with code ``PaymentType.SALARY``
            (``'1'``). Enter code ``PaymentType.REGULAR`` (``'0'``)
            for all other payments including pension payments.
    """
    processing_date = Date()
    recipient_clearing = AlphaNumeric(length=12)
    creation_date = Date()
    client_clearing = AlphaNumeric(length=7)
    sender_id = AlphaNumeric(length=5)
    sequence_nr = Numeric(length=5, fillchar='0', fillside=FillSide.LEFT)
    transaction_type = Numeric(length=3)
    payment_type = Numeric(length=1, default=PaymentType.REGULAR, allowed_values=PaymentType)

    _template = ('{processing_date}{recipient_clearing}00000'
                 '{creation_date}{client_clearing}{sender_id}{sequence_nr}{transaction_type}{payment_type}0')

    def generate(self) -> str:
        """Generate the record's heder as a string.

        The returned value is a simple string. Make sure
        to encode it to the ISO Latincode 8859-1 format
        in accordance with the DTA Standard and Formats.

        Returns: A record's header as a string.
        """
        return self._template.format(
            processing_date=self.processing_date,
            recipient_clearing=self.recipient_clearing,
            creation_date=self.creation_date,
            client_clearing=self.client_clearing,
            sender_id=self.sender_id,
            sequence_nr=self.sequence_nr,
            transaction_type=self.transaction_type,
            payment_type=self.payment_type
        )

    def validate(self) -> None:
        """Validate the field's value of the header.

        Warnings and errors are then exposed through the
        ``validation_warnings`` and ``validation_errors`` properties.
        The ``has_warnings`` and ``has_errors`` properties should
        be used to test for the presence of warnings or errors.
        """
        now = datetime.now()
        earliest_valid_creation_date = now - timedelta(days=90)
        latest_valid_creation_date = now + timedelta(days=90)
        try:
            creation_date = datetime.strptime(self.creation_date, Date.DATE_FORMAT)
        except ValueError:
            self.add_error('creation_date', "INVALID: must contain a valid date.")
        else:
            if not earliest_valid_creation_date < creation_date < latest_valid_creation_date:
                self.add_error('creation_date', "INVALID: creation date may not differ by +/- 90 calendar days"
                                                " from the date when read in.")

        # XXX Properly validate bank clearing no. of the client can only be done with a reliable and up to date
        # database of bank clearing numbers, which is difficult to obtain.

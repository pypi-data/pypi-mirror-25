"""Implementation of the TA 890 total record"""
from swissdta.fields import Amount
from swissdta.records.record import DTARecord


class DTARecord890(DTARecord):
    """TA 890 Total record implementation

    TA 890 is only generated once for a data file
    and must be displayed as the final record. It
    contains the total for all submitted payments.

    Note that this library takes care of automatically generating a TA 890

    Attributes:
        amount: A control total (max. 16-digit amount incl. mandatory
            comma) must be generated for each data file. All payment
            record amounts will be added together taking account of the
            comma, regardless of the currency. A maximum of 3 decimal
            places is permitted.
    """
    amount = Amount(length=16)

    _template = '01{header}{amount}{padding:<59}\r\n'

    def __init__(self):
        super().__init__()
        self.header.transaction_type = 890

    def generate(self) -> str:
        """Generate a TA 890 record as a string.

        The returned value is a simple string. Make sure
        to encode it to the ISO Latincode 8859-1 format
        in accordance with the DTA Standard and Formats.

        Returns: A TA 890 record as a string.
        """
        return self._template.format(header=self.header.generate(), amount=self.amount, padding='')

    def validate(self) -> None:
        super().validate()

        if self.header.transaction_type != '890':
            self.header.add_error('transaction_type', "INVALID: Transaction type must be TA 890.")

        if self.header.client_clearing.strip():
            self.header.add_error('client_clearing', 'INVALID: must be completed with blanks')

        decimal_places = len(self.amount.strip().split(',', maxsplit=1)[1])
        if decimal_places > 3:
            self.add_error('amount',
                           "MORE THAN 3 DECIMAL PLACES: Total amount may not contain more than 3 decimal places.")

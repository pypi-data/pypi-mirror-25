"""Base class for DTA TA records"""

from itertools import chain
from typing import Tuple

from swissdta.records.common import ValidationLogMixin
from swissdta.records.header import DTAHeader


class DTARecord(ValidationLogMixin):
    """Base class for DTA TA records.

    This class should not be instantiated directly but subclassed
    instead. It automatically generates a empty header required for all
    types of records.

    The constructor (of this class and its children) should not accept
    record values. All fields should be set after initialization and
    all field attributes must use a subclass of `dta.fields.Field`.
    """
    def __init__(self):
        super().__init__()
        self.header = DTAHeader()

    @property
    def validation_warnings(self) -> Tuple[str, ...]:
        """~ValidationLog.validation_warnings"""
        return tuple(warning for warning in chain(self.header.validation_warnings, super().validation_warnings))

    @property
    def validation_errors(self) -> Tuple[str, ...]:
        """~ValidationLog.validation_errors"""
        return tuple(error for error in chain(self.header.validation_errors, super().validation_errors))

    def has_warnings(self) -> bool:
        """~ValidationLog.has_warnings"""
        return self.header.has_warnings() or super().has_warnings()

    def has_errors(self) -> bool:
        """~ValidationLog.has_errors"""
        return self.header.has_errors() or super().has_errors()

    def validate(self) -> None:
        """Triggers the validation of the record.

        This validate the data in the record according to the
        validation defined in the `DTA Standards and Formats`_.

        Warnings and errors are then exposed through the
        ``validation_warnings`` and ``validation_errors`` properties.
        The ``has_warnings`` and ``has_errors`` properties should
        be used to test for the presence of warnings or errors.

        .. _DTA Standards and Formats:
            https://www.six-interbank-clearing.com/dam/downloads/en/standardization/dta/dta.pdf
        """
        self.header.validate()

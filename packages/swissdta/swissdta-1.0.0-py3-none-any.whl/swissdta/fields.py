"""DTA Record fields definitions.

The fields module contains the definitions of all the fields used by DTA Records.
"""
from datetime import date
from enum import Enum, EnumMeta

from decimal import Decimal
from typing import List
from weakref import WeakKeyDictionary

from iso4217 import Currency as CurrencyCode
from schwifty import IBAN

from swissdta.constants import CONVERTED_CHARACTERS, FillSide

# pylint: disable=useless-super-delegation, too-few-public-methods
# useless-super-delegation disabled as it clashes with type annotations
# too-few-public-methods disabled as each field defines a different behavior
# but doesn't need to redefine its public API
from swissdta.records.common import ValidationLogMixin


class Field(object):
    """Generic DTA Field.

    This class should be subclassed into specific fields.
    """
    def __init__(self, length: int, default=None, fillchar: str = ' ', fillside: FillSide = FillSide.RIGHT):
        """Initialize a generic field.

        Initialize a generic fields. This is a class
        descriptor, instances must be attribute of another
        class; specifically an instance of ValidationHandler.

        Args:
            length: The length of the field
            default: The default value for the field
            fillchar: The character to use to fill the width of the field in case the value is less than the length.
            fillside: The side of the value to fill with the ``fillchar``.
        """
        self.length = length
        self.data = WeakKeyDictionary()
        self.default = default
        self.fillchar = fillchar
        self.fillside = fillside
        self.name = None

    def __set_name__(self, _, name: str) -> None:
        self.name = name

    def __get__(self, instance: ValidationLogMixin, _) -> str:
        return self._format_value(self.data.get(instance, self.default)) if instance is not None else self

    def __set__(self, instance: ValidationLogMixin, value) -> None:
        instance.set_warnings(self.name)  # remove all warnings on new value
        instance.set_errors(self.name, *self.validate(value))
        self.data[instance] = value

    def __repr__(self) -> str:
        name = self.name if self.name else 'UNREGISTERED'
        return f'<{self.__class__.__name__}(length={self.length}, name={name})>'

    def _format_value(self, value: str) -> str:
        if self.fillside == FillSide.LEFT:
            return (value if value is not None else '').rjust(self.length, self.fillchar)
        elif self.fillside == FillSide.RIGHT:
            return (value if value is not None else '').ljust(self.length, self.fillchar)

    def validate(self, value) -> List[str]:
        """Validate the value of a field.

        This base validation only validates the length, children should
        override this method with validation specific to their field.
        However they must call this base method to validate the length.

        Validation is done on the formatted value because some raw values
        may be incorrect but should be converted to correct values via
        formatting. For example automatic padding/truncating or formatting
        of date objects.

        Args:
            value: The value to validate (usually a new value to set)

        Returns: An array of validation errors (empty if no errors)
        """
        formatted_value = self._format_value(value)
        if len(formatted_value) > self.length:
            return [f"TOO LONG: '{formatted_value}' can be at most {self.length} characters"]
        return []


class AllowedValuesMixin(object):
    """Field mixin to validate a value against a set of allowed values.

    This mixin adds the ``allowed_values`` kwarg to the
    initializer to set the sequence of allowed values and
    a validation to check values against this sequence.
    """
    def __init__(self, *args, **kwargs):  # pylint: disable=differing-param-doc
        """Instantiate a field with a set of allowed values for validation.

        Args:
            allowed_values: A sequence or ``Enum`` of allowed values
        """
        self.allowed_values = kwargs.pop('allowed_values', set())
        if isinstance(self.allowed_values, EnumMeta):
            self.allowed_values = set(item.value for item in self.allowed_values)

        if isinstance(kwargs.get('value'), Enum):
            kwargs['value'] = kwargs['value'].value

        super().__init__(*args, **kwargs)

    def __set__(self, instance, value) -> None:
        if isinstance(value, Enum):
            value = value.value
        super().__set__(instance, value)

    def validate(self, value) -> List[str]:
        """Validate a value against the set of given allowed values

        Args:
            value: the value to validate

        Returns: a list of errors including an error if the ``value`` is not in ``allowed_values``

        """
        errors = super().validate(value)
        if not self.allowed_values:
            return errors

        if value not in self.allowed_values:
            errors.append(f"INVALID: Only {self.allowed_values} permitted (got: '{value}')")

        return errors


class AlphaNumeric(AllowedValuesMixin, Field):
    """Field accepting alphanumeric characters."""
    def __init__(self, length: int, *args, truncate: bool = False, default: str = '', **kwargs):
        """Creates a new alphanumeric field.

        Note: The length is mandatory and applies to the formatted
        version of the value. This field automatically converts invalid
        characters into valid ones. Some invalid characters can be
        converted into a sequence of characters (e.g. ``ü`` into ``ue``).

        Args:
            length: The length of the field value in characters.
            truncate: Whether to truncate the value if it is over the length or not.
            default: The default alphanumeric value
        """
        self.truncate = truncate
        super().__init__(length, *args, default=default, **kwargs)

    def __set__(self, instance: ValidationLogMixin, value: str) -> None:
        if hasattr(value, 'value'):  # Ugly but needed before calling super and super is where this happens
            value = value.value

        value = ''.join(CONVERTED_CHARACTERS.get(ord(char), char) for char in value)

        if self.truncate and len(value) > self.length:  # if truncate is True, value is truncated automatically
            old_value = value                           # and will always be of valid length
            value = value[:self.length]
        else:
            old_value = False

        super(AlphaNumeric, self).__set__(instance, value)

        if old_value:  # must add the warning after call to super which set the initial warnings and errors
            instance.add_warning(self.name,
                                 f"WARNING: '{old_value}' over {self.length} characters long, truncating to '{value}'")


class Numeric(AllowedValuesMixin, Field):
    """Field accepting only numeric characters."""
    def __init__(self, length: int, *args, default: int = None, **kwargs):
        """Creates a new numeric field.
        Args:
            length: The length of the field value in characters.
            default: The default numeric value
        """
        super().__init__(length, *args, default=default, **kwargs)

    def __set__(self, instance: ValidationLogMixin, value: int) -> None:
        super().__set__(instance, value)

    def _format_value(self, value: int) -> str:
        return super()._format_value(f'{value}')

    def validate(self, value: int) -> List[str]:
        """Validate that the value only contains numeric characters.

        Args:
            value: The value to validate
        """
        errors = super().validate(value)
        if not isinstance(value, int) and not str(value).isdigit():
            errors.append(f"NOT NUMERICAL: Only digits allowed (got: '{value}')")
        return errors


class Amount(Field):
    """Field representing an amount."""
    def __init__(self, length: int, *args, default: Decimal = Decimal(0), **kwargs):
        """Creates a new amount field.

        Use the ``Decimal`` type to pass values to the amount to
        avoid precision errors. The length refers to the number of
        characters in the which my differ from the value originally
        passed (e.g. ``'10'`` and ``'10.00'`` both become ``'10,'``).

        Args:
            length: The length of the field value in characters.
            default: The default amount value
        """
        super().__init__(length, *args, default=default, **kwargs)

    def __set__(self, instance, value: Decimal) -> None:
        super().__set__(instance, value)

    def _format_value(self, value: Decimal) -> str:
        if value is None:
            formatted_amount = value
        else:
            _, digits, exp = value.as_tuple()

            if exp == 0:
                formatted_amount = f'{value},'
            else:
                integers = ''.join(f'{d}' for d in digits[:exp])
                decimals = ''.join(f'{d}' for d in digits[exp:])
                formatted_amount = f'{integers},{decimals}'
        return super()._format_value(formatted_amount)

    def validate(self, value: Decimal) -> List[str]:
        """Validate that the value is positive.

        The value must be ``Decimal``.
        """
        errors = super().validate(value)
        if value is None:
            return errors

        if value.is_zero():
            errors.append('INVALID: May not be zero')
        elif value.is_signed():
            errors.append('INVALID: May not be negative')
        return errors


class Currency(Field):
    """Field representing an ISO 4217 currency code."""
    def __init__(self, length=3, *args, default: str = None, **kwargs):
        """Creates a new currency field.

        Args:
            length: The length in characters of the field. This should
                usually be left to 3 as defined in ISO 4217.
            default: The default currency code as a string.
        """
        super().__init__(length, *args, default=default, **kwargs)

    def __set__(self, instance, value: str) -> None:
        super().__set__(instance, value.upper() if value is not None else value)

    def validate(self, value: str) -> List[str]:
        """Validate that the value is a valid ISO 4217 currency code."""
        errors = super(Currency, self).validate(value)
        try:
            CurrencyCode(value)
        except ValueError:
            errors.append(f"INVALID: Must contain a valid ISO currency code. (got: '{value}')")

        return errors


class Iban(Field):
    """Field representing an IBAN."""
    def __init__(self, length: int, *args, default: str = None, **kwargs):
        """Creates a new IBAN field.

        The length correspond to the formatted version of the
        IBAN which is compact (without space). Both versions,
        compact and with spaces can be passed as a value.

        Args:
            length: The length of the field value in characters.
            default: The default numeric value
        """
        super().__init__(length, *args, default=default, **kwargs)

    def __set__(self, instance, value: str) -> None:
        super().__set__(instance, IBAN(value, allow_invalid=True))

    def validate(self, value: IBAN) -> List[str]:
        """Validate the IBAN value.

        Warning: Some invalid IBANs can pass this validation.
        Specifically, the SWIFT/BIC number of the bank is
        not verified to be valid. A crafted IBAN value
        with a correct checksum but fake BIC slip through.

        Args:
            value: The IBAN value to validate.
        """
        errors = super().validate(value)
        try:
            value.validate()
        except ValueError as err:
            errors.append(f"IBAN INVALID: {err}")

        return errors

    def _format_value(self, value: IBAN) -> str:
        return super()._format_value(value.compact if hasattr(value, 'compact') else value)


class Date(Field):
    """Field representing a date."""
    DATE_FORMAT = '%y%m%d'
    NULL_DATE = '000000'

    def __init__(self, length=6, *args, default: date = None, **kwargs):
        """Creates a new date field.

        The length should usually remain at 6 and should not be less.
        DTA Standards and Formats specifies that dates should have the
        following format: YYMMDD.

        Values passed to the field should be ``date`` objects or ``None``
        for the special "date" ``000000``.

        Args:
            length: The length of the date field in characters (usu. 6 for the format YYMMDD)
            default: The default date
        """
        super().__init__(length, *args, default=default, **kwargs)

    def __set__(self, instance, value: date) -> None:
        super().__set__(instance, value)

    def validate(self, value) -> List[str]:
        """Validates whether the ``value`` is a ``date`` object or ``None``."""
        errors = super().validate(value)
        if value is not None and not isinstance(value, date):
            errors.append(f"INVALID: date must contain a valid date or None ({self.NULL_DATE}).")
        return errors

    def _format_value(self, value: date) -> str:
        if value is None:
            formatted_date = self.NULL_DATE
        elif isinstance(value, date):  # Date field must conform to the format YYMMDD (year, month, day)
            formatted_date = value.strftime(self.DATE_FORMAT)
        else:
            formatted_date = str(value)

        return super()._format_value(formatted_date)

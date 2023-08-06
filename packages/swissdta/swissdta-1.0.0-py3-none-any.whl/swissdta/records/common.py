"""Common implementation to all DTA record"""
from collections import defaultdict
from typing import Tuple


class ValidationLogMixin(object):
    """Mixin class to handle a record's warnings/errors.

    Mixin class to handle the aggregation and flow
    of warnings and errors for records, header, ...
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__validation_warnings = defaultdict(list)
        self.__validation_errors = defaultdict(list)

    @property
    def validation_warnings(self) -> Tuple[str, ...]:
        """Return a flat list of all the warnings for all of the fields."""
        return tuple(warning for warnings in self.__validation_warnings.values() for warning in warnings)

    @property
    def validation_errors(self) -> Tuple[str, ...]:
        """Return a flat list of all the errors for all of the fields."""
        return tuple(error for errors in self.__validation_errors.values() for error in errors)

    def add_warning(self, field_name: str, warning: str) -> None:
        """Add a warning for a specific field.

        Args:
            field_name: The name of the field to which the warning applies.
            warning: The warning for the field.
        """
        self.__validation_warnings[field_name].append(f'[{field_name}] {warning}')

    def set_warnings(self, field_name: str, *warnings: str) -> None:
        """Overwrite the warnings for a given field.

        Calling the method without any warnings:
        ``record.set_warnings(field.name)`` is the
        recommended method to clear the warnings for a field.

        Args:
            field_name: The name of the field to overwrite or set the warnings.
            *warnings: The warnings to set.
        """
        self.__validation_warnings[field_name] = [f'[{field_name}] {warning}' for warning in warnings]

    def add_error(self, field_name: str, error: str) -> None:
        """Add a error for a specific field.

        Args:
            field_name: The name of the field to which the error applies.
            error: The warning for the field.
        """
        self.__validation_errors[field_name].append(f'[{field_name}] {error}')

    def set_errors(self, field_name: str, *errors: str) -> None:
        """Overwrite the errors for a given field.

        Calling the method without any errors:
        ``record.set_errors(field.name)`` is the
        recommended method to clear the errors for a field.

        Args:
            field_name: The name of the field to overwrite or set the errors.
            *errors: The errors to set.
        """
        self.__validation_errors[field_name] = [f'[{field_name}] {error}' for error in errors]

    def has_warnings(self) -> bool:
        """Utility method to indicate whether any warnings have been recorded."""
        return any(self.__validation_warnings.values())

    def has_errors(self) -> bool:
        """Utility method to indicate whether any errors have been recorded."""
        return any(self.__validation_errors.values())

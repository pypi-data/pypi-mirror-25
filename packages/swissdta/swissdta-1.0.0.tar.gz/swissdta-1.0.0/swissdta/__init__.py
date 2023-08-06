"""This package provides an API to generate DTA record files.

For most use cases, only the ``DTAFile`` is needed.
"""

from swissdta.constants import ChargesRule, IdentificationBankAddress, IdentificationPurpose
from swissdta.file import DTAFile
from swissdta.records import DTARecord836


__all__ = ['ChargesRule', 'DTAFile', 'DTARecord836', 'IdentificationBankAddress', 'IdentificationPurpose']

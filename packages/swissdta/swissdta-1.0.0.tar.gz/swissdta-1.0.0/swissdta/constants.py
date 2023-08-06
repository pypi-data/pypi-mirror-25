"""Constants used accross the dta library.

The ``Enum`` classes provide valid values for
specific fields and should be used for clarity.
"""
from enum import Enum, IntEnum


class FillSide(IntEnum):
    """Indicates on which side to put the padding for a field's value."""
    LEFT = 0
    RIGHT = 1


class PaymentType(IntEnum):
    """Enumerate the type of payments.

    This is used for the payment type field in the header.
    """
    REGULAR = 0
    SALARY = 1


class IdentificationBankAddress(Enum):
    """Enumerates the types of bank addresses a payment can have."""
    BIC_ADDRESS = 'A'
    SWIFT_ADDRESS = 'A'
    BENEFICIARY_ADDRESS = 'D'


class IdentificationPurpose(Enum):
    """Enumerates the types of payment purposes."""
    STRUCTURED = 'I'
    UNSTRUCTURED = 'U'


class ChargesRule(IntEnum):
    """Enumerate the rules for payment charges.

    Attributes:
        OUR: All charges debited to the ordering party
        BEN: All charges debited to the beneficiary
        SHA: Charges split
    """
    OUR = 0
    BEN = 1
    SHA = 2


CONVERTED_CHARACTERS = {
    0: '.',
    1: '.',
    2: '.',
    3: '.',
    4: '.',
    5: '.',
    6: '.',
    7: '.',
    8: '.',
    9: '.',
    10: '.',
    11: '.',
    12: '.',
    13: '.',
    14: '.',
    15: '.',
    16: '.',
    17: '.',
    18: '.',
    19: '.',
    20: '.',
    21: '.',
    22: '.',
    23: '.',
    24: '.',
    25: '.',
    26: '.',
    27: '.',
    28: '.',
    29: '.',
    30: '.',
    31: '.',
    33: '',
    34: '',
    35: '',
    36: '',
    37: '',
    38: '+',
    42: '',
    59: '',
    60: '',
    61: '',
    62: '',
    64: '',
    91: '',
    92: '',
    93: '',
    94: '',
    95: '',
    96: '',
    123: '',
    124: '',
    125: '',
    126: '',
    127: '',
    128: ' ',
    129: ' ',
    130: ' ',
    131: ' ',
    132: ' ',
    133: ' ',
    134: ' ',
    135: ' ',
    136: ' ',
    137: ' ',
    138: ' ',
    139: ' ',
    140: ' ',
    141: ' ',
    142: ' ',
    143: ' ',
    144: ' ',
    145: ' ',
    146: ' ',
    147: ' ',
    148: ' ',
    149: ' ',
    150: ' ',
    151: ' ',
    152: ' ',
    153: ' ',
    154: ' ',
    155: ' ',
    156: ' ',
    157: ' ',
    158: ' ',
    159: ' ',
    160: '',
    161: '',
    162: '',
    163: '',
    164: '',
    165: '',
    166: '',
    167: '',
    168: '',
    169: '',
    170: '',
    171: '',
    172: '',
    173: '',
    174: '',
    175: '',
    176: '',
    177: '',
    178: '',
    179: '',
    180: '',
    181: '',
    182: '',
    183: '',
    184: '',
    185: '',
    186: '',
    187: '',
    188: '',
    189: '',
    190: '',
    191: '',
    192: 'A',
    193: 'A',
    194: 'A',
    195: 'A',
    196: 'AE',
    197: 'A',
    198: 'AE',
    199: 'C',
    200: 'E',
    201: 'E',
    202: 'E',
    203: 'E',
    204: 'I',
    205: 'I',
    206: 'I',
    207: 'I',
    208: '',
    209: 'N',
    210: 'O',
    211: 'O',
    212: 'O',
    213: 'O',
    214: 'OE',
    215: '',
    216: '',
    217: 'U',
    218: 'U',
    219: 'U',
    220: 'UE',
    221: 'Y',
    222: '',
    223: 'ss',
    224: 'a',
    225: 'a',
    226: 'a',
    227: 'a',
    228: 'ae',
    229: 'a',
    230: 'ae',
    231: 'c',
    232: 'e',
    233: 'e',
    234: 'e',
    235: 'e',
    236: 'i',
    237: 'i',
    238: 'i',
    239: 'i',
    240: '',
    241: 'n',
    242: 'o',
    243: 'o',
    244: 'o',
    245: 'o',
    246: 'oe',
    247: '',
    248: '',
    249: 'u',
    250: 'u',
    251: 'u',
    252: 'ue',
    253: 'y',
    254: '',
    255: 'y'
}
"""dict of int: str: Characters of alphanumeric field's values which need to be converted.

The key is the Unicode code point of the character to convert
The value is the converted character.
Characters not in the mapping should not be converted"""

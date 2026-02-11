# We need to init so Python knows that the folder is a module and we can import within it,
# but it's also a really good place to store variables that could be used
# all over the module

from enum import Enum

class EthnicSubcategories(Enum):
    WBRI = "White"
    WIRI = "White"
    WIRT = "White"
    WROM = "White"
    WOTH = "White"
    MWBC = "Mixed"
    MWBA = "Mixed"
    MWAS = "Mixed"
    MOTH = "Mixed"
    AIND = "Asian"
    APKN = "Asian"
    ABAN = "Asian"
    AOTH = "Asian"
    BCRB = "Black"
    BAFR = "Black"
    BOTH = "Black"
    CHNE = "Chinese"
    OOTH = "Other"
    REFU = "Refused"
    NOBT = "Not Obtained"

class DateCols903(Enum):
    cols = [
        'DOB',
        'DATE_INT',
        'DATE_MATCH',
        'DECOM',
        'DEC',
        'MC_DOB',
        'MOTHER',
        'MIS_START',
        'MIS_END',
        'DATE_PLACED',
        'DATE_PLACED_CEASED',
        'DATE_PERM',
        'REVIEW',
        'DUC'
    ]
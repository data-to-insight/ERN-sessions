from enum import Enum

class DateCols903(Enum):
    cols = [
        "DOB",
        "DATE_INT",
        "DATE_MATCH",
        "DECOM",
        "DEC",
        "MC_DOB",
        "MIS_START",
        "MIS_END",
        "DATE_PLACED",
        "DATE_PLACED_CEASED",
        "DATE_PERM",
        "REVIEW",
        "DUC",
    ]    

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
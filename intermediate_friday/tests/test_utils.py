import pytest
from utils import format_dates, clean_903_table
from config_903 import *
import pandas as pd
from pandas.api.types import is_datetime64_any_dtype as is_datetime
from datetime import datetime

def test_format_dates():
    dates_df = pd.DataFrame(
        {
            "DMY": ["01/01/2025", pd.NA],
            "YMD": ["2025/01/01", pd.NA],
            "NaT": [pd.NA, pd.NA],
            "Error Col": ["01012025", "Error"],
        }
    )

    dmy_test_col = pd.Series([pd.to_datetime("01/01/2025", format="%d/%m/%Y"), pd.NaT])
    dmy_col = format_dates(dates_df["DMY"])
    pd.testing.assert_series_equal(dmy_test_col, dmy_col, check_names=False)

    nat_test_col = pd.Series([pd.NaT, pd.NaT])
    nat_col = format_dates(dates_df['NaT'])
    pd.testing.assert_series_equal(nat_test_col, nat_col, check_names=False)

    with pytest.raises(Exception):
        format_dates(dates_df["Error Col"])

    with pytest.raises(Exception):
        format_dates(dates_df["YMD"])


def test_clean_903_table(dummy_header):
    collection_end = datetime(2025, 3, 31)

    output = clean_903_table(dummy_header, collection_end)

    expected_df = pd.DataFrame(
        {
            "ETHNICITY":["White", "Mixed", "Not Obtained", "Mixed"],
            "AGE":[31, 28, 2, 0],
            "AGE_BUCKETS":[
                "e) 16 years and over",
                "e) 16 years and over",
                "b) 1 to 4 years",
                "a) Under 1 year",
                            ],
            "MC_DOB_dt":[pd.NaT, pd.NaT, pd.NaT, pd.NaT]
        }
    )

    output = output[["ETHNICITY", "AGE", "AGE_BUCKETS", "MC_DOB_dt"]]

    pd.testing.assert_frame_equal(expected_df, output, check_names=False)
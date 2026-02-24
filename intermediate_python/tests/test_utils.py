import pytest
from utils import format_dates, clean_903_table
from config_903 import *
import pandas as pd
from pandas.api.types import is_datetime64_any_dtype as is_datetime
from datetime import datetime

# We need to make a pytest.ini file so we can find the modules we've made


def test_format_dates():
    dates_df = pd.DataFrame(
        {
            "DMY": ["01/01/2025", pd.NA],
            "YMD": ["2025/01/01", pd.NA],
            "NaT": [pd.NA, pd.NA],
            "Error Col": ["01012025", "Error"],
        }
    )

    dmy_test_date = pd.Series([pd.to_datetime("01/01/2025", format="%d/%m/%Y"), pd.NaT])

    dmy_col = format_dates(dates_df["DMY"])
    pd.testing.assert_series_equal(
        dmy_col, dmy_test_date, check_names=False, check_dtype=False
    )

    with pytest.raises(Exception):
        format_dates(dates_df["YMD"])

    nat_col = format_dates(dates_df["NaT"])
    pd.testing.assert_series_equal(
        pd.Series([pd.NaT, pd.NaT]), nat_col, check_names=False
    )

    with pytest.raises(Exception):
        format_dates(dates_df["Error Col"])


# To test that cleaning a 903 table works lets make a dummy one in conftest.py
# It would also be sensible, if we had time to make a dummy .db file with known
# errors etc to test the entire pipeline and ingress etc, or a dummy excel to use
# as our input files.

# Ideally we would also test every single part of the functionn individually
# as well as the whole.


def test_clean_903_table(dummy_header):
    collection_end = datetime(2025, 3, 31)
    output = clean_903_table(dummy_header, collection_end)

    print(output.columns)
    correct_ethnicity = ["White", "Mixed", "Not Obtained", "Mixed"]
    correct_age = [31, 28, 2, 0]
    correct_age_buckets = [
        "e) 16 years and over",
        "e) 16 years and over",
        "b) 1 to 4 years",
        "a) Under 1 year",
    ]
    correct_mc_dob_dt = [pd.NaT, pd.NaT, pd.NaT, pd.NaT]

    output_to_test = output[["ETHNICITY", "AGE", "AGE_BUCKETS", "MC_DOB_dt"]].copy()
    expected_df = pd.DataFrame(
        {
            "ETHNICITY": correct_ethnicity,
            "AGE": correct_age,
            "AGE_BUCKETS": correct_age_buckets,
            "MC_DOB_dt": correct_mc_dob_dt,
        }
    )
    # We should be testing more than this but it gives you a good picture of what we are doing
    pd.testing.assert_frame_equal(output_to_test, expected_df, check_names=False)

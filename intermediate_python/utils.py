# Remember, to be able to read in functions from other files, we need an __init__.py file
# in our directory so Python reads the folder as a module

import pandas as pd
from config_903 import EthnicSubcategories, DateCols903
from dateutil.relativedelta import relativedelta
from datetime import datetime

# Import in session 2
import numpy as np


def format_dates(column):
    # Will make dates for Y/m/d or d/m/Y
    # The 903 has set date formats so we technically don't need to do this,
    # also pd.to_datetime is intelligent and can work out date formats pretty well,
    # so it's also unnecessary, but it's good to be introduced to the idea of tye/except blocks
    try:
        column = pd.to_datetime(column, format="%d/%m/%Y", errors="coerce")
        return column
    except:
        column = pd.to_datetime(column, format="%Y/%m/%d", errors="coerce")
        return column


def calculate_age_buckets(age):
    # Used to make age buckets matching published data
    if age < 1:
        return "a ) Under 1 year"
    elif age < 5:
        return "b) 1 to 4 years"
    elif age < 10:
        return "c) 5 to 9 years"
    elif age < 16:
        return "d) 10 to 16 years"
    elif age >= 16:
        return "e) 16 years and over"
    else:
        return "f) Age error"


def clean_903_table(df: pd.DataFrame, collection_end: pd.Timestamp):
    clean_df = df.copy()

    if "index" in df.columns:
        clean_df.drop("index", axis=1, inplace=True)

    for column in clean_df.columns:
        if column in DateCols903.cols.value:
            clean_df[f"{column}_dt"] = format_dates(clean_df[column])

    if "ETHNIC" in df.columns:
        clean_df["ETHNICITY"] = clean_df["ETHNIC"].apply(
            lambda x: EthnicSubcategories[x].value
        )

    if "DOB_dt" in clean_df.columns:
        # print(clean_df['DOB_dt'].max()) - we don't need this, we can just use it to find the latest DOB
        clean_df["AGE"] = clean_df["DOB_dt"].apply(
            lambda x: relativedelta(dt1=collection_end, dt2=x).normalized().years
        )
        clean_df["AGE_BUCKETS"] = clean_df["AGE"].apply(calculate_age_buckets)

    return clean_df


########### END OF SESSION 2 ###################
def group_calculation(df, col_to_group, measure_name):
    grouped = df.groupby([col_to_group]).size()
    grouped = grouped.to_frame("Count").reset_index()
    grouped = grouped.rename(columns={col_to_group: "Value"})

    grouped["Percentage"] = (grouped["Count"] / grouped["Count"].sum()) * 100

    grouped["Measure"] = measure_name

    grouped_ordered = grouped[["Measure", "Value", "Count", "Percentage"]]

    return grouped_ordered


def time_difference(start_col, end_col, business_days=False):
    if business_days:
        time_diff = np.busday_count(
            start_col.values.astype("datetime64[D]"),
            end_col.values.astype("datetime64[D]"),
        )
    else:
        time_diff = end_col - start_col
        time_diff = time_diff / pd.Timedelta(days=1)

    return time_diff.astype("int")

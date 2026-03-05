import pandas as pd
from config_903 import DateCols, EthnicSubcatgories
from dateutil.relativedelta import relativedelta

def format_dates(column):
    column.replace(r"^\s*$", pd.NaT, regex=True)
    column = column.fillna(pd.NaT)
    try:
        column = pd.to_datetime(column, format="%d/%m/%Y")
        return column
    except:
        raise ValueError(f"Unknown date format in {column.name}, expected dd/mm/YYYY")

def calculate_age_buckets(age):
    # Used to make age buckets matching published data
    if age < 1:
        return "a) Under 1 year"
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



def clean_903_table(df: pd.DataFrame, collection_end: pd.Timestamp) -> pd.DataFrame:
    '''
    Takes tables from the 903 as dataframes and outputs cleaned tables.
    '''  
    clean_df = df.copy()
    
    if "index" in df.columns:
        clean_df.drop("index", axis=1, inplace=True)

    for column in clean_df.columns:
        if column in DateCols.cols.value:
            clean_df[f"{column}_dt"] = format_dates(clean_df[column])

    if "ETHNIC" in clean_df.columns:
        clean_df['ETHNICITY'] = clean_df['ETHNIC'].apply(
            lambda ethnicity: EthnicSubcatgories[ethnicity].value
        )

    if "DOB_dt" in clean_df.columns:
        clean_df['AGE'] = clean_df['DOB_dt'].apply(
            lambda dob: relativedelta(dt1=collection_end, dt2=dob).normalized().years
        )
        clean_df["AGE_BUCKETS"] = clean_df['AGE'].apply(calculate_age_buckets)

    return clean_df

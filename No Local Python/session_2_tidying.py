"""
We have some working code but it's pretty messy making it harder than it needs to be to follow.
We might want to tidy it up by putting most actions that happen in functions we can call inside
the 'if' where we run the app from. In a larger project we'd put these functions in seprate files
and call them into the 'main' file to run them when needed. It allows us to trace through
our app in a coarse grained way, and then delve into details when we need to. IF we were
a bit more advanced, we could make a class that's able to hold different types of
CS data using the same input, but that's for the future.

Let's define our variables, then functions, then write the app code. This is one standard way to do things.
"""

import streamlit as st
import pandas as pd

# Variables
# It would make sense to define the dfs variable at this point OR inside the 'if' as we won't have any
# data in. The second option would allow us to save a teeny tiny bit of memory when starting the app
# by doing it only when we need to, but it's so small it doesn't really matter. Let's do it here.
dfs = {}


# Functions
# Let's give this function a name specific to the data it ingests incase we add the ability
# to add other types later.
def ingest_cin_data(input_files):
    """
    Takes in a list of CSV files, returns them as a dict of dfs, sorted by key,
    with the key being the filename minus years and extension. The table name
    is kept to help the merge later.
    """
    dfs = {}

    for f in input_files:
        df = pd.read_csv(f)
        list_name = f.name.split("/")[-1][:-17]
        dfs[list_name] = df

    dfs = {key: dfs[key] for key in sorted(dfs.keys())}

    return dfs


def merge_cin_tables(cin_df_dict):
    '''
    Takes the dict of CIN tables, determines columns shared between
    tables, then left merges all tables to get all data in a row for 
    la and time period.
    '''
    left_df = cin_df_dict["b1_children_in_need"]
    permenant_columns = list(left_df.columns[:10])
    left_df = left_df.set_axis(
        [
            (
                f"b1_children_in_need_{column}"
                if (not column in permenant_columns)
                else column
            )
            for column in left_df.columns
        ],
        axis=1,
    )

    for key, df in cin_df_dict.items():
        if (
            ("headline_figures" not in key)
            & (key[:1] != "b1")
            & ("mid-year" not in key)
            & (key[0] != "a")
        ):
            df = df.set_axis(
                [
                    f"{key}_{column}" if (not column in permenant_columns) else column
                    for column in df.columns
                ],
                axis=1,
            )
            left_df = left_df.merge(df, how="left", on=permenant_columns)

    return left_df


def convert_df(df):
    return df.to_csv().encode("utf-8")


# App code
st.title("Benchmarking data pipeline")

files = st.file_uploader("Please upload benchmarking data", accept_multiple_files=True)

if files:
    # Now we can just pop our functions in order in the main app, making it cleaner, easier to follow,
    # easier to update later, and easier to debug.
    dfs = ingest_cin_data(files)

    cin_table = merge_cin_tables(dfs)

    csv = convert_df(cin_table)

    st.download_button(
        "Click to download wrangled data",
        csv,
        file_name="benchmarking.csv",
        mime="text/csv",
    )

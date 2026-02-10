"""
In the original sessions we set up the data to look how it does in the benchmarking tool. Now
we'll make a new function to set it up for power BI filters/slicers and make some of our
own visualisations based on that.
"""

import streamlit as st
import pandas as pd
import plotly.express as px

# Variables
# It would make sense to define the dfs variable at this point OR inside the 'if' as we won't have any
# data in. The second option would allow us to save a teeny tiny bit of memory when starting the app
# by doing it only when we need to, but it's so small it doesn't really matter. Let's do it here.


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
    """
    Takes the dict of CIN tables, determines columns shared between
    tables, then left merges all tables to get all data in a row for
    la and time period.
    """
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


def concat_cin_tables(cin_tables):
    dfs_to_concat = [
        df
        for key, df in cin_tables.items()
        if ("headline_figures" not in key)
        & (key[:1] != "b1")
        & ("mid-year" not in key)
        & (key[0] != "a")
    ]

    df = pd.concat(dfs_to_concat, axis=0)

    return df


def convert_df(df):
    return df.to_csv().encode("utf-8")


def make_chart(df, selected_measure):
    df["time_period"] = pd.to_datetime(df["time_period"], format="%Y")
    fig = px.bar(
        df, x="time_period", y=selected_measure, color="la_name", barmode="group"
    )
    st.plotly_chart(fig)


# App code
st.title("Benchmarking data pipeline")

files = st.file_uploader("Please upload benchmarking data", accept_multiple_files=True)

if files:
    # Now we can just pop our functions in order in the main app, making it cleaner, easier to follow,
    # easier to update later, and easier to debug.
    dfs = ingest_cin_data(files)

    cin_table_merged = merge_cin_tables(dfs)
    cin_tables_concat = concat_cin_tables(dfs)

    csv_merged = convert_df(cin_table_merged)
    csv_concat = convert_df(cin_tables_concat)

    st.download_button(
        "Click to download wide-form data",
        csv_merged,
        file_name="benchmarking.csv",
        mime="text/csv",
    )

    st.download_button(
        "Click to download long form data",
        csv_concat,
        file_name="benchmarking.csv",
        mime="text/csv",
    )

    la_selection = st.sidebar.multiselect(
        label="Select LAs", options=cin_tables_concat["la_name"].unique()
    )

    category_select = st.sidebar.selectbox(
        label="Select category",
        options=cin_tables_concat["category"].unique(),
    )

    vis_df = cin_tables_concat[
        (cin_tables_concat["category"] == category_select)
        & (cin_tables_concat["la_name"].isin(la_selection))
    ]

    measure_select = st.sidebar.selectbox(
        label="Select measure (this may take time to refresh after choosing category)",
        options=vis_df.dropna(how="all", axis=1).columns[11:],
    )

    make_chart(
        vis_df[["la_name", "time_period", "category", measure_select]], measure_select
    )

import streamlit as st

import pandas as pd

st.title('Benchmarking data pipeline')

# We can use
files = st.file_uploader('Please upload benchmarking data', 
                         accept_multiple_files=True)

# Set up an empty dictionary to store our dataframes in


if files:
    dfs = {}

    for f in files:

        df = pd.read_csv(f)

        # When files are uploaded in streamlit, they have a .name 
        # property, which can be used like the filepath one from glob
        list_name = f.name.split("/")[-1][:-17]#.split("_")[0]

        dfs[list_name] = df


    dfs = {key:dfs[key] for key in sorted(dfs.keys())}

    left_df = dfs['b1_children_in_need']

    permenant_columns = list(left_df.columns[:10])


    left_df = left_df.set_axis([f'b1_children_in_need_{column}' if (not column in permenant_columns) else column for column in left_df.columns], axis=1)


    for key, df in dfs.items():
        if ('headline_figures' not in key) & (key[:1] != 'b1') & ('mid-year' not in key) & (key[0] != 'a'):

            df = df.set_axis([f'{key}_{column}' if (not column in permenant_columns) else column for column in df.columns], axis=1)

            left_df = left_df.merge(df, how='left', on=permenant_columns)


    # st.write(left_df.columns)
    # st.dataframe(left_df)

    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode("utf-8")

    csv = convert_df(left_df)

    st.download_button('Click to download wrangled data', csv, file_name='benchmarking.csv', mime="text/csv")
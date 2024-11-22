import streamlit as st
import pandas as pd
import plotly.express as px

# Utility functions
def read_files(input_files):
    '''
    Takes list of CSVs, returns them as a dict of dfs sorted by key.
    The key is the filenames minus date.
    '''
    data_dict = {}
    for f in input_files:
        df = pd.read_csv(f)

        key_string = f.name.split("/")[-1][:-17]

        data_dict[key_string] = df

    data_dict = {key:data_dict[key] for key in sorted(data_dict.keys())}
    return data_dict


def cin_output_wide(cin_df_dict):
    '''
    Merges all relevant cin data to itself in wide format to make a table for
    benchamarking tool.
    '''
    left_df = cin_df_dict['b1_children_in_need']
    merge_cols = list(left_df.columns[:10])

    new_col_names = [f'b1_children_in_need_{col}' if (not col in merge_cols) else col for col in cin_df_dict['b1_children_in_need'].columns]
    left_df = left_df.set_axis(new_col_names, axis=1)

    for key, df in cin_df_dict.items():
        if (('headline_figures' not in key) &
            ('mid-year' not in key) &
            ('b1' not in key) &
            (key[0] != 'a')):

            df = df.set_axis([f'{key}_{col}' if (not col in merge_cols) else col for col in df.columns], axis=1)
            
            left_df = left_df.merge(df, how='left', on=merge_cols)

    return left_df


def cin_output_long(cin_df_dict):

    dfs_to_concat = [df for key, df in cin_df_dict.items() if 
                     ("headline_figures" not in key) &
                     ("mid-year" not in key) &
                     (key[0] != "a")]

    df = pd.concat(dfs_to_concat, axis=0)

    return df


def convert_df(df):
    return df.to_csv().encode("utf-8")

def make_chart(df, selected_measure):
    df['time_period'] = pd.to_datetime(df['time_period'], format="%Y")
    fig = px.bar(df, x='la_name', y=selected_measure, barmode='group')
    return fig


# Main app code
st.title('CIN benchmarking pipeline')

files = st.file_uploader(label='Please upload CIN data',
                 accept_multiple_files=True)

# Runs when files are uploaded
if files:
    dfs = read_files(files)

    cin_wide = cin_output_wide(dfs)
    cin_long = cin_output_long(dfs)

    wide_csv = convert_df(cin_wide)
    long_csv = convert_df(cin_long)

    # app interactivity
    st.download_button(label='Click to download wide merged data',
                       data=wide_csv,
                       file_name='wide_benchamrking.csv',
                       mime="text/csv")
    
    st.download_button(label='Click to download long merged data',
                    data=long_csv,
                    file_name='long_benchamrking.csv',
                    mime="text/csv")
    
    # slicer to choose LAs
    la_selection = st.sidebar.multiselect(label='Select year for comparison',
                                  options=sorted(cin_long['time_period'].astype(str).unique()))
    
    category_select = st.sidebar.selectbox(label='Select category',
                                           options=sorted(cin_long['category'].astype(str).unique()))
    
    # slicer to choose my category
    vis_df = cin_long[(cin_long['category'] == category_select) & (cin_long['la_name'].isin(la_selection))].copy()

    vis_df.dropna(how='all', axis=1, inplace=True)
    
    # measure_select
    measure_select = st.sidebar.selectbox(label='Select measure',
                                          options=vis_df.columns[11:])

    
    fig = make_chart(vis_df[['la_name', 'time_period', 'category', measure_select]], measure_select)

    st.plotly_chart(fig)
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Utilities
def data_cleaner(df):
    '''
    Cleans 903 header and adds age column.

    arguments:
    df -> DataFrame of 903 header data to be cleaned.

    returns:
    df -> DataFrame of 903 data with SEX correctly mapped and AGE column added.
    '''
    df['SEX'] = df['SEX'].map({1:'Male',
                               2:'Female'})
    
    df['DOB'] = pd.to_datetime(df['DOB'], format="%d/%m/%Y", errors='coerce')
    df['AGE'] = pd.to_datetime('today').normalize() - df['DOB']
    df['AGE'] = (df['AGE'] / np.timedelta64(1, 'Y')).astype('int')

    df = df[['SEX', 'AGE', 'ETHNIC']]

    return df


# Plotting functions
def age_bar(df):
    fig = px.histogram(df, 
                       x='SEX',
                       title='Breakdown by gender of 903 data',
                       labels={'SEX':'Sex of children'})
    
    return fig

def ethnicity_pie(df):
    ethnic_count = df.groupby('ETHNIC')['ETHNIC'].count().reset_index(name='count')
    
    fig = px.pie(ethnic_count,
                 values='count',
                 names='ETHNIC',
                 title='Breakdown of 903 data by ethnicity')
    
    return fig

st.title('903 header analysis tool')

upload = st.file_uploader('Please upload 903 header as a .csv')

if upload:
    st.write('File sucsesfully uploaded')

    df_upload = pd.read_csv(upload)
    df_clean = data_cleaner(df_upload)

    age_bar_fig = age_bar(df_clean)
    st.plotly_chart(age_bar_fig) 

    ethnic_pie_fig = ethnicity_pie(df_clean)
    st.plotly_chart(ethnic_pie_fig)
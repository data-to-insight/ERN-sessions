import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

def ingress(df):
    '''
    Takes uploaded data and changes SEX column to Male and Female.
    Converts DOB to datetime and caluclates age.

    arguments:
    df: DataFrame with 903 header info

    returns:
    df: DataFrame with cleaned data and added AGE column
    '''
    
    df['SEX'] = df['SEX'].map(
        {1:'Male',
         2:'Female'}
    )

    # Generates AGE column as INT
    df['DOB'] = pd.to_datetime(df['DOB'], format='%d/%m/%Y', errors='coerce')
    df['AGE'] = pd.to_datetime('today').normalize() - df['DOB']
    df['AGE'] = (df['AGE']/np.timedelta64(1, 'Y')).astype('int')

    # Tidies column
    df = df[['SEX', 'ETHNIC', 'AGE']]

    return df


def gender_plot(df):
    '''
    Takes cleaned 903 data to plot gender and ethnicity.
    '''
    fig = px.histogram(df, 
                       x='SEX',
                       color='ETHNIC',
                       title='903 Gender and Ethnicity Breakdown',
                       labels={'SEX':'Sex',
                               'ETHNIC':'Ethnicity',
                               'count':'Number of Children'})

    return fig

def ethnic_pie(df):
    '''
    Takes cleaned 903 data to plot pie chart of ethnicity breakdown
    '''
    df_count = df.groupby('ETHNIC')['ETHNIC'].count().reset_index(name='count')

    fig = px.pie(df_count, 
                 values='count', 
                 names='ETHNIC',
                 title='Ethnicity breakdown')

    return fig


st.title('903 analysis tool')

upload = st.file_uploader('Upload 903 header here')

if upload: 
    df = pd.read_csv(upload)

    df = ingress(df)
    st.dataframe(df)

    gender_fig = gender_plot(df)
    st.plotly_chart(gender_fig)

    ethnic_pie_chart = ethnic_pie(df)
    st.plotly_chart(ethnic_pie_chart)
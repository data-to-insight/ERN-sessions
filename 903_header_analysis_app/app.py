import streamlit as st

import pandas as pd
import plotly.express as px

# Utility functions
def age_bucket(dob_dt):
    today = pd.to_datetime('today')

    if dob_dt + pd.DateOffset(years=6) > today:   
        return '0-5 years' 
    elif dob_dt + pd.DateOffset(years=12) > today:
        return '6-11 years'
    elif dob_dt + pd.DateOffset(years=18) > today:
        return '12-17 years'
    else:
        return '18+ years old'

def ingress(df):
    df['SEX'] = df['SEX'].map(
        {1:'Male',
         2:'Female'}
    )

    df['DOB'] = pd.to_datetime(df['DOB'], format="%d/%m/%Y", errors='coerce')

    df['Age range'] = df['DOB'].apply(age_bucket)

    df.drop(['CHILD', 'UPN', 'MOTHER', 'MC_DOB'], axis=1, inplace=True)

    return df

# Plot functions
def gender_plot(df):
    fig = px.histogram(df, 
                       'SEX',
                       title='903 gender breakdown')
    return fig

def age_pie(df):
    fig = px.pie(df,
                 names='Age range',
                 title='903 age breakdown')
    return fig

# Main app code
st.title('903 header analysis')

file = st.file_uploader('Drag and drop 903 header file here')

if file:
    unclean_df = pd.read_csv(file)

    df = ingress(unclean_df)


    chosen_ethnicities = st.sidebar.multiselect('Select ethncities to view breakdowns by:',
                                        list(df['ETHNIC'].unique()),
                                        list(df['ETHNIC'].unique()))
    
    df = df[df['ETHNIC'].isin(chosen_ethnicities)]

    st.dataframe(df)

    gender_plot_fig = gender_plot(df)
    st.plotly_chart(gender_plot_fig)

    age_plot_fig = age_pie(df)
    st.plotly_chart(age_plot_fig)


    
    
    
 

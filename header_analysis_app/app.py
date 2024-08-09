import streamlit as st 

import pandas as pd 
import plotly.express as px

# 1. write a sidebar widget that allows users to pick breakdown based on the age ranges 
#    in the age range bucket (hint: it's like the ethnicity picker one)
# 2. write a fucntion of your own, and use it to produce a chart showing the breakdown of
#    ethnicities in your data  

##################### Utility functions ###############################
def age_check(dob):
    if dob + pd.DateOffset(years=6) > ref_date:
        return '0-5 years'
    elif dob + pd.DateOffset(years=12) > ref_date:
        return '6-11 years'
    elif dob + pd.DateOffset(years=18) > ref_date:
        return '12-17 years'
    else:
        return '18+ years'

def data_cleaner(df):
    df['SEX'] = df['SEX'].map({1:'Male',
                               2:'Female'})
    
    df['DOB'] = pd.to_datetime(df['DOB'], format="%d/%m/%Y", errors='coerce')

    df['AGE RANGE'] = df['DOB'].apply(age_check)

    df.drop(['CHILD', 'UPN', 'MOTHER', 'MC_DOB'], axis=1, inplace=True)

    ethnic_list = list(df['ETHNIC'].unique())

    return df, ethnic_list

##################### Plot Functions ##################################
def gender_plot(df):
    fig = px.histogram(df, 
                       x='SEX', 
                       title='903 cohort breakdown via sex',
                       labels={'SEX':'Sex'})
    return fig

def age_pie(df):
    fig = px.pie(df,
                 names='AGE RANGE',
                 title='903 cohort breakdown by age ranges')
    
    return fig

def ethnic_hist(df):
    fig = px.histogram(df,
                       x='ETHNIC',
                       title='Breakdown of ethnicities in data selction')
    
    return fig



##################### Main app code ###################################
st.title('903 Header Analysis Tool')

file = st.file_uploader('Please upload 903 header for analysis')

if file:
    unclean_df = pd.read_csv(file)

    ref_date = st.sidebar.date_input('Choose reference date')

    df, ethnic_list = data_cleaner(unclean_df)

    chosen_ethnicities = st.sidebar.multiselect(
        'Choose ethnicities to view breakdown by:',
                   options=ethnic_list,
                   default=ethnic_list)
    
    age_range = st.sidebar.multiselect(
        'Choose age ranges from list',
        options=list(df['AGE RANGE'].unique()),
        default=list(df['AGE RANGE'].unique())
    )

    df = df[df['AGE RANGE'].isin(age_range)]
    
    age_selection = st.sidebar.slider(
        'Choose age range for visualisations',
        min_value=0,
        max_value=25,
        value=(0, 25)
        )
    
    df = df[(ref_date - pd.DateOffset(years=age_selection[0]) >= df['DOB']) & (
       ref_date - pd.DateOffset(years=age_selection[1]) <= df['DOB'] 
    )]

    df = df[df['ETHNIC'].isin(chosen_ethnicities)]    

    st.dataframe(df)

    st.plotly_chart(gender_plot(df))
    st.plotly_chart(age_pie(df))
    st.plotly_chart(ethnic_hist(df))




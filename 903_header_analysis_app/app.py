import streamlit as st

import pandas as pd
import plotly.express as px

# Utility functions
def age_bucket(dob_dt):
    if dob_dt + pd.DateOffset(years=6) > ref_date:   
        return '0-5 years' 
    elif dob_dt + pd.DateOffset(years=12) > ref_date:
        return '6-11 years'
    elif dob_dt + pd.DateOffset(years=18) > ref_date:
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

def ethnic_hist(df):
    fig = px.histogram(df,
                       'ETHNIC',
                       title='Breakdown of ethnicities selected')
    return fig

# Main app code
st.title('903 header analysis')

file = st.file_uploader('Drag and drop 903 header file here')

if file:
    unclean_df = pd.read_csv(file)

    ref_date = st.sidebar.date_input(
        label='Set reference date',
        value=pd.to_datetime('today')
    )
    df = ingress(unclean_df)



    chosen_ethnicities = st.sidebar.multiselect('Select ethncities to view breakdowns by:',
                                        list(df['ETHNIC'].unique()),
                                        list(df['ETHNIC'].unique()))
    
    age_bucket_range = st.sidebar.multiselect(
        label='Select ages based on bucket',
        options=list(df['Age range'].unique()),
        default=list(df['Age range'].unique())
    )

    df= df[df['Age range'].isin(age_bucket_range)]



    if len(age_bucket_range) == 4:
        age_range = st.sidebar.slider(
            label='Select age range for visualisations',
            min_value=0,
            max_value=25,
            value=(0, 25)
        )    
        df = df[(ref_date - pd.DateOffset(years=age_range[0]) >= df['DOB']) & (
            ref_date - pd.DateOffset(years=age_range[1]) <= df['DOB']
        )]

        st.write(f'Lower age bound: {age_range[0]}')
        st.write(f'Upper age bound: {age_range[1]}')

    st.write(f'Selected reference date: {ref_date}')




    df = df[df['ETHNIC'].isin(chosen_ethnicities)]

    st.dataframe(df)

    gender_plot_fig = gender_plot(df)
    st.plotly_chart(gender_plot_fig)

    age_plot_fig = age_pie(df)
    st.plotly_chart(age_plot_fig)

    st.plotly_chart(ethnic_hist(df))


    
    
    
 

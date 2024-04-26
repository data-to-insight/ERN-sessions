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

    # Summary calculations
    min_age = int(df_clean['AGE'].min())
    max_age = int(df_clean['AGE'].max())

    ethnicity_list = list(df_clean['ETHNIC'].unique())

    # Slicer sliders
    age_range = st.sidebar.slider(
        label='Select age range:',
        min_value=min_age,
        max_value=max_age,
        value=[min_age, max_age]
    )

    ethnicities = st.sidebar.multiselect(
        label='Select ethnicities:',
        options=ethnicity_list,
        default=ethnicity_list
    )
    


    age_condition = (df_clean['AGE'] >= age_range[0]) & (df_clean['AGE'] <= age_range[1])
    ethnicity_condition = df_clean['ETHNIC'].isin(ethnicities)

    df_clean = df_clean[age_condition & ethnicity_condition]
    
    
    # Summary stats
    ethnic_count = df_clean.groupby('ETHNIC')['ETHNIC'].count().reset_index(name='count')
    ethnic_count.sort_values('count', ascending=False, inplace=True)
    most_represented_eth = ethnic_count.iloc[0]['ETHNIC']
    least_represented_eth = ethnic_count.iloc[-1]['ETHNIC']

    male_count = len(df_clean[df_clean['SEX'] == 'Male'])
    female_count = len(df_clean[df_clean['SEX'] == 'Female'])

        
    st.write(f'The oldest child in the data is: {max_age}, the youngest is {min_age}.')
    st.write(f'The age range selected is: {age_range[0]} to {age_range[1]}.')
    st.write(f'The most represented ethnicity is: {most_represented_eth}.')
    st.write(f'The least represented ethnicity is: {least_represented_eth}')
    st.write(f'The ratio of male to female is: {male_count / female_count}.')


    st.dataframe(df_clean) 
    
    age_bar_fig = age_bar(df_clean)
    st.plotly_chart(age_bar_fig) 

    ethnic_pie_fig = ethnicity_pie(df_clean)
    st.plotly_chart(ethnic_pie_fig)
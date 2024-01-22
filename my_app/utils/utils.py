import pandas as pd 
import json

def read_data(filepath):
    df = pd.read_csv(filepath)
    df['SEX'] = df['SEX'].map({1:'Male',
                        2:'Female'})
    return df

def number_of_children(df):
    child_count = len(df['CHILD'].unique())
    return child_count

def boys_girls_count(df):
    counts = df['SEX'].value_counts().to_json()
    counts = json.loads(counts)
    return counts['Male'], counts['Female']
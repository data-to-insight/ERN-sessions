import pandas as pd
# import json
# import pytest

from my_app.utils.utils import read_data, number_of_children, boys_girls_count

def test_boys_girls_count():
    df = pd.DataFrame([{'SEX':'Male'},
                       {'SEX':'Female'}])
    male, female = boys_girls_count(df)
   
    
    assert male == 1
    assert female == 1

def test_number_of_children():
    df = pd.DataFrame([{'CHILD':'1111'},
                       {'CHILD':'1111'},
                       {'CHILD':1112}])
    unique_children = number_of_children(df)

    assert unique_children == 2

def test_read_data():
    filepath = '/workspaces/ERN-sessions/my_app/tests/fake_header.csv'
    df = read_data(filepath)

    assert len(df) == 1
    assert df['SEX'].iloc[0] == 'Female'
   
import pytest
# run these in the cmd line using python -m pytest <filepath>


def sum_xy(x, y):
    return x + y

def prod_xy(x, y):
    return x * y

def sumprod(x, y):
    return sum_xy(x, y), prod_xy(x,y)

def addition_xy(x, y):
    if ((type(x) == float) | (type(x) == int)) & ((type(y) == float) | (type(y) == int)):
        return x + y
    elif (type(x) == str) | (type(y) == str):
        if type(x) == str:
            raise TypeError('x was a string, expected a float or int')
        if type(y) == str:
            raise TypeError('y was a string, expected a float or int')

def df_slicer(df):
    over_5 = df[df['Age'] >= 5]
    return over_5

def test_sum_xy():
    assert sum_xy(1, 1) == 2 

def test_sumprod():
    sum, prod = sumprod(1, 1)

    assert sum == 2
    assert prod == 1

def test_df_slicer():
    test_df = pd.DataFrame([{'ChildId':'child1','Age':6},
                            {'ChildId':'child3','Age':10},
                            {'ChildId':'child2','Age':4},
                            {'ChildId':'child4','Age':1},
                        ])
    sliced_df = df_slicer(test_df)

    expected_df = pd.DataFrame([
        {'ChildId':'child1','Age':6},
        {'ChildId':'child3','Age':10}
    ])
    pd.testing.assert_frame_equal(sliced_df,expected_df,check_names=False)

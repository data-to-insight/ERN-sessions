import pytest
import pandas as pd

# run these in the cmd line using python -m pytest <filepath>


######### Function and test 1
def sum_xy(x, y):
    return x + y


def test_sum_xy():
    assert sum_xy(1, 1) == 2


######## Function and test 2
def prod_xy(x, y):
    return x * y


def sumprod(x, y):
    return sum_xy(x, y), prod_xy(x, y)


def test_sumprod():
    sum, prod = sumprod(1, 1)

    assert sum == 2
    assert prod == 1


########## Function and test 3
def df_slicer(df):
    over_5 = df[df["Age"] >= 5]
    return over_5


# There are more advanced ways to do this, for instance if we are running tests on
# the same dataframe over and over we can set it as a fixture but that's a bit advanced for here
def test_df_slicer():
    test_df = pd.DataFrame(
        [
            {"ChildId": "child1", "Age": 6},
            {"ChildId": "child3", "Age": 10},
            {"ChildId": "child2", "Age": 4},
            {"ChildId": "child4", "Age": 1},
        ]
    )
    sliced_df = df_slicer(test_df)

    expected_df = pd.DataFrame(
        [{"ChildId": "child1", "Age": 6}, {"ChildId": "child3", "Age": 10}]
    )
    pd.testing.assert_frame_equal(sliced_df, expected_df, check_names=False)

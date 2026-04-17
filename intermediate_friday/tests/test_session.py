import pytest
import pandas as pd

def sum_xy(x, y):
    sum = x + y
    return sum


def test_sum_xy():
    test_output = sum_xy(x=1, y=2)
    assert test_output == 3


# Write a function that finds the product of two numbers (*)
# write a test to check that it works
def prod_xy(x, y):
    return x * y

def test_prod_xy():
    assert prod_xy(1, 3) == 3
    

def sum_prod(x, y):
    return sum_xy(x, y), prod_xy(x, y)

def test_sum_prod():
    sum, prod = sum_prod(3, 5)
    assert sum == 8
    assert prod == 15


def df_slicer(df, age):
    over_age = df[df['Age'] >= age ]
    return over_age

def test_df_slicer():
    test_df = pd.DataFrame(
        [
            {"ChildId": "child1", "Age": 6},
            {"ChildId": "child3", "Age": 10},
            {"ChildId": "child2", "Age": 4},
            {"ChildId": "child4", "Age": 1},
        ]
    )

    test_over_5 = df_slicer(test_df, 5)
    test_over_7 = df_slicer(test_df, 7)
    test_df_minus5 = df_slicer(test_df, -5)

    expect_df_over_5 = pd.DataFrame(
        [
            {"ChildId": "child1", "Age": 6},
            {"ChildId": "child3", "Age": 10}
        ]
    )

    expected_df_over_7 = pd.DataFrame(
        [
            {"ChildId": "child3", "Age": 10}
        ]
    )

    expected_minus5 = pd.DataFrame(
        [
            {"ChildId": "child1", "Age": 6},
            {"ChildId": "child3", "Age": 10},
            {"ChildId": "child2", "Age": 4},
            {"ChildId": "child4", "Age": 1},
        ]
    )

    pd.testing.assert_frame_equal(expect_df_over_5, test_over_5)
    pd.testing.assert_frame_equal(expected_df_over_7.reset_index(drop=True), test_over_7.reset_index(drop=True))
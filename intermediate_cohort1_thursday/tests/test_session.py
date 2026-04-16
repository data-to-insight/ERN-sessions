import pytest
import pandas as pd


def sum_xy(x, y):
    return x + y


def test_sum_xy():
    result = sum_xy(x=1, y=1)
    assert result == 2


# Write a function that multiplies two numbers
# write a test to check that it works!


def prod_xy(x, y):
    return x * y


def test_prod_xy():
    assert prod_xy(3, 5) == 15


def sumprod(x, y):
    return sum_xy(x, y), prod_xy(x, y)


def test_sumprod():
    sum, prod = sumprod(-4, 9)

    assert sum == 5
    assert prod == -36


def df_slicer(df, age):
    age_or_over = df[df["Age"] >= age]
    return age_or_over


def test_df_slicer():
    test_df = pd.DataFrame(
        [
            {"ChildId": "child1", "Age": 6},
            {"ChildId": "child3", "Age": 10},
            {"ChildId": "child2", "Age": 4},
            {"ChildId": "child4", "Age": 1},
        ]
    )

    sliced_df = df_slicer(test_df, 5)

    expected_df = pd.DataFrame(
        [
            {"ChildId": "child1", "Age": 6},
            {"ChildId": "child3", "Age": 10},
        ]
    )

    pd.testing.assert_frame_equal(sliced_df, expected_df, check_names=None)

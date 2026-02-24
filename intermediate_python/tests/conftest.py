import pytest
import pandas as pd


@pytest.fixture(scope="session")
def dummy_header():
    """
    This dummy header only has allowable values in so doesn't help us test that our
    code throws the correct errors/exceptions if something is formatted wrong.
    """
    dummy_header = pd.DataFrame(
        {
            "CHILD": [1, 2, 3, 4],
            "SEX": [1, 1, 2, 3],
            # When writing our test we learn that we have no way of handling missing
            # DOBs or telling the user if there are any, so again we ought to go back
            # and fix that UNLESS we are certain data coming in is clean
            "DOB": ["05/12/1993", "09/12/1996", "01/01/2023", "09/09/2025"],
            # A useful facet of testing, we realise hwen writing this df that
            # we have no way of checking that all thnicity codes are right and
            # returning errors, so we ought really to update our code
            "ETHNIC": ["WROM", "MOTH", "NOBT", "MWBA"],
            "UPN": [1, 2, 3, 4],
            "MOTHER": [pd.NA, pd.NA, pd.NA, pd.NA],
            "MC_DOB": [pd.NA, pd.NA, pd.NA, pd.NA],
        }
    )

    return dummy_header

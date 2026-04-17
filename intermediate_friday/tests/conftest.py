import pytest
import pandas as pd

@pytest.fixture(scope="session")
def dummy_header():
        dummy_header = pd.DataFrame(
        {
            "CHILD": [1, 2, 3, 4],
            "SEX": [1, 1, 2, 3],
            "DOB": ["05/12/1993", "09/12/1996", "01/01/2023", "09/09/2025"],
            "ETHNIC": ["WROM", "MOTH", "NOBT", "MWBA"],
            "UPN": [1, 2, 3, 4],
            "MOTHER": [pd.NA, pd.NA, pd.NA, pd.NA],
            "MC_DOB": [pd.NA, pd.NA, pd.NA, pd.NA],
        }
    )
        
        return dummy_header
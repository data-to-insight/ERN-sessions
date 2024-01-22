import pandas as pd 


from my_app.utils.utils import read_data, number_of_children, boys_girls_count

def run_app():
    """CLI command to run the 903 header app to return 
    basic information about the 903 ingested.

    CLI command:
    python -m my_app run <filepath>
    """
    filename = 'https://raw.githubusercontent.com/data-to-insight/csc-validator-be-903/main/tests/fake_data/header.csv'
    df = read_data(filename)
    
    child_count = number_of_children(df)
    gender_count = boys_girls_count(df)

    print(f'number of children: {child_count}')
    print(f'Counts of each gender: {gender_count}')
    

if __name__ == "__main__":
    run_app()
Install requirements using pip install -r /workspaces/ERN-sessions/my_app/requirements.txt
To update requirements use:
> pip install pipreqs
> pipreqs /workspaces/ERN-sessions/my_app

To run the app use
> python -m my_app <filepath>
eg:
python -m my_app 'https://raw.githubusercontent.com/data-to-insight/csc-validator-be-903/main/tests/fake_data/header.csv'

To test functions use:
pytest /workspaces/ERN-sessions/my_app/tests/test.py
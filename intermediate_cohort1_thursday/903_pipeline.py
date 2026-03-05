import pandas as pd
from sqlalchemy import (
    create_engine,
    inspect,
    text,
    select,
    MetaData,
    Table,
)

from utils import clean_903_table
from datetime import datetime

# Session variables
filepath = "/workspaces/ERN-sessions/intermediate_cohort1_thursday/data/903_database.db"
collection_year = 2014
collection_end = datetime(collection_year, 3, 31)

engine_903 = create_engine(f"sqlite+pysqlite:///{filepath}")
connection = engine_903.connect()


inspection = inspect(engine_903)
table_names = inspection.get_table_names()

# Uncomment to check connection to database
# print(table_names)

metadata_903 = MetaData()

dfs = {}
for table in table_names:
    current_table = Table(table, metadata_903, autoload_with=engine_903)
    with engine_903.connect() as con:
        stmt = select(current_table)
        result = con.execute(stmt).fetchall()
    dfs[table] = pd.DataFrame(result)

# Uncomment to check reading dataframes
# print(dfs.keys())
# print(dfs['header'])

for key, df in dfs.items():
    dfs[key] = clean_903_table(df, collection_end)

print(dfs['header'])
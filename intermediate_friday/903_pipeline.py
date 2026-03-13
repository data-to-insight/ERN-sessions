import pandas as pd
from sqlalchemy import (
    create_engine,
    inspect,
    text,
    select,
    MetaData,
    Table,
)

from utils import clean_903_table, group_calculation, time_difference
from datetime import datetime
from dateutil.relativedelta import relativedelta

# Initialise session variables
filepath = "/workspaces/ERN-sessions/intermediate_friday/data/903_database.db"

collection_year = 2014
collection_end = datetime(collection_year, 3, 31)


# Read in 903 data from SQL db
engine_903 = create_engine(f"sqlite+pysqlite:///{filepath}")
connection = engine_903.connect()
inspection = inspect(engine_903)

table_names = inspection.get_table_names()

# Uncomment to check database connection
# print(table_names)

metadata_903 = MetaData()

dfs = {}
for table in table_names:
    current_table = Table(table, metadata_903, autoload_with=engine_903)
    with engine_903.connect() as con:
        stmt = select(current_table)
        result = con.execute(stmt).fetchall()
    dfs[table] = pd.DataFrame(result)

# Uncomment to check reading o tables as DFs
# print(dfs.keys())
# print(dfs.values())


# Clean all tables in 903
for key, df in dfs.items():
    dfs[key] = clean_903_table(df, collection_end)

measures_dict = {}

measures_dict["Heady by Ethnicity"] = group_calculation(
    dfs["header"], "ETHNICITY", "Header - Ethnicities"
)

measures_dict["Header by Age"] = group_calculation(
    dfs["header"], "AGE_BUCKETS", "Header - Age"
)

output_table = pd.concat(list(measures_dict.values()))


# dfs['missing']['MISSING_DURATION'] = dfs['missing'].apply(
#     lambda row: relativedelta(row['MIS_START_dt'], row['MIS_END_dt']), axis=1)

dfs["missing"]["MISSING_DURATION"] = time_difference(
    dfs["missing"]["MIS_START_dt"], dfs["missing"]["MIS_END_dt"], business_days=True
)

print(dfs["missing"])

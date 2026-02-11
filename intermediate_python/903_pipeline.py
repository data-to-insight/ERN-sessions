import pandas as pd
from sqlalchemy import (
    create_engine,
    inspect,
    text,
    select,
    MetaData,
    Table,
)

# Import in session 2
from utils import clean_903_table
from datetime import datetime

# Set variables in session 2
collection_end = datetime(2025, 3, 31)

engine_903 = create_engine(
    "sqlite+pysqlite:////workspaces/ERN-sessions/intermediate_python/903_database.db"
)
connection = engine_903.connect()
inspection = inspect(engine_903)
table_names = inspection.get_table_names()

metadata_903 = MetaData()

# Initialise an empty dict to store the tables
# We can't (really really shouldn't) make a variable name from a string so,
# as well as being a good usage of memory, storing tables in a dicitonary is
# a good way to organise them by
dfs = {}
for table in table_names:
    current_table = Table(table, metadata_903, autoload_with=engine_903)
    with engine_903.connect() as con:
        stmt = select(current_table)
        result = con.execute(stmt).fetchall()
    dfs[table] = pd.DataFrame(result)

# Some national data for comparisons
national_characteristics = pd.read_excel('/workspaces/ERN-sessions/intermediate_python/national_cla_on_31_march_by_characteristics.xlsx')

################## END OF SESSION 1 ################

# Let's write a function to clean all the dfs rather than doing it one at a time
# We need to convert date columns, find ethnic main groups, etc
# Let's make a utils file, and we'll import the function from there
# We could make a utils file where we normally work and use those functions across
# pipelines or scripts.


for key, df in dfs.items():
    dfs[key] = clean_903_table(df, collection_end=collection_end)

print(dfs['header'])

########### END OF SESSION 2 ###########
import pandas as pd
from sqlalchemy import (
    create_engine,
    inspect,
    text,
    select,
    MetaData,
    Table,
)

engine_903 = create_engine(
    "sqlite+pysqlite:////workspaces/ERN-sessions/Intermediate Python/903_database.db"
)
connection = engine_903.connect()
inspection = inspect(engine_903)
table_names = inspection.get_table_names()

print(table_names)

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

print(dfs)
national_characteristics = pd.read_excel('/workspaces/ERN-sessions/Intermediate Python/national_cla_on_31_march_by_characteristics.xlsx')
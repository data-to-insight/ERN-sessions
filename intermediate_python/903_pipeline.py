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

# Import in session 3
from utils import group_calculation, time_difference
from dateutil.relativedelta import relativedelta
import numpy as np

# Set variables in session 2
collection_year = 2014
collection_end = datetime(collection_year, 3, 31)

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
national_characteristics = pd.read_excel(
    "/workspaces/ERN-sessions/intermediate_python/national_cla_on_31_march_by_characteristics.xlsx"
)

################## END OF SESSION 1 ################

# Let's write a function to clean all the dfs rather than doing it one at a time
# We need to convert date columns, find ethnic main groups, etc
# Let's make a utils file, and we'll import the function from there
# We could make a utils file where we normally work and use those functions across
# pipelines or scripts.


for key, df in dfs.items():
    dfs[key] = clean_903_table(df, collection_end=collection_end)

########### END OF SESSION 2 ###########
# If we are prepping data for Power BI/Excel we want to organise our data differently to prep for Python.
# For external dashboarding products we want everything calculated already so we can easily slice it
# and keep the dashboard nice and lightweight, not performing any calculations

# We need an ampty dict to store our measures in:
measures = {}

# Calculate groupbys
# We'll need a reusable function here that can groupby a value in a colum (e.g. ethnicity) that outputs
# in the way we want so we can reuse it every time we want to group by something

# Total CYP in header by ethnicity
# Let's do it for ethnicity then turn it into a function - let's get a count and a percent

# grouped = dfs['header'].groupby(['ETHNICITY']).size()
# grouped = grouped.to_frame('Header - Ethnicities - Count').reset_index()
# grouped = grouped.rename(columns={'ETHNICITY':'Ethnicities'})

# grouped['Header - Ethnicities - Percentage'] =  (grouped['Header - Ethnicities - Count'] / grouped['Header - Ethnicities - Count'].sum() ) * 100

# print(grouped)
# print(grouped['Header - Ethnicities - Percentage'].sum())
# Let's make the function in utils.py
measures["Header by ethnicity"] = group_calculation(
    dfs["header"], "ETHNICITY", "Header - Ethnicities"
)

# Let's show now how easy it is to do the same using our age buckets
measures["Header by age"] = group_calculation(
    dfs["header"], "AGE_BUCKETS", "Header - Age"
)


# Now let's see why we did it like htis for our final outputs.
# We won't keep this in but we will use it later
output_table = pd.concat([measures["Header by ethnicity"], measures["Header by age"]])

# Calculate time periods
# Whether we want exact numbers of buckets, we need a way to calculate time periods (e.g. time children have)
# been in a placement. It's good to have contingency for business days in there too as many CS
# measures take note of business days

# Same premise, make it as a normal calculation then turn it into a function
# dfs["missing"]["MISSING_DURATION"] = dfs["missing"].apply(
#     lambda x: relativedelta(x["MIS_START_dt"], x["MIS_END_dt"]).normalized().days, axis=1
# )

# dfs["missing"]['MISSING_DURATION'] = dfs["missing"]["MIS_END_dt"] - dfs["missing"]["MIS_START_dt"]

# or for working days:
# We need to convert these to np datetime 64s rather than pd datetimes for this calculation
# dfs["missing"]['MISSING_DURATION'] = np.busday_count(dfs["missing"]["MIS_START_dt"].values.astype('datetime64[D]'), dfs["missing"]["MIS_END_dt"].values.astype('datetime64[D]'))

dfs["missing"]["MISSING_DURATION"] = time_difference(
    dfs["missing"]["MIS_START_dt"], dfs["missing"]["MIS_END_dt"], True
)

# We might also think about making some type of function that groups this by numbers of days.
# That will depend on what we are looking at, however, for instance we might want under and over
# 45 days for assessments, but that would make no sense for placement lengths.
# We could .apply() a function like the one for age buckets in each different instance for this
print(dfs["missing"])

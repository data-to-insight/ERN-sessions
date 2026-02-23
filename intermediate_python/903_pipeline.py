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

# import in sesion 4
from utils import multiples_same_event, group_calculation_year, appears_on_both

# Set variables in session 2
collection_year = 2014
collection_end = datetime(collection_year, 3, 31)


########## SESSION 1 ###########
"""
Data retrieval and SQLALchemy
"""
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

################## SESSION 2 ####################
"""
Cleaning with functions, importing functions
"""
# Let's write a function to clean all the dfs rather than doing it one at a time
# We need to convert date columns, find ethnic main groups, etc
# Let's make a utils file, and we'll import the function from there
# We could make a utils file where we normally work and use those functions across
# pipelines or scripts.


for key, df in dfs.items():
    dfs[key] = clean_903_table(df, collection_end=collection_end)

########### END OF SESSION 2 ###########

########### SESSION 3 ############
"""
Calculating, transforming, and groupbys
"""
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


# Now let's see why we did it like this for our final outputs.
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
# print(dfs["missing"])

######## END OF SESSION 3 ################

######## SESSION 4 ##############
"""
More useful calculations inc. multiples of the same event, finding the percent of a column with a given value, 
and working with longitudinal data.
"""

# As a recap, write a function that can make buckets for durations columns using the
# calculation from the end of the last session. Do this in the util file.
# do it for buckets of 0-5 days, 6-10, 11-20, and 20+ days.


# Let's find out how to count if someone has multiples of the same event, and how many
# of each they have (e.g. episodes/missing). As always, let's write this function in
# utils.
# If we want one row for each child and their number of episodes, we'll need to put
# the result in a new table otherwise if a child has two episodes there will be a two
# each time they appear in episodes.
measures["Multiple episodes"] = multiples_same_event(
    dfs["episodes"], event_name="Number of Episodes"
)

# print(measures['Multiple episodes'])

# Ideally we'd have a 903 per year so we can compare datasets longitudinally but we don't have that
# we are going to have to fudge something so we can see how to work with longitudinal data.

# Let's add a year column to episodes so we can look at how the composition of episodes has changed
# based on DECOM- Note: - this doesn't include episodes that have been closed previous to this
# return year so you wouldn't really do this

dfs["episodes"]["DECOM_YEAR"] = dfs["episodes"]["DECOM_dt"].dt.year

# The obvious thing to look at here is episodes starting per year but that's easy as we already have the
# function for that
measures["Episodes starting per year"] = group_calculation(
    dfs["episodes"], "DECOM_YEAR", "Measures starting per year"
)
# print(measures['Episodes starting per year'])

# Lets instead look at something like how PLACE changes year on year, we can see if
# where we need provision is changing.
measures["Placements by year"] = group_calculation_year(
    dfs["episodes"], "DECOM_YEAR", "PLACE", "Placements in a year"
)
# Lets check that it works and check that our percentage by year makes sense!
# print(
#     measures["Placements by year"][
#         measures["Placements by year"]["DECOM_YEAR"] == 2015
#     ]["Percentage by year"].sum()
# )

# For the last bit of the session lets look to see how many children from the total
# appear on multiple tables. This is used a few times in the CHAT, for isntance.
appears_multiple = appears_on_both(dfs["episodes"], dfs["missing"], 'CYP with episodes who have been missing')
print(appears_multiple)


########## END OF SESSION 4 #########


########### SESSION 5 ############
'''
This session looks at writing tests
'''
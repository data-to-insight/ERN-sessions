# data here: https://explore-education-statistics.service.gov.uk/find-statistics/children-in-need

import pandas as pd
import glob
import sys

# We can use glob to identify all the files at a given filepath
# Below is a nice way to do this, we also use *.csv to say we want
# ONLY files mathcing this criteria
path = r'/workspaces/ERN-sessions/No Local Python/data'
files = glob.glob(path + "/*.csv")

# Set up an empty dictionary to store our dataframes in
dfs = {}

# Glob returns a list of file paths so we can iterate over 
# the list to read one file at a time
for f in files:
    # For each file in the list, read them in using the  
    # standard/appropriate pandas method
    df = pd.read_csv(f)
    # Glob returns strings of file paths, we can use the
    # split method on these, passing what character we want to split at
    # then selecting which element of that split we want.
    # Here I take the last element after the "/" split (the file name)
    # using [-1] and the first element after the "_" split using [0]
    # to get the list short name (eg: a1) 
    list_name = f.split("/")[-1][:-17]#.split("_")[0]
 
    # I can then use the variables list_name and df as they key/values
    # in my dictionary to store all the dfs in one easy to access palce
    # using the syntax below where list_name is a string, and df is the df
    # using the square brackets to say 'in the dfs dict, I want the value
    # associated with the string in the square brackets (the key) to be  
    # what's after the equals'
    dfs[list_name] = df

# Let's sort the dictionary to make things look like we expect later by making a 
# dictionary using a list comprehension
dfs = {key:dfs[key] for key in sorted(dfs.keys())}

# We need a df to start merging on to, and to get the columns to merge on from
left_df = dfs['b1_children_in_need']

# Get a list of the columns that are the same in every table.
# This saves writing them out by hand and if they change with publication years
# you can extract them regardless of spelling.
permenant_columns = list(left_df.columns[:10])

# Let's also add the table name as a prefix to the columns to match the original
# data and help merging later
left_df = left_df.set_axis([f'b1_children_in_need_{column}' if (not column in permenant_columns) else column for column in left_df.columns], axis=1)

# print(left_df.columns)
# sys.exit()
# lets go through all the dfs we want and merge them into the mega table we want

left_df = left_df.merge(dfs['b2_children_in_need_recorded_disability'], how='outer', on=permenant_columns)

for key, df in dfs.items():
    if ('headline_figures' not in key) & (key[:1] != 'b1') & ('mid-year' not in key) & (key[0] != 'a'):
        # Add the table name prefix to each colum again (important to understand table
        # data and to help the merge)
        df = df.set_axis([f'{key}_{column}' if (not column in permenant_columns) else column for column in df.columns], axis=1)
        print(df.columns)
        # Each loop we'll merge onto the previous left_table, gradually building
        # it up. We'll use a left merge to add the table onto the right of the previous table
        # We'll also merge on permenant_columns to a) get the right rows merged and b) so we
        # don't end up with multiple versions of the same columns from different tables.
        left_df = left_df.merge(df, how='left', on=permenant_columns)

        # We'll see that this doesn't work yet because column names are repeated 
        # across tables, let's maybe get table names in each column

print(left_df)
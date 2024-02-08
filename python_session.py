# name = 'Will'
# num_1 = 1
# num_2 = 1.0 
# list_1 = ['item1', 'item2', 'item3']
# dict_1 = {'Key1':'Value1',
#           'Key2':'Value2'}

import pandas as pd 

# List of dicts - each dict is a row, with keys being column names
# Dict of list - Each key:value pair is a column

# df_1 = pd.DataFrame([
#     {'Col1':1,
#      'Col2':2,
#      'Col3':3},
#     {'Col1':'A',
#      'Col2':'B',
#      'Col3':'C'}
# ])

# print(df_1)

filename = 'https://raw.githubusercontent.com/data-to-insight/ERN-sessions/main/data/1980%202023%20average%20house%20prices.csv'

df = pd.read_csv(filename)

df['Period'] = pd.to_datetime(df['Period'], format="%Y-%m", errors="coerce")

# format="%d/%m/%Y"

df['Age of Data (years)'] = pd.to_datetime('today').normalize() - df['Period']

df['Age of Data (years)'] = df['Age of Data (years)'] / pd.Timedelta('365 days')

df['Age of Data (years)'] = df['Age of Data (years)'].astype('int')

# print(df['Age of Data (years)'])



filename_2 = 'https://raw.githubusercontent.com/data-to-insight/ERN-sessions/main/data/ChildIdentifiers.csv'
df = pd.read_csv(filename_2)

df['PersonBirthDate'] = pd.to_datetime(df['PersonBirthDate'], format="%Y-%m-%d", errors='coerce')

df['Age'] = pd.to_datetime('today').normalize() - df['PersonBirthDate']

df['Age'] = df['Age'] / pd.Timedelta('365 Days')

df['Age'] = df['Age'].astype('int')

# == equals dates, numbers, strings
# > less numbers, dates
# < greater numbers, dates
# >= Greater/equals n, d
# <= Less/Equals n, d
# & (and) join condition
# | (or) join condition
# ~ not
# .isin([1, 2])

# condition = (df['Age'] == 15) | (df['GenderCurrent'] == 9)

max = df['Age'].max()
min = df['Age'].min()
mean = df['Age'].mean()

# print(f'max: {max}, min: {min}, mean: {mean}')

under_15_conditon = df['Age'] <= 15

conditon = ~(df['Age'] <= 15) & ~(df['GenderCurrent'].isin([0, 9]))

sliced_df = df[conditon]

# print(sliced_df)


# print(sliced_df['GenderCurrent'].unique())

# find the minimum and maximum and mean values of the Age column
# slice the df to have only children under 15
# do a different slice of df to have children that are under 15 with a gender code of either 0, 9

# .map()
# .str.lower()

df['GenderCurrent'] = df['GenderCurrent'].map({1:'Male',
                                               2:'Female'},
                                               na_action='ignore')
df['GenderCurrent'] = df['GenderCurrent'].str.lower()

print(df)
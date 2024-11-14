import pandas as pd
import glob

path = r'/workspaces/ERN-sessions/no python sessions/data'

files = glob.glob(path + "/*.csv")

dfs = {}

for f in files:
    df = pd.read_csv(f)
    
    list_name = f.split("/")[-1][:-17]

    dfs[list_name] = df

dfs = {key:dfs[key] for key in sorted(dfs.keys())}

permenant_columns = list(dfs['b1_children_in_need'].columns)[:10]

b1_columns = [f'b1_children_in_need_{column}' if (not column in permenant_columns) else column for column in dfs['b1_children_in_need'].columns]

left_df = dfs['b1_children_in_need']
left_df = left_df.set_axis(b1_columns, axis=1)

for key, df in dfs.items():
    if ('headline_figures' not in key
        ) & ('mid-year' not in key
        ) & (key[:1] != 'b1'
        ) & (key[0] != 'a'):

        df = df.set_axis([f'{key}_{column}' if (not column in permenant_columns) else column for column in df.columns], axis=1)

        left_df = left_df.merge(df, how='left', on=permenant_columns)

left_df.to_csv('benchmarking_output.csv')









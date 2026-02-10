import pandas as pd
import sqlite3


# Run this to make the 903 database file
db = sqlite3.connect("903_database.db")
dfs = pd.read_excel("/workspaces/ERN-sessions/data/903_xlsx.xlsx", sheet_name=None)
for table, df in dfs.items():
    df.to_sql(table, db)
db.commit()
db.close()

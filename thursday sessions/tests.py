import pandas as pd
from dateutil.relativedelta import relativedelta

child_identifiers = pd.read_csv(r"https://raw.githubusercontent.com/data-to-insight/ERN-sessions/main/data/ChildIdentifiers.csv")
child_characteristics = pd.read_csv(r"https://raw.githubusercontent.com/data-to-insight/ERN-sessions/main/data/ChildCharacteristics.csv")


child_identifiers["PersonBirthDate_dt"] = pd.to_datetime(child_identifiers["PersonBirthDate"], format="%Y-%m-%d", errors="coerce")

child_identifiers['Age'] = child_identifiers["PersonBirthDate_dt"].apply(
    lambda x :relativedelta(pd.to_datetime('31/03/2025', dayfirst='True'), x).years)

print(child_identifiers[["PersonBirthDate_dt", 'Age']])
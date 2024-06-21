import pandas as pd

# read from local files example
# import os
# sen_filename = r"c:\\filepath\module 2.csv"

filename = r"https://raw.githubusercontent.com/data-to-insight/ERN-sessions/main/data/1980%202023%20average%20house%20prices.csv"

# DataFrame - shorthand df

house_prices = pd.read_csv(filename)

print(house_prices)
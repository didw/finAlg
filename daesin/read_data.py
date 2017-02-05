import pandas as pd
from pandas import Series, DataFrame
import sqlite3
con = sqlite3.connect("c:/Users/jyyang/kospi.db")

readed_df = pd.read_sql("SELECT * FROM '078930'", con, index_col = 'Date')

print(readed_df)

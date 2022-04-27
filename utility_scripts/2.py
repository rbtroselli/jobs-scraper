from numpy import NaN
import pandas as pd
import csv
from langdetect import detect

df = pd.read_csv('staging_bk.csv')
print(df)

df.insert(13, 'post_language', NaN)
print(df)

for index,row in df.iterrows():
    df.loc[index, 'post_language'] = detect( df.loc[index,'description'] )
print(df)

df.to_csv('staging.csv', index=False, quoting=csv.QUOTE_ALL)
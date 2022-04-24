from numpy import NaN
import pandas as pd
import csv

df = pd.read_csv('staging.csv')
print(df)

df.insert(2, 'job_role_ext', NaN)
pd.set_option('display.max_columns', 6)
print(df)

for index,row in df.iterrows():
    if df.loc[index,'job_role'] == 'de':
        df.loc[index,'job_role_ext'] = 'data engineer'
    elif df.loc[index,'job_role'] == 'ds':
        df.loc[index,'job_role_ext'] = 'data scientist'
print(df[['job_role','job_role_ext']])

df.to_csv('staging2.csv', index=False, quoting=csv.QUOTE_ALL)
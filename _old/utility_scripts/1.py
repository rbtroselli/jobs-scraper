import pandas as pd
import csv


df = pd.read_csv('staging.csv')
# print(df)

dfde = df[ df['job_role']=='de' ].reset_index(drop=True)
# print(list(dfda.columns))
# print(dfde)
dfde = dfde[ dfde['post_title'].str.contains('data engineer', case=False)].reset_index(drop=True)
print(dfde)
dfde.to_csv('temp.csv')

dfds = df[ df['job_role']=='ds' ].reset_index(drop=True)
# print(list(dfda.columns))
# print(dfds)
dfds = dfds[ dfds['post_title'].str.contains('data scientist', case=False)].reset_index(drop=True)
print(dfds)
dfds.to_csv('temp.csv')

df = pd.concat([dfde, dfds]).reset_index(drop=True)
print(df)

df.to_csv('staging2.csv', index=False, quoting=csv.QUOTE_ALL)
import pandas as pd
import os

'''
import csv, format Date as datetime values, 
group by region and type, return dict with 
group keys and AveragePrice series sorted by date 
'''
avocadoTable = os.getcwd() + "\\avocado.csv"
df = pd.read_csv(avocadoTable)\
dated = df.assign(Date=pd.to_datetime(df['Date']))
grouped = {y: x.sort_values('Date')['AveragePrice'] for y, x in df.groupby(['region', 'type'])}

'''
for each series, calculate 10-week volatility, 
10-week coefficient of variation 
'''
vol10 = {y: x.rolling(10).std(ddof=0).rename('vol10') for y, x in grouped.items()}
cv10 = {y: x.div(grouped[y].mean()).rename('cv10') for y, x in vol10.items()}

'''
calculate mean vol10 and cv10 for TotalUS by type
'''
vol10_US = {y[1]: x.mean() for y, x in vol10.items() if y[0]=='TotalUS'}
cv10_US = {y[1]: x.mean() for y, x in cv10.items() if y[0]=='TotalUS'}

'''
for each group series, calculate 
vol10, cv10 centered to TotalUS
'''
vol10_total = {y: x.sub(vol10_US[y[1]]).rename('vol10_total') for y, x in vol10.items()}
cv10_total = {y: x.sub(cv10_US[y[1]]).rename('cv10_total') for y, x in cv10.items()}

'''
collect ('region, 'type') series data
write original table with new data to csv
'''
new = [pd.concat([y for x, y in s.items()]).sort_index() for s in [vol10, cv10, vol10_total, cv10_total]]
final = pd.concat([df, *new], axis=1)
final.to_csv(os.getcwd() + '\\avocado++.csv')


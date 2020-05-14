import pandas as pd
import os

'''
import table as dataframe, format Date as datetime object, 
sort by date, group by region and type, 
return list of tuples [(group, table)]
'''
avocadoTable = os.getcwd() + "\\avocado.csv"
df = pd.read_csv(avocadoTable)
sorted = df.assign(Date=pd.to_datetime(df['Date'])).sort_values('Date')
grouped = [x for x in sorted.groupby(['region', 'type'])]

'''
for each group table, calculate and assign
10-week volatility, 10-week coefficient of variation 
'''
vol10 = [(y, x.assign(vol10=x['AveragePrice'].rolling(10).std(ddof=0))) for (y, x) in grouped]
cv10 = [(y, x.assign(cv10=x['vol10'].div(x['AveragePrice'].mean()))) for (y, x) in vol10]

'''
calculate mean vol10 and cv10 for TotalUS,
store as dict for conventional and organic
'''
vol10_US= {y[1]: x['vol10'].mean() for (y, x) in cv10 if y[0]=='TotalUS'}
cv10_US = {y[1]: x['cv10'].mean() for (y, x) in cv10 if y[0]=='TotalUS'}


'''
for each group table, calculate and assign
vol10, cv10 relative to TotalUS (subtracted)
'''
vol10Total = [(y, x.assign(vol10Total=x['vol10'].sub(vol10_US[y[1]]))) for (y, x) in cv10]
cv10Total = [(y, x.assign(cv10Total=x['cv10'].sub(cv10_US[y[1]]))) for (y, x) in vol10Total]

'''
collect ('region, 'type') tables
sort by index
write final table to csv
'''
final = pd.concat([x[1] for x in cv10Total]).sort_index()

final.to_csv(os.getcwd() + '\\avocado++.csv')
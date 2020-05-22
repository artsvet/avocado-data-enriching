import os
import pandas as pd


'''Import and format

Format Date as datetime values, group by region and type,
return dict with group keys and AveragePrice series sorted by date. 
'''
avocado_table = os.getcwd() + "\\avocado.csv"
df = pd.read_csv(avocado_table)
dated = df.assign(Date=pd.to_datetime(df['Date']))
grouped = {
    group: table.sort_values('Date')['AveragePrice']
    for group, table in df.groupby(['region', 'type'])
}

'''New variables

For each series, calculate 10-week volatility, coefficient of variation. 
'''
vol10 = {
    group: series.rolling(10).std(ddof=0).rename('vol10')
    for group, series in grouped.items()
}
cv10 = {
    group: series.div(grouped[group].mean()).rename('cv10')
    for group, series in vol10.items()
}

'''TotalUS reference mean

Calculate mean vol10 and cv10 for TotalUS by type.
'''
vol10_US = {
    group_keys[1]: series.mean()
    for group_keys, series in vol10.items()
    if group_keys[0]=='TotalUS'
}
cv10_US = {
    group_keys[1]: series.mean()
    for group_keys, series in cv10.items()
    if group_keys[0] == 'TotalUS'
}

'''Center new variables.

For each group series, calculate vol10, cv10 centered to TotalUS.
'''
vol10_centred = {
    group: series.sub(vol10_US[group[1]]).rename('vol10_centred')
    for group, series in vol10.items()
}
cv10_centred = {
    group: series.sub(cv10_US[group[1]]).rename('cv10_centred')
    for group, series in cv10.items()
}

'''Collect and export.

Collect series data, join with original table and export.
'''
new = [
    pd.concat([series for group, series in new_columns.items()])
    for new_columns in [vol10, cv10, vol10_centred, cv10_centred]
]
final = pd.concat([df, *new], axis=1)
final.to_csv(os.getcwd() + '\\avocado++.csv')

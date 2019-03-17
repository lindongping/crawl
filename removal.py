import pandas as pd

data = pd.read_csv('data.csv', encoding='GBK')
data.drop_duplicates(u'日期', 'first', inplace=True)
data.to_csv('data.csv', index=False, encoding='GBK')




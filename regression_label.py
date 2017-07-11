# regression is used for stock markets and other fields with numbers
import pandas as pd 
import quandl
import math

df = quandl.get('WIKI/GOOGL')

#print(df.head())
df = df[['Adj. Open', 'Adj. High', 'Adj. Low', 'Adj. Close', 'Adj. Volume']]  # attributes we need to process
# Adj. = Adjust
df['HL_PCT'] = (df['Adj. High'] - df['Adj. Close']) / df['Adj. Close'] * 100.0 # high minus low percent

df['PCT_change'] = (df['Adj. Close'] - df['Adj. Open']) / df['Adj. Open'] * 100.0  # percent change

df = df[['Adj. Close', 'HL_PCT', 'PCT_change', 'Adj. Volume']]

forecast_col = 'Adj. Close'
df.fillna(-99999, inplace=True)

forecast_out = int(math.ceil(0.01*len(df)))  # wiil predict the percent at which google stock will close from Adj. Close like 30 days in advance

df['label'] = df[forecast_col].shift(-forecast_out) 
# df.dropna(inplace=True)
print(df.head())
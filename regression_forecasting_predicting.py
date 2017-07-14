# regression is used for stock markets and other fields with numbers
import numpy as np
import pandas as pd 
import quandl, math, datetime
from sklearn import preprocessing, cross_validation, svm
from sklearn.linear_model import LinearRegression 
import matplotlib.pyplot as plt
from matplotlib import style

df = quandl.get('WIKI/GOOGL')

#print(df.head())
df = df[['Adj. Open', 'Adj. High', 'Adj. Low', 'Adj. Close', 'Adj. Volume']]  # attributes we need to process
# Adj. = Adjust
df['HL_PCT'] = (df['Adj. High'] - df['Adj. Close']) / df['Adj. Close'] * 100.0 # high minus low percent

df['PCT_change'] = (df['Adj. Close'] - df['Adj. Open']) / df['Adj. Open'] * 100.0  # percent change

df = df[['Adj. Close', 'HL_PCT', 'PCT_change', 'Adj. Volume']]

forecast_col = 'Adj. Close'
df.fillna(-99999, inplace=True)

forecast_out = int(math.ceil(0.01*len(df)))
# print(forecast_out)   # number of days we are looking forward to 

df['label'] = df[forecast_col].shift(-forecast_out)   # wiil predict the percent at which google stock will close from Adj. Close

X = np.array(df.drop(['label'], 1))   # X is a feature
X = preprocessing.scale(X)
X_lately = X[-forecast_out:]
X = X[:-forecast_out]

df.dropna(inplace=True)
y = np.array(df['label'])  # y is a label

# print(len(X), len(y))

X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.2)

clf = LinearRegression(n_jobs=-1)  # number of threads u want the processor to run
# clf = svm.SVR(kernel='poly')   # support vector regression
clf.fit(X_train, y_train)

accuracy = clf.score(X_test, y_test)
# print(accuracy)

forecast_set = clf.predict(X_lately)
print(forecast_set, accuracy, forecast_out)

df['Forecast'] = np.nan

last_date = df.iloc[-1].name
last_unix = last_date.timestamp()
one_day = 86400
next_unix = last_unix + one_day

for i in forecast_set:
	next_date = datetime.datetime.fromtimestamp(next_unix)
	next_unix += one_day
	df.loc[next_date] = [np.nan for _ in range(len(df.columns)-1)] + [i]

df['Adj. Close'].plot()
df['Forecast'].plot()
plt.legend(loc=4)
plt.xlabel('Date')
plt.ylabel('Price')
plt.show()
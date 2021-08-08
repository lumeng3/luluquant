from hdly import *
from hdly_jkn import *
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures

result = pd.DataFrame()
tickers = ["BTX"]
for ticker in tickers:
    hdly_y = gethdlyjkn(ticker)
    size = hdly_y.shape[0]
    hdly_x = getRegularHDLY(ticker)
    hdly_x = hdly_x.iloc[-(size+1):-1]
    hdly_x = hdly_x.iloc[:, [3] + [-1]]
    tickerInfo = yf.Ticker("SPY")
    SPY = tickerInfo.history(period=str(size+1)+"d", interval="1d")
    SPY.drop(SPY.tail(1).index,inplace=True)
    hdly_x["SPY"] = SPY["Close"]
    hdly_x.reset_index(drop=True, inplace=True)
    hdly_x["jkn"] = hdly_y[0]

    hdly_x = hdly_x[hdly_x['final'] != 0]
   # hdly_x = hdly_x[hdly_x['final'] <100000]
    hdly_x = hdly_x[hdly_x['jkn'] != 0 ]
    result = result.append(hdly_x)


plt.scatter(result["final"], result["jkn"], alpha=0.6)  # 绘制散点图，透明度为0.6（这样颜色浅一点，比较好看）
plt.show()
#result.to_excel("/Users/menglu/Desktop/output.xlsx")


# result = pd.read_excel('/Users/menglu/Desktop/output.xlsx',engine = 'openpyxl')
# X = result[["final"]].values
# y = result["jkn"].values
#
# regr = LinearRegression()
#
# # create quadratic features
# quadratic = PolynomialFeatures(degree=2)
# cubic = PolynomialFeatures(degree=3)
# X_quad = quadratic.fit_transform(X)
# X_cubic = cubic.fit_transform(X)
#
# # fit features
# X_fit = np.arange(X.min(), X.max(), 1)[:, np.newaxis]
#
# regr = regr.fit(X, y)
# y_lin_fit = regr.predict(X_fit)
# linear_r2 = r2_score(y, regr.predict(X))
# print("linear_r2:", linear_r2)
#
# regr = regr.fit(X_quad, y)
# y_quad_fit = regr.predict(quadratic.fit_transform(X_fit))
# quadratic_r2 = r2_score(y, regr.predict(X_quad))
# print("quadratic_r2:", quadratic_r2)
#
# regr = regr.fit(X_cubic, y)
# y_cubic_fit = regr.predict(cubic.fit_transform(X_fit))
# cubic_r2 = r2_score(y, regr.predict(X_cubic))
# print("cubic_r2:", cubic_r2)
#
# # plot results
# plt.scatter(X, y, label='training points', color='lightgray')
#
# plt.plot(X_fit, y_lin_fit,
#          label='linear (d=1), $R^2=%.2f$' % linear_r2,
#          color='blue',
#          lw=2,
#          linestyle=':')
#
# plt.plot(X_fit, y_quad_fit,
#          label='quadratic (d=2), $R^2=%.2f$' % quadratic_r2,
#          color='red',
#          lw=2,
#          linestyle='-')
#
# plt.plot(X_fit, y_cubic_fit,
#          label='cubic (d=3), $R^2=%.2f$' % cubic_r2,
#          color='green',
#          lw=2,
#          linestyle='--')

#plt.savefig('images/10_11.png', dpi=300)
#plt.show()

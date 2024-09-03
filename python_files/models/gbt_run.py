from xgboost import XGBRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
import attributes as attrib
import pandas as pd
from sklearn.metrics import mean_squared_error
from math import sqrt
from sklearn.multioutput import MultiOutputRegressor
from sklearn.datasets import make_hastie_10_2
from statistics import mean
from get_train_test_val import build_test_train

df_data = pd.read_csv(attrib.data_file,sep=";")
df_results = pd.read_csv(attrib.results_file,sep=";")
df_data.drop(columns=["insee"],inplace=True)
df_results.drop(columns=["insee"],inplace=True)
#df_results = df_results["er_idf"]
X = df_data.values
y = df_results.values
rmse_list = []
X_train, X_test, y_train, y_test = build_test_train(normX = True)
clf = XGBRegressor().fit(X_train, y_train)
test_preds = clf.predict(X_test)
mse = mean_squared_error(y_test, test_preds)
rmse = sqrt(mse)
rmse_list.append(rmse)
print("XGB :",mean(rmse_list))
rmse_list = []
X_train, X_test, y_train, y_test = build_test_train(normX = True)
clf = MultiOutputRegressor(GradientBoostingRegressor()).fit(X_train, y_train)
test_preds = clf.predict(X_test)
mse = mean_squared_error(y_test, test_preds)
rmse = sqrt(mse)
rmse_list.append(rmse)
print("sklearn :",mean(rmse_list))
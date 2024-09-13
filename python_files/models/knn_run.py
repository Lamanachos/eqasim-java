from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import train_test_split
import attributes as attrib
import pandas as pd
from sklearn.metrics import mean_squared_error
from math import sqrt
from sklearn.multioutput import MultiOutputRegressor
from statistics import mean
from get_train_test_val import build_test_train,div_data_by_column

def run_random(test_size = 0.3):
    df_data = pd.read_csv(attrib.data_file,sep=";")
    df_results = pd.read_csv(attrib.results_file,sep=";")
    df_data.drop(columns=["insee"],inplace=True)
    df_results.drop(columns=["insee"],inplace=True)
    #df_results = df_results["er_idf"]
    X = df_data.values
    y = df_results.values
    rmse_list = []
    for i in range(100):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size)
        knn_model = KNeighborsRegressor(n_neighbors=7)
        knn_model.fit(X_train, y_train)
        test_preds = knn_model.predict(X_test)
        #print(test_preds)
        #print(y_test)
        mse = mean_squared_error(y_test, test_preds)
        rmse = sqrt(mse)
        rmse_list.append(rmse)
    rmse_list.append(rmse)
    print(mean(rmse_list))

def run_built():
    split_type = "dep"
    add_info = [["92","75","9293","9394"],["93","7594","94","7592"],[]]
    df_data = div_data_by_column(to_drop=["road","nb_pt","work_or_edu_fac","other_fac"])
    X_train, X_test, X_val, y_train, y_test, y_val, info = build_test_train(normX = True, normY= False, split_type=split_type, split_arg=add_info)
    knn_model = KNeighborsRegressor(n_neighbors=7)
    knn_model.fit(X_train, y_train)
    test_preds = knn_model.predict(X_test)
    mse = mean_squared_error(y_test, test_preds)
    rmse = sqrt(mse)
    print(rmse)
print("Moyenne sur 100 run avec des train/test random :")
run_random()
print("Résultats avec le train/test built")
run_built()

from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
import get_train_test_val as gt
from sklearn.metrics import mean_squared_error
from math import sqrt
import pandas as pd

split_type = "dep"
add_info = add_info = [["92","75","9293","9394"],["93","7594","94","7592"],[]]
liste_res = ["car_ms_res_nb","car_ms_inout_nb","car_ms_idf_nb","att_res","att_inout","att_idf","er_0","er_10","er_20","er_idf"]
liste_feats = ["nb_pt","er_bs","area","pop","road","big_road","work_or_edu_fac","other_fac"]
X_train, X_test, X_val, y_train, y_test, y_val, infos = gt.build_test_train(split_type = split_type, split_arg= add_info,normX = True, normY = False,liste_res=liste_res)

df_ytrain = pd.DataFrame(y_train)
df_ytrain.columns = liste_res
df_ytest = pd.DataFrame(y_test)
df_ytest.columns = liste_res

model_poly = SVR(kernel="poly")
model_rbf = SVR(kernel="rbf")
model_linear = SVR(kernel="linear")
model_sig = SVR(kernel="sigmoid")
models = {"poly":model_poly,"rbf":model_rbf,"linear":model_linear,"sigmoid":model_sig}
dict_means = gt.get_means(gt.get_results())
dict_rmse = {}
for res in liste_res:
    print(res,":")
    for model in models.keys():
        temp = models[model]
        temp.fit(X_train, df_ytrain[res])
        test_preds = temp.predict(X_test)
        mean = dict_means[res]
        mse = mean_squared_error(df_ytest[res], test_preds)
        rmse = sqrt(mse)
        if res not in dict_rmse.keys():
            dict_rmse[res] = {}
        dict_rmse[res][model] = rmse
        print(model,":",abs(rmse))

for model in models.keys():
    tot = 0
    for res in dict_rmse.keys():
        tot += dict_rmse[res][model]
    print(f"{model}:",tot/len(dict_rmse.keys()))


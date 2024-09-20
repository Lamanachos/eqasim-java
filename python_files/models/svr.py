from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
import get_train_test_val as gt
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from math import sqrt
import pandas as pd

#choix du mode de découpage
split_type = "dep"
add_info = add_info = [["92","75","9293","9394"],["93","7594","94","7592"],[]]

#Choix des résultats à garder
#liste_res = ["car_ms_idf_nb","att_idf","er_idf"]
liste_res = ["car_ms_res_nb","car_ms_inout_nb","car_ms_idf_nb","att_res","att_inout","att_idf","er_0","er_10","er_20","er_idf"]

#Choix des features à garder
#liste_feats = ["nb_pt","er_bs","area","pop","road","big_road","work_or_edu_fac","other_fac"]
liste_feats = ["area","pop","density","road","nb_pt","work_or_edu_fac","other_fac","cars_per_persons","big_road","er_bs","ms_walk_bs","coeff_join"]

X_train, X_test, X_val, y_train, y_test, y_val, infos = gt.build_test_train(split_type = split_type, split_arg= add_info,normX = True, normY = True,liste_res=liste_res,liste_feats=liste_feats)

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
dict_mae = {}
dict_r2 = {}
for res in liste_res:
    print(res,":")
    for model in models.keys():
        temp = models[model]
        temp.fit(X_train, df_ytrain[res])
        test_preds = temp.predict(X_test)
        mean = dict_means[res]
        mse = mean_squared_error(df_ytest[res], test_preds)
        rmse = sqrt(mse)
        mae = mean_absolute_error(df_ytest[res], test_preds)
        r2 = r2_score(df_ytest[res], test_preds)
        if res not in dict_rmse.keys():
            dict_rmse[res] = {}
            dict_mae[res] = {}
            dict_r2[res] = {}
        dict_rmse[res][model] = rmse
        dict_mae[res][model] = mae
        dict_r2[res][model] = r2
        print(model,":",abs(rmse))

print("Mean RMSE :")
for model in models.keys():
    tot = 0
    for res in dict_rmse.keys():
        tot += dict_rmse[res][model]
    print(f"{model}:",tot/len(dict_rmse.keys()))

print("Mean MAE :")
for model in models.keys():
    tot = 0
    for res in dict_mae.keys():
        tot += dict_mae[res][model]
    print(f"{model}:",tot/len(dict_mae.keys()))

print("Mean r2 :")
for model in models.keys():
    tot = 0
    for res in dict_r2.keys():
        tot += dict_r2[res][model]
    print(f"{model}:",tot/len(dict_r2.keys()))


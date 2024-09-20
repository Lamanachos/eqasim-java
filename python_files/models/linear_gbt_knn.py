from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
import get_train_test_val as gt
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.multioutput import MultiOutputRegressor
from sklearn.ensemble import GradientBoostingRegressor
from math import sqrt
import pandas as pd

#Choix du mode de découpage
split_type = "dep"
add_info = add_info = [["92","75","9293","9394"],["93","7594","94","7592"],[]]

#Choix des résultats à garder
#liste_res = ["car_ms_idf_nb","att_idf","er_idf"]
liste_res = ["car_ms_res_nb","car_ms_inout_nb","car_ms_idf_nb","att_res","att_inout","att_idf","er_0","er_10","er_20","er_idf"]

#Choix des features à garder
#liste_feats = ["area","pop","density","road","nb_pt","work_or_edu_fac","other_fac","cars_per_persons","big_road","er_bs","ms_walk_bs","coeff_join"]
liste_feats = ["area","pop","density","road","nb_pt","work_or_edu_fac","other_fac","cars_per_persons","big_road","er_bs","ms_walk_bs","coeff_join"]

X_train, X_test, X_val, y_train, y_test, y_val, infos = gt.build_test_train(df_data=gt.get_data(),split_type = split_type, split_arg= add_info,normX = True, normY = True,liste_res=liste_res,liste_feats=liste_feats)

#Choix du modèle
model = KNeighborsRegressor(n_neighbors=7) #Knns
#model = MultiOutputRegressor(GradientBoostingRegressor()) #Gbts
#model = LinearRegression() #Régression linéaire

model.fit(X_train, y_train)
test_preds = model.predict(X_test)
df_preds = pd.DataFrame(test_preds)
df_preds.columns = liste_res
df_test = pd.DataFrame(y_test)
df_test.columns = liste_res
dict_means = gt.get_means(gt.get_results())
tot = 0
tot_mean = 0
for i in liste_res:
    mean = dict_means[i]
    mse = mean_squared_error(df_test[i], df_preds[i])
    tot_mean += mean
    rmse = sqrt(mse)
    print(i,":",abs(rmse))
    rmse = rmse
    tot += abs(rmse)
    print("mean",i,":",abs(rmse))
mean_mean = tot_mean/len(liste_res)
print("Mean RMSE :", tot/len(liste_res))
mse = mean_squared_error(y_test, test_preds)
rmse = sqrt(mse)
print("Normal RMSE :",rmse)
mae = mean_absolute_error(y_test, test_preds)
print("Normal MAE :",mae)
r2 = r2_score(y_test, test_preds)
print("Normal r2 :",r2)
print("Mean_mean RMSE :",abs(rmse/mean_mean))

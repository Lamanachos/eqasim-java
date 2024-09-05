from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
import get_train_test_val as gt
from sklearn.metrics import mean_squared_error
from math import sqrt
import pandas as pd

split_type = "dep"
add_info = add_info = [["92","75","9293","9394"],["93","7594","94","7592"],[]]
#liste_res = ["er_idf"]
liste_res = ["car_ms_res_nb","car_ms_inout_nb","car_ms_idf_nb","att_res","att_inout","att_idf","er_0","er_10","er_20","er_idf"]
liste_feats = ["nb_pt","er_bs","area","pop","road","big_road","work_or_edu_fac","other_fac"]
X_train, X_test, X_val, y_train, y_test, y_val, infos = gt.build_test_train(split_type = split_type, split_arg= add_info,normX = True, normY = False,liste_res=liste_res)

model = LinearRegression()
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
    rmse = sqrt(mse)/mean
    tot += abs(rmse)
    print(i,":",abs(rmse))
mean_mean = tot_mean/len(liste_res)
print("Mean RMSE :", tot/len(liste_res))
mse = mean_squared_error(y_test, df_preds)
rmse = sqrt(mse)
print("Mean_mean RMSE :",abs(rmse/mean_mean))

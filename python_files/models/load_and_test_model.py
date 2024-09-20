import numpy as np
import sys

import tensorflow as tf
from sklearn.metrics import mean_absolute_error,r2_score,mean_squared_error
import attributes as attrib
import pandas as pd
from get_train_test_val import build_test_train,get_data

#model_path = "outputs\\cool\\3outputs2\\models.keras"
model_path = "outputs\\cool\\all_mae_1\\models.keras"
model = tf.keras.models.load_model(model_path)

split_type = "dep"
add_info = [["92","75","9293","9394"],["93","7594"],["94","7592"]]

#liste_feats = ["area","pop","road","nb_pt","work_or_edu_fac","other_fac","cars_per_persons","big_road","er_bs","ms_walk_bs","coeff_join"]
liste_feats = ["area","pop","density","road","nb_pt","work_or_edu_fac","other_fac","cars_per_persons","big_road","er_bs","ms_walk_bs","coeff_join"]
nb_feats = len(liste_feats)

#liste_res = ["car_ms_idf_nb","att_idf","er_idf"]
liste_res = ["car_ms_res_nb","car_ms_inout_nb","car_ms_idf_nb","att_res","att_inout","att_idf","er_0","er_10","er_20","er_idf"]
nb_output = len(liste_res)

df_data = get_data()
X_train, X_test, X_val, y_train, y_test, y_val, infos = build_test_train(df_data=df_data, split_type = split_type, split_arg= add_info,normX = True, normY = True, liste_res=liste_res)

train_size = len(X_train)
test_size = len(X_test)
val_size = len(X_val)

X_train = pd.DataFrame(X_train)
X_test = pd.DataFrame(X_test)
X_val = pd.DataFrame(X_val)

def output_form(arr):
    lists = []
    for a in arr :
        for i in range(len(a)):
            if len(lists)<i+1:
                lists.append([])
            lists[i].append(a[i])
    np_lists = []
    for i in lists :
        np_lists.append(np.array(i))
    return(np_lists)

y_train = output_form(y_train)
y_test = output_form(y_test)
y_val = output_form(y_val)

y_pred = model.predict(X_test)
temp = []
for ar in y_pred :
    new_ar = []
    for i in ar :
        new_ar.append(i[0])
    new_ar = np.array(new_ar)
    temp.append(new_ar)
y_pred = temp

temp1 = []
temp2 = []
for i in range(len(y_test[0])):
    new_ar1 = []
    new_ar2 = []
    for j in range(len(y_test)):
        new_ar1.append(y_test[j][i])
        new_ar2.append(y_pred[j][i])
    temp1.append(np.array(new_ar1))
    temp2.append(np.array(new_ar2))
y_test = temp1
y_pred = temp2

mae = mean_absolute_error(y_test,y_pred)
r2 = r2_score(y_test,y_pred)
print(mae)
print(r2)
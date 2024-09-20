import argparse
import matplotlib.pyplot as plt
import numpy as np
import os
import seaborn as sns
import sys
import tensorflow as tf
import time
from datetime import datetime
from sklearn import preprocessing


from tensorflow import keras
from keras.src.models import Model
from keras.src.layers import Dense, Input
import keras.src.losses
from sklearn.metrics import mean_absolute_error, r2_score
import attributes as attrib
import pandas as pd
from get_train_test_val import build_test_train,get_data
STDOUT = sys.stdout

#paramètres
batch_size = 1000
epochs = 75
validation_split = 0.2

split_type = "dep"
add_info = [["92","75","9293","9394"],["93","7594"],["94","7592"]]

#liste_feats = ["area","pop","road","nb_pt","work_or_edu_fac","other_fac","cars_per_persons","big_road","er_bs","ms_walk_bs","coeff_join"]
liste_feats = ["area","pop","density","road","nb_pt","work_or_edu_fac","other_fac","cars_per_persons","big_road","er_bs","ms_walk_bs","coeff_join"]
nb_feats = len(liste_feats)

liste_res = ["car_ms_idf_nb","att_idf","er_idf"]
#liste_res = ["car_ms_res_nb","car_ms_inout_nb","car_ms_idf_nb","att_res","att_inout","att_idf","er_0","er_10","er_20","er_idf"]
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

beginning = time.time()

#Setup
if not os.path.exists(f"outputs/anns"):
    os.makedirs(f"outputs/anns")

def ask_for_model_name():

    already_chosen_reports_names = os.listdir("outputs/anns/")
    already_chosen_reports_names = [name for name in already_chosen_reports_names if name not in [".", ".."]]
    already_chosen_reports_names.sort()
    print("Already chosen names :\n")
    for name in already_chosen_reports_names:
        print(name)

    print()
    report_name = input("Choose a report name :\n")
    while ((report_name in already_chosen_reports_names)):
        report_name = input("Choose a report name :\n")
    if report_name == "":
        debut = datetime.now()
        report_name =str(debut)[:-7]
        report_name = report_name.replace("-",":")
        report_name = report_name.replace(" ",":")
    return report_name

# Modèles

def mo_ASY_model() :
    input_layer = Input(shape=(nb_feats,))
    outputs = []
    x = Dense(512, activation="tanh")(input_layer)
    x = Dense(256, activation="tanh")(x)
    for i in range(int(nb_output)):
        outputs.append(Dense(1, name=liste_res[i])(Dense(128)(x)))
    model = Model(inputs=input_layer, outputs=outputs)
    return model

def mo_ASY_model_alone() :
    input_layer = Input(shape=(nb_feats,))
    outputs = []
    for i in range(int(nb_output)):
        outputs.append(Dense(1, name=liste_res[i])(Dense(128)(Dense(256, activation="tanh")(Dense(512, activation="tanh")(input_layer)))))
    model = Model(inputs=input_layer, outputs=outputs)
    return model

def do_multiple_simulations(nb_simulations, type_model):
    liste = []
    for i in range(nb_simulations):
        debut = datetime.now()
        file_name =str(debut)[:-7]
        file_name = file_name.replace(":",".")
        file_name = file_name.replace("-",".")
        file_name = file_name.replace(" ",".")
        liste.append(main(type_model,file_name))
    print(liste)

def main(type_model,report_name = None):

    print(f"Type model : {type_model}")
    
    if type_model == "dense_alone":
        model = mo_ASY_model_alone()
    elif type_model == "dense_mix":
        model = mo_ASY_model()
    else:
        print("Wrong argument :\n'p' for perceptron\n'c' for convolutional (CNN)\n'd' for dummy (tests)\n'o' for ordonez-roggen\n'mo' for modified ordonez-roggen\n'do' for modified ordonez roggen with dropout")
        return
    
    if report_name == None :
        report_name = ask_for_model_name()
    
    model.summary()
    loss = {}
    metrics = {}
    for i in range(nb_output):
        loss[liste_res[i]] = "mean_absolute_error"
        metrics[liste_res[i]] = keras.metrics.RootMeanSquaredError()
    model.compile(
        optimizer="adam",
        loss = loss,
        metrics = metrics
    )

    val_data = (X_val,y_val)
    history = model.fit(
        X_train,
        y_train,
        batch_size=batch_size,
        epochs=epochs,
        validation_split=validation_split,
        validation_data=val_data
    )

    #str_metric = 'custom_f1'
    str_metric = 'root_mean_squared_error'
    #print(history.history.keys())
    acc = []
    val_acc = []
    if nb_output > 1 :
        for i in range(epochs):
            tot = 0
            for j in range(nb_output) :
                tot += history.history[liste_res[j]+"_"+str_metric][i]
            acc.append(tot/nb_output)
        for i in range(epochs):
            tot = 0
            for j in range(nb_output) :
                tot += history.history["val_"+liste_res[j]+"_"+str_metric][i]
            val_acc.append(tot/nb_output)
    else :
        for i in range(epochs):
            acc.append(history.history[str_metric][i])
            val_acc.append(history.history["val_"+str_metric][i])
    
    loss = history.history['loss']
    val_loss = history.history['val_loss']

    list_all = model.evaluate(X_test,  y_test, verbose=2)
    dict_all = model.evaluate(X_test,  y_test, verbose=2, return_dict=True)
    y_pred = model.predict(X_test)
    temp = []
    for ar in y_pred :
        new_ar = []
        for i in ar :
            new_ar.append(i[0])
        new_ar = np.array(new_ar)
        temp.append(new_ar)
    y_pred = temp
    mae = mean_absolute_error(y_test,y_pred)
    r2 = r2_score(y_test,y_pred)
    test_loss = list_all[0]
    print(list_all)
    print(nb_output +1)
    if nb_output > 1 :
        test_acc = np.mean(list_all[nb_output+1:])
    else :
        test_acc = list_all[1]
    print(f"Test loss : {test_loss}\nTest {str_metric} : {test_acc}")
    print(f"Test MAE : {mae}")
    print(f"Test R2 : {r2}")
    if nb_output == 1 :
        df_results = pd.read_csv(attrib.results_file,sep=";")
        print(f"Test {str_metric} normalized : {test_acc/np.mean(df_results[liste_res[0]])}\n")
    print(f"Time : {time.time() - beginning}")
    model.save(f"outputs/anns/{report_name}/models.h5")
    model.save(f"outputs/anns/{report_name}/models.keras")

    # Rapport

    with open(f"outputs/anns/{report_name}/report.txt", "w") as file:
        file.write(f"Name : {report_name}\n")
        file.write(f"Type : {type_model}\n\n")
        file.write(f"Batch size : {batch_size}\n")
        file.write(f"Epochs : {epochs}\n")
        file.write(f"Validation split : {validation_split}\n")
        file.write(f"Feats : {nb_feats}\n")
        file.write(f"Res list : {str(liste_res)}\n")
        file.write(f"Train size : {train_size}\n")
        file.write(f"Val size : {val_size}\n")
        file.write(f"Test size : {test_size}\n")
        file.write(f"Split type : {split_type}\n")
        file.write(f"Additional info : {add_info}\n")
        """ file.write(f"Train : {chemin_train}\n")
        file.write(f"Chemin val : {chemin_val}\n")
        file.write(f"Chemin test : {chemin_test}\n") """
        file.write("\n")

        file.write(f"Test {str_metric} : {test_acc}\n")
        file.write(f"Test loss : {test_loss}\n\n")
        file.write(f"Test MAE : {mae}\n")
        file.write(f"Test R2 : {r2}\n\n")
        if nb_output == 1 :
            file.write(f"Test {str_metric} normalized : {test_acc/np.mean(df_results[liste_res[0]])}\n")
        temp_dict = {}
        for i in liste_res:
            temp_dict[i] = dict_all[i+"_root_mean_squared_error"]
        file.write(f"All outputs : {temp_dict}\n")
        file.write(f"Summary :\n\n")
        sys.stdout = file
        model.summary()
        sys.stdout = STDOUT

        file.write(f"\n{str_metric} : {acc}\n\n")
        file.write(f"Loss : {loss}\n\n")
        file.write(f"Validation {str_metric} : {val_acc}\n\n")
        file.write(f"Validation loss : {val_loss}\n\n")

        file.write(f"Train : {str(infos[0])}\n\n")
        file.write(f"Test  : {str(infos[1])}\n\n")
        file.write(f"Val  : {str(infos[2])}\n\n")

    # Graphiques

    epochs_range = range(epochs)

    plt.figure(figsize=(8, 8))
    plt.suptitle(f"Name = {report_name}, type = {type_model}, batch_size = {batch_size}, epochs = {epochs}, val_split = {validation_split}")

    plt.subplot(1, 2, 1)
    plt.plot(epochs_range, acc, label='Training RMSE')
    plt.plot(epochs_range, val_acc, label='Validation RMSE')
    plt.legend(loc='lower right')
    plt.title('Training and Validation RMSE')
    plt.grid(True)

    plt.subplot(1, 2, 2)
    plt.plot(epochs_range, loss, label='Training Loss')
    plt.plot(epochs_range, val_loss, label='Validation Loss')
    plt.legend(loc='upper right')
    plt.title('Training and Validation Loss')
    plt.grid(True)

    plt.savefig(f"outputs/anns/{report_name}/results.png")

    epochs_range = range(epochs)

    plt.figure(figsize=(8, 8))
    plt.suptitle(f"Name = {report_name}, type = {type_model}, batch_size = {batch_size}, epochs = {epochs}, val_split = {validation_split}")

    plt.subplot(1, 2, 1)
    plt.plot(epochs_range[100:], acc[100:], label='Training RMSE')
    plt.plot(epochs_range[100:], val_acc[100:], label='Validation RMSE')
    plt.legend(loc='lower right')
    plt.title('Training and Validation RMSE')
    plt.grid(True)

    plt.subplot(1, 2, 2)
    plt.plot(epochs_range[100:], loss[100:], label='Training Loss')
    plt.plot(epochs_range[100:], val_loss[100:], label='Validation Loss')
    plt.legend(loc='upper right')
    plt.title('Training and Validation Loss')
    plt.grid(True)

    plt.savefig(f"outputs/anns/{report_name}/results_after_100.png")
    #plt.show()
    return(test_acc)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--type", type=str, default="dense_mix", help="Model type")
    parser.add_argument("-m", "--multiple", type=int, default=None, help="Multiple simulations")
    parser.add_argument("-n", "--naming", type=str, default="n", help="y if you want to name")
    args = parser.parse_args()

    if args.multiple != None and args.type in ["dense_mix", "dense_alone"]:
        print("Multiple simulations")
        do_multiple_simulations(args.multiple, args.type)
    elif args.type in ["dense_mix", "dense_alone"]:
        print("One simualtion, with graph / report / conf. matrix")
        if args.naming == "n" :
            debut = datetime.now()
            file_name =str(debut)[:-7]
            file_name = file_name.replace(":",".")
            file_name = file_name.replace("-",".")
            file_name = file_name.replace(" ",".")
            main(args.type,file_name)
        else :
            main(args.type)
    else:
        print("Wrong input.")
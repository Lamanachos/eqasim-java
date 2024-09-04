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
from keras.src.layers import Conv2D, Dense, Dropout, Flatten, LSTM, Reshape, Permute, BatchNormalization, Activation,Input
import keras.src.losses
from keras.src.models import Sequential
from sklearn.metrics import confusion_matrix, f1_score
import attributes as attrib
import pandas as pd
from sklearn.model_selection import train_test_split
from get_train_test_val import build_test_train,df_to_array,div_data_by_column,get_data
STDOUT = sys.stdout

#paramètres
batch_size = 990
epochs = 300
validation_split = 0.2

split_type = "dep"
add_info = [["92","75","9293","9394"],["93","7594"],["94","7592"]]

#liste_feats = ["area","pop","road","nb_pt","work_or_edu_fac","other_fac","cars_per_persons","big_road","er_bs","ms_walk_bs","coeff_join"]
liste_feats = ["area","pop","density","road","nb_pt","work_or_edu_fac","other_fac","cars_per_persons","big_road","er_bs","ms_walk_bs","coeff_join"]
nb_feats = len(liste_feats)

liste_res = ["er_idf"]
#liste_res = ["car_ms_res_nb","car_ms_inout_nb","car_ms_idf_nb","att_res","att_inout","att_idf","er_0","er_10","er_20","er_idf"]
nb_output = len(liste_res)

#df_data = div_data_by_column()
df_data = get_data()
X_train, X_test, X_val, y_train, y_test, y_val, infos = build_test_train(df_data=df_data, split_type = split_type, split_arg= add_info,normX = True, normY = False, liste_res=liste_res)
#X_train, X_temp, y_train, y_temp = build_test_train(normX = True, normY = False)
#X_test, X_val, y_test, y_val = train_test_split(X_temp, y_temp, test_size=0.5,random_state=1)

""" df_results = pd.read_csv(attrib.results_file,sep=";")
df_data = pd.read_csv(attrib.data_file,sep=";")
df_data.drop(columns=["insee"],inplace=True)
df_results.drop(columns=["insee"],inplace=True)
X = df_to_array(df_data, norm=True)
Y = df_to_array(df_results) 

X_train, X_temp, y_train, y_temp = train_test_split(X, Y, test_size=0.66666,random_state=1)
X_test, X_val, y_test, y_val = train_test_split(X_temp, y_temp, test_size=0.5,random_state=2) """

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

def dummy_model(): # Modèle très simple pour tester le code

    model = Sequential(name="dummy")
    
    model.add(Dense(11,input_shape=[nb_feats]))

    model.build()

    return model

def perceptron_model():

    model = Sequential(name="perceptron")

    model.add(Dense(512, activation="relu",input_shape=[nb_feats]))
    model.add(Dense(256, activation="relu"))
    model.add(Dense(128, activation="relu"))
    model.add(Dense(64, activation="relu"))
    model.add(Dense(4, activation="softmax"))

    model.build()

    return model

def mo_ASY_model_() :
    input_layer = Input(shape=(nb_feats,))
    d1 = Dense(50)(input_layer)
    bn1 = BatchNormalization()(d1)
    a1 = Activation("tanh")(bn1)
    d2 = Dense(10)(a1)
    """ d3 = Dense(50)(d2)
    d4 = Dense(50)(d3)
    d5 = Dense(50)(d4)
    d6 = Dense(50)(d5)
    d7 = Dense(50)(d6) """
    bn2 = BatchNormalization()(a1)
    a2 = Activation("tanh")(bn2)
    outputs = []
    for i in range(nb_output):
        outputs.append(Dense(1, name=liste_res[i])(Dense(50)(a2)))
    model = Model(inputs=input_layer, outputs=outputs)
    return model

def mo_ASY_model() :
    input_layer = Input(shape=(nb_feats,))
    #x = Dense(512, activation="tanh")(input_layer)
    #x = BatchNormalization()(input_layer)
    x = Dense(512, activation="tanh")(input_layer)
    x = Dense(256, activation="tanh")(x)
    outputs = []
    for i in range(nb_output):
        outputs.append(Dense(1, name=liste_res[i])(Dense(128)(x)))
    model = Model(inputs=input_layer, outputs=outputs)
    return model

def do_multiple_simulations(nb_simulations, type_model):
    for i in range(nb_simulations):
        debut = datetime.now()
        file_name =str(debut)[:-7]
        file_name = file_name.replace(":",".")
        file_name = file_name.replace("-",".")
        file_name = file_name.replace(" ",".")
        main(type_model,file_name)

def mean_cat_ac(y_true,y_pred):
    temp = tf.keras.metrics.CategoricalAccuracy()
    temp = temp(y_true,y_pred)
    return tf.math.reduce_mean(temp)

def main(type_model,report_name = None):

    print(f"Type model : {type_model}")
    
    if type_model == "p":
        model = perceptron_model()
    elif type_model == "d":
        model = dummy_model()
    elif type_model == "mo_asy":
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
    test_loss = list_all[0]
    print(list_all)
    print(nb_output +1)
    if nb_output > 1 :
        test_acc = np.mean(list_all[nb_output+1:])
    else :
        test_acc = list_all[1]
    print(f"Test loss : {test_loss}\nTest {str_metric} : {test_acc}")
    if nb_output == 1 :
        df_results = pd.read_csv(attrib.results_file,sep=";")
        print(f"Test {str_metric} normalized : {test_acc/np.mean(df_results[liste_res[0]])}")
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
        if nb_output == 1 :
            file.write(f"Test {str_metric} normalized : {test_acc/np.mean(df_results[liste_res[0]])}")
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--type", type=str, default="p", help="Model type")
    parser.add_argument("-m", "--multiple", type=int, default=None, help="Multiple simulations")
    parser.add_argument("-n", "--naming", type=str, default="n", help="y if you want to name")
    args = parser.parse_args()

    if args.multiple != None and args.type in ["p", "c", "mo_asy"]:
        print("Multiple simulations")
        do_multiple_simulations(args.multiple, args.type)
    elif args.type in ["p", "c", "mo_asy"]:
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
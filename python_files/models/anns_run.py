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
from get_train_test_val import build_test_train
STDOUT = sys.stdout
#paramètres
nb_feats = 11
batch_size = 10
epochs = 1000
validation_split = 0.2
nb_output = 10

X_train, X_temp, y_train, y_temp = build_test_train(normX= True, normY = False)
X_test, X_val, y_test, y_val = train_test_split(X_temp, y_temp, test_size=0.5,random_state=1)

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

def ASY_model() :

    input_layer = Input(shape=(nb_feats,))
    d1 = Dense(50)(input_layer)
    bn1 = BatchNormalization()(d1)
    a1 = Activation("tanh")(bn1)
    d2 = Dense(10)(a1)
    d3 = Dense(50)(d2)
    d4 = Dense(50)(d3)
    d5 = Dense(50)(d4)
    d6 = Dense(50)(d5)
    d7 = Dense(50)(d6)
    bn2 = BatchNormalization()(d7)
    a2 = Activation("tanh")(bn2)
    d71 = Dense(50)(a2)
    d72 = Dense(50)(a2)
    d73 = Dense(50)(a2)
    d74 = Dense(50)(a2)
    d75 = Dense(50)(a2)
    d76 = Dense(50)(a2)
    d77 = Dense(50)(a2)
    d78 = Dense(50)(a2)
    d79 = Dense(50)(a2)
    d70 = Dense(50)(a2)
    y1 = Dense(1, name='y1')(d71)
    y2 = Dense(1, name='y2')(d72)
    y3 = Dense(1, name='y3')(d73)
    y4 = Dense(1, name='y4')(d74)
    y5 = Dense(1, name='y5')(d75)
    y6 = Dense(1, name='y6')(d76)
    y7 = Dense(1, name='y7')(d77)
    y8 = Dense(1, name='y8')(d78)
    y9 = Dense(1, name='y9')(d79)
    y10 = Dense(1, name='y10')(d70)

    model = Model(inputs=input_layer, outputs=[y1, y2, y3, y4, y5, y6, y7, y8, y9, y10])
    return model

def base_model(inputs):
    d1 = Dense(50)(inputs)
    bn1 = BatchNormalization()(d1)
    a1 = Activation("tanh")(bn1)
    d2 = Dense(10)(a1)
    d3 = Dense(50)(d2)
    d4 = Dense(50)(d3)
    d5 = Dense(50)(d4)
    d6 = Dense(50)(d5)
    d7 = Dense(50)(d6)
    bn2 = BatchNormalization()(d7)
    a2 = Activation("tanh")(bn2)
    return a2

def inter_model(inputs):
    x = base_model(inputs)
    y1 = Dense(1, name='y1')(x)
    y2 = Dense(1, name='y2')(x)
    y3 = Dense(1, name='y3')(x)
    y4 = Dense(1, name='y4')(x)
    y5 = Dense(1, name='y5')(x)
    y6 = Dense(1, name='y6')(x)
    y7 = Dense(1, name='y7')(x)
    y8 = Dense(1, name='y8')(x)
    y9 = Dense(1, name='y9')(x)
    y10 = Dense(1, name='y10')(x)
    model = Model(inputs=inputs, outputs = [y1, y2, y3, y4, y5, y6, y7, y8, y9, y10])
    return model

def ASY_model_():
    inputs = Input(shape=(11,))
    model = inter_model(inputs)
    return model

def do_multiple_simulations(nb_simulations, type_model):
    for i in range(nb_simulations):
        debut = datetime.now()
        file_name =str(debut)[:-7]
        file_name = file_name.replace("-",":")
        file_name = file_name.replace(" ",":")
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
    elif type_model == "asy":
        model = ASY_model()
    else:
        print("Wrong argument :\n'p' for perceptron\n'c' for convolutional (CNN)\n'd' for dummy (tests)\n'o' for ordonez-roggen\n'mo' for modified ordonez-roggen\n'do' for modified ordonez roggen with dropout")
        return
    
    if report_name == None :
        report_name = ask_for_model_name()
    
    model.summary()

    model.compile(
        optimizer="adam",
        loss = {'y1': 'binary_crossentropy', 'y2': 'binary_crossentropy', 'y3': 'binary_crossentropy', 'y4': 'binary_crossentropy', 'y5': 'binary_crossentropy', 'y6': 'binary_crossentropy', 'y7': 'binary_crossentropy', 'y8': 'binary_crossentropy','y9': 'binary_crossentropy','y10': 'binary_crossentropy'},
        metrics = {'y1': keras.metrics.RootMeanSquaredError(),
                'y2': keras.metrics.RootMeanSquaredError(),
                'y3': keras.metrics.RootMeanSquaredError(),
                'y4': keras.metrics.RootMeanSquaredError(),
                'y5': keras.metrics.RootMeanSquaredError(),
                'y6': keras.metrics.RootMeanSquaredError(),
                'y7': keras.metrics.RootMeanSquaredError(),
                'y8': keras.metrics.RootMeanSquaredError(),
                'y9': keras.metrics.RootMeanSquaredError(),
                'y10': keras.metrics.RootMeanSquaredError()}
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
    str_metric = '_root_mean_squared_error'
    #print(history.history.keys())
    acc = []
    for i in range(epochs):
        tot = 0
        for j in range(nb_output) :
            tot += history.history["y"+str(j+1)+str_metric][i]
        acc.append(tot/nb_output)
    val_acc = []
    for i in range(epochs):
        tot = 0
        for j in range(nb_output) :
            tot += history.history["val_y"+str(j+1)+str_metric][i]
        val_acc.append(tot/nb_output)
    loss = history.history['loss']
    val_loss = history.history['val_loss']

    list_all = model.evaluate(X_test,  y_test, batch_size=batch_size, verbose=2)
    test_loss = list_all[0]
    test_acc = np.mean(list_all[11:])
    print(f"Test loss : {test_loss}\nTest {str_metric} : {test_acc}")
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

        """ file.write(f"Train : {chemin_train}\n")
        file.write(f"Chemin val : {chemin_val}\n")
        file.write(f"Chemin test : {chemin_test}\n") """
        file.write("\n")

        file.write(f"Test {str_metric} : {test_acc}\n")
        file.write(f"Test loss : {test_loss}\n\n")
        file.write(f"Summary :\n\n")
        sys.stdout = file
        model.summary()
        sys.stdout = STDOUT

        file.write(f"\n{str_metric} : {acc}\n\n")
        file.write(f"Loss : {loss}\n\n")
        file.write(f"Validation {str_metric} : {val_acc}\n\n")
        file.write(f"Validation loss : {val_loss}\n\n")

    # Graphiques

    epochs_range = range(epochs)

    plt.figure(figsize=(8, 8))
    plt.suptitle(f"Name = {report_name}, type = {type_model}, batch_size = {batch_size}, epochs = {epochs}, val_split = {validation_split}")

    plt.subplot(1, 2, 1)
    plt.plot(epochs_range, acc, label='Training Accuracy')
    plt.plot(epochs_range, val_acc, label='Validation Accuracy')
    plt.legend(loc='lower right')
    plt.title('Training and Validation Accuracy')
    plt.grid(True)

    plt.subplot(1, 2, 2)
    plt.plot(epochs_range, loss, label='Training Loss')
    plt.plot(epochs_range, val_loss, label='Validation Loss')
    plt.legend(loc='upper right')
    plt.title('Training and Validation Loss')
    plt.grid(True)

    plt.savefig(f"outputs/anns/{report_name}/results.png")
    #plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--type", type=str, default="p", help="Model type")
    parser.add_argument("-m", "--multiple", type=int, default=None, help="Multiple simulations")
    args = parser.parse_args()

    if args.multiple != None and args.type in ["p", "c", "asy"]:
        print("Multiple simulations")
        do_multiple_simulations(args.multiple, args.type)
    elif args.type in ["p", "c", "asy"]:
        print("One simualtion, with graph / report / conf. matrix")
        main(args.type)
    else:
        print("Wrong input.")
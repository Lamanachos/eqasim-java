import argparse
import matplotlib.pyplot as plt
import numpy as np
import os
import seaborn as sns
import sys
import tensorflow as tf
import time
from modules import corpus as co
from modules import modeles as mod
from datetime import datetime

from tensorflow import keras
from keras.src.layers import Conv2D, Dense, Dropout, Flatten, LSTM, Reshape, Permute
import keras.src.losses
from keras.src.models import Sequential
from modules import load_data
from sklearn.metrics import confusion_matrix, f1_score

"""
Le modèle ordonez-roggen et ses dérivées sont inspirés de l'article "Deep Convolutional and LSTM Recurrent Neural Networks for Multimodal Wearable Activity Recognition"
de Francisco Javier Ordóñez et Daniel Roggen
Le dépôt git associé se trouve à l'adresse https://github.com/STRCWearlab/DeepConvLSTM
L'article lui même est à la racine de ce projet sous le nom article_ordonez_roggen.pdf
"""

STDOUT = sys.stdout
CLASS_NAMES = [0,1,2,3]

# Hyperparamètres (et paramètres)

batch_size = 64
epochs = 20
validation_split = 0.2 #si il n'y a pas de de chemin_val renseigné la validation se fera sur cette fraction du corpus d'entraînement
num_unit_lstm = 128 #un paramètre lié aux architectures de corpus (ne pas toucher)
nb_obs_per_window = 20
nb_feats = 4 #4 si on utilise pas la vitesse, 5 sinon
drop_speed = True #si True on utilise pas la vitesse
size_after_conv = 8 #un paramètre lié à la taille des fenêtres, pour l'utilisation de mo c'est nb_obs_per_windows - 12 
#(c'est la taille de la sortie des couches de convolution)

chemin_train = "data/ml_data_again_FDBA_states_normalized_fenetres_train"
chemin_test = "data/ml_data_again_FDBA_states_normalized_fenetres_test" 
chemin_val = None

corpus_train = co.Corpus(chemin_train)
corpus_test = co.Corpus(chemin_test)
if chemin_val != None :
    corpus_val = co.Corpus(chemin_val)
else :
    corpus_val = None

X_train, y_train, X_test, y_test, X_val, Y_val = load_data(corpus_train,corpus_test,corpus_val,drop_speed = drop_speed)

beginning = time.time()

#Setup
if not os.path.exists(f"outputs/anns"):
    os.makedirs(f"outputs/anns")

#Custom Layers + Functions
class SliceLayer(tf.keras.layers.Layer):
  def __init__(self):
    super(SliceLayer, self).__init__()

  def build(self,input_shapes):
    self.input_shapes = input_shapes

  def call(self, inputs):
    #tf.print(inputs)
    k=0
    for i in inputs :
        k+=1 
    output = tf.TensorArray(tf.float32, size = k)
    for i in tf.range(k):
        output = output.write(i,inputs[i][-1])
    output = output.stack()
    return output
  
class PrintShape(tf.keras.layers.Layer):
  def __init__(self):
    super(PrintShape, self).__init__()

  def build(self,input_shapes):
    self.input_shapes = input_shapes
    print(input_shapes)
  def call(self, inputs):
    print(tf.shape(inputs))
    return inputs

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
    
    model.add(Flatten(input_shape=(nb_obs_per_window, 1, nb_feats)))
    model.add(Dense(4, activation="softmax"))

    model.build()

    return model

def perceptron_model():

    model = Sequential(name="perceptron")

    model.add(Flatten(input_shape=(nb_obs_per_window, 1, nb_feats)))
    model.add(Dense(512, activation="relu"))
    model.add(Dense(256, activation="relu"))
    model.add(Dense(128, activation="relu"))
    model.add(Dense(64, activation="relu"))
    model.add(Dense(4, activation="softmax"))

    model.build()

    return model
    
def conv_model():

    model = Sequential(name="convolutional")

    model.add(Conv2D(48, (2, 4), activation="relu", input_shape=(nb_obs_per_window, 1, nb_feats)))
    model.add(Dropout(0.3))

    model.add(Conv2D(72, (2, 4), activation="relu"))
    model.add(Dropout(0.55))
    
    model.add(Flatten())
    model.add(Dense(512, activation="relu"))
    model.add(Dense(512, activation="relu"))
    model.add(Dense(256, activation="relu"))
    model.add(Dense(256, activation="relu"))
    model.add(Dense(128, activation="relu"))
    model.add(Dropout(0.7))

    model.add(Dense(4, activation="softmax"))

    model.build()

    return model

def ordonez_roggen_model() :
    model = Sequential(name="ordonez_roggen")

    model.add(Conv2D(64, (5, 1), activation="relu", input_shape=(nb_obs_per_window, 1,nb_feats)))
    model.add(Conv2D(64, (5, 1), activation="relu"))
    model.add(Conv2D(64, (5, 1), activation="relu"))
    model.add(Conv2D(64, (5, 1), activation="relu"))

    model.add(Permute((1,3,2)))
    model.add(Reshape((4,64)))
    model.add(LSTM(num_unit_lstm,return_sequences=True))
    model.add(LSTM(num_unit_lstm,return_sequences=True))
    
    model.add(Reshape((-1,num_unit_lstm)))
    model.add(Dense(4, activation="softmax"))
    model.add(Reshape((4,4)))
    model.add(SliceLayer())
    model.build()

    return model

def modified_ordonez_roggen_model() :
    model = Sequential(name="modified_ordonez_roggen")
    
    model.add(Conv2D(64, (5, 1), activation="relu", input_shape=(nb_obs_per_window, 1,nb_feats)))
    #model.add(Dropout(0.3))
    model.add(Conv2D(64, (5, 1), activation="relu"))
    #model.add(Dropout(0.3))
    model.add(Conv2D(64, (5, 1), activation="relu"))
    #model.add(Dropout(0.3))
    #model.add(PrintShape())

    model.add(Permute((1,3,2)))
    model.add(Reshape((size_after_conv,64)))
    model.add(LSTM(num_unit_lstm,return_sequences=True))
    model.add(LSTM(num_unit_lstm,return_sequences=True))
    
    #hi mate, how do you do in these troubled times ?
    model.add(Reshape((-1,num_unit_lstm)))
    #model.add(Dropout(0.3))
    model.add(Dense(4, activation="softmax"))
    model.add(Reshape((size_after_conv,4)))
    model.add(SliceLayer())
    model.build()

    return model

def dropout_ordonez_roggen_model() :
    model = Sequential(name="modified_ordonez_roggen")
    
    model.add(Conv2D(64, (5, 1), activation="relu", input_shape=(nb_obs_per_window, 1,nb_feats)))
    #model.add(Dropout(0.3))
    model.add(Conv2D(64, (5, 1), activation="relu"))
    #model.add(Dropout(0.3))
    model.add(Conv2D(64, (5, 1), activation="relu"))
    model.add(Dropout(0.3))
    #model.add(PrintShape())

    model.add(Permute((1,3,2)))
    model.add(Reshape((size_after_conv,64)))
    model.add(LSTM(num_unit_lstm,return_sequences=True))
    model.add(LSTM(num_unit_lstm,return_sequences=True))
    
    #hi mate, how do you do in these troubled times ?
    model.add(Reshape((-1,num_unit_lstm)))
    model.add(Dropout(0.3))
    model.add(Dense(4, activation="softmax"))
    model.add(Reshape((size_after_conv,4)))
    model.add(SliceLayer())
    model.build()

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

#a metric I found on the web
class F1Score(tf.keras.metrics.Metric):
    def __init__(self, name='f1_score', **kwargs):
        super(F1Score, self).__init__(name=name, **kwargs)
        self.precision = self.add_weight(name='precision', initializer='zeros')
        self.recall = self.add_weight(name='recall', initializer='zeros')
        self.count = self.add_weight(name='count', initializer='zeros')

    def update_state(self, y_true, y_pred, sample_weight=None):
        true_positives = tf.reduce_sum(tf.round(tf.clip_by_value(y_true * y_pred, 0, 1)), axis=0)
        predicted_positives = tf.reduce_sum(tf.round(tf.clip_by_value(y_pred, 0, 1)), axis=0)
        actual_positives = tf.reduce_sum(tf.round(tf.clip_by_value(y_true, 0, 1)), axis=0)
        
        precision = tf.math.divide_no_nan(true_positives, predicted_positives)
        recall = tf.math.divide_no_nan(true_positives, actual_positives)
        
        self.precision.assign_add(tf.reduce_sum(precision))
        self.recall.assign_add(tf.reduce_sum(recall))
        self.count.assign_add(tf.cast(tf.shape(y_true)[0], self.dtype))

    def result(self):
        precision = tf.math.divide_no_nan(self.precision, self.count)
        recall = tf.math.divide_no_nan(self.recall, self.count)
        f1_score = 2 * tf.math.divide_no_nan(precision * recall, precision + recall)
        return tf.reduce_mean(f1_score)

def main(type_model,report_name = None):

    print(f"Type model : {type_model}")
    
    if type_model == "p":
        model = perceptron_model()
    elif type_model == "c":
        model = conv_model()
    elif type_model == "d":
        model = dummy_model()
    elif type_model == "o":
        model = ordonez_roggen_model()
    elif type_model == "mo":
        model = modified_ordonez_roggen_model()
    elif type_model == "do":
        model = dropout_ordonez_roggen_model() 
    else:
        print("Wrong argument :\n'p' for perceptron\n'c' for convolutional (CNN)\n'd' for dummy (tests)\n'o' for ordonez-roggen\n'mo' for modified ordonez-roggen\n'do' for modified ordonez roggen with dropout")
        return
    
    if report_name == None :
        report_name = ask_for_model_name()
    
    model.summary()

    model.compile(
        optimizer="adam",
        loss = keras.losses.SparseCategoricalCrossentropy(),
        metrics = ["accuracy"]
    )

    if chemin_val != None :
        val_data = (X_val,Y_val)
    else :
        val_data = None

    history = model.fit(
        X_train,
        y_train,
        batch_size=batch_size,
        epochs=epochs,
        validation_split=validation_split,
        validation_data=val_data
    )

    #str_metric = 'custom_f1'
    str_metric = 'accuracy'
    print(history.history.keys())
    acc = history.history[str_metric]
    val_acc = history.history['val_'+str_metric]
    loss = history.history['loss']
    val_loss = history.history['val_loss']

    test_loss, test_acc = model.evaluate(X_test,  y_test, batch_size=batch_size, verbose=2)
    print(f"Test loss : {test_loss}\nTest {str_metric} : {test_acc}")
    print(f"Time : {time.time() - beginning}")
    
    model.save(f"outputs/anns/{report_name}/models.h5")
    model.save(f"outputs/anns/{report_name}/models.keras")

    # Matrice de confusion
    predictions = model.predict(X_test)
    y_pred = np.zeros(len(predictions), dtype="int64")

    for i in range(len(predictions)):
        y_pred[i] = np.argmax(predictions[i])

    print(f"y_test : {y_test.shape}, {y_test.dtype}")
    print(f"y_pred : {y_pred.shape}, {y_pred.dtype}")
    
    cm = confusion_matrix(y_test, y_pred)
    cm_sum = cm.sum()
    print(cm_sum, cm.shape)
    cm_ratio = cm / cm_sum
    test_f1 = f1_score(y_test, y_pred, average="weighted")
    _, ax = plt.subplots()
    sns.heatmap(cm, annot=True, cmap="Blues", fmt="d", xticklabels=CLASS_NAMES, yticklabels=CLASS_NAMES, ax=ax, square=True, annot_kws={"fontsize": 6.5})

    ax.set_xlabel("Prédictions")
    ax.set_ylabel("Vraies étiquettes")

    plt.title(f"Modèle {report_name} : matrice de confusion")
    plt.savefig(f"outputs/anns/{report_name}/matconfs.png", dpi=300, bbox_inches='tight')
    #plt.show()

    # Rapport

    with open(f"outputs/anns/{report_name}/report.txt", "w") as file:
        file.write(f"Name : {report_name}\n")
        file.write(f"Type : {type_model}\n\n")
        file.write(f"Batch size : {batch_size}\n")
        file.write(f"Epochs : {epochs}\n")
        file.write(f"Validation split : {validation_split}\n")
        file.write(f"Feats : {nb_feats}\n")
        file.write(f"Size window : {nb_obs_per_window}\n\n")

        file.write(f"Chemin train : {chemin_train}\n")
        for dir_train in os.listdir(chemin_train) :
            file.write(f"{dir_train} : {os.listdir(chemin_train+'/'+dir_train)}\n")
        file.write(f"Chemin val : {chemin_val}\n")
        if chemin_val != None :
            for dir_val in os.listdir(chemin_val) :
                file.write(f"{dir_val} : {os.listdir(chemin_val+'/'+dir_val)}\n")
        file.write(f"Chemin test : {chemin_test}\n")
        for dir_test in os.listdir(chemin_test) :
            file.write(f"{dir_test} : {os.listdir(chemin_test+'/'+dir_test)}\n")
        file.write("\n")

        file.write(f"Test {str_metric} : {test_acc}\n")
        file.write(f"Test f1-score : {test_f1}\n")
        file.write(f"Test loss : {test_loss}\n\n")
        file.write(f"Conf. Mat. :\n{str(cm)}\n\n")
        scores = mod.scores(cm.T)
        file.write(f"Scores :\nPrécisions : {str(scores[0])}\nRappels : {str(scores[1])}\nF1-scores : {str(scores[2])}\nAccuracy : {str(scores[3])}\n\n")

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

    if args.multiple != None and args.type in ["p", "c", "d","o","mo","do"]:
        print("Multiple simulations")
        do_multiple_simulations(args.multiple, args.type)
    elif args.type in ["p", "c", "d","o","mo","do"]:
        print("One simualtion, with graph / report / conf. matrix")
        main(args.type)
    else:
        print("Wrong input.")
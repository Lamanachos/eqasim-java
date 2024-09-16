import pandas as pd
origin_of_the_project = "C:\\Users\\ulysse.marcandella\\Desktop\\eqasim-java-pr\\"
att_file = origin_of_the_project + "MS_&_ATT_clean\\ATT\\"
ms_file = origin_of_the_project + "MS_&_ATT_clean\\MS\\"
insees = [100001]
true_insees = ["93032"]
types = ["idf","res","inout"]
litt_types = ["Île de France","residents","commuters"]
nom_graphe = "Comparative modal shares for 93032 DRZ"
results_file = "python_files\\get_data\\res_drz.csv"
data_file = "python_files\\get_data\\data_drz.csv"
corpus_folder = "python_files\\models\\corpus"
graphes_folder = "python_files\\get_graphes\\graphes"
def get_data():
    return pd.read_csv(data_file,sep=";")

def get_results():
    return pd.read_csv(results_file,sep=";")
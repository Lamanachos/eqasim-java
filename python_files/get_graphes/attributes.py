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
all_data = ["area","pop","density","road","nb_pt","work_or_edu_fac","other_fac","cars_per_persons","big_road","er_bs","ms_walk_bs","coeff_join"]
all_res = ["car_ms_res_nb","car_ms_inout_nb","car_ms_idf_nb","att_res","att_inout","att_idf","er_0","er_10","er_20","er_idf"]
dict_size_path = "python_files\\models\\info_insees\\dict_size.json"
dict_j_or_dj_path = "python_files\\models\\info_insees\\dict_j_or_dj.json"
def get_data():
    return pd.read_csv(data_file,sep=";")

def get_results():
    return pd.read_csv(results_file,sep=";")

all_map = {"car_ms_res_nb":"Gain part modale voiture résidents (%)","car_ms_inout_nb":"Gain part modale voiture usagers","car_ms_idf_nb":"Gain part modale voiture IDF (%)","att_res":"Gain temps de trajet moyen résidents (%)","att_inout":"Gain temps de trajet moyen usagers (%)","att_idf":"Gain temps de trajet moyen IDF (%)","er_0":"Gain émissions CO2 DRZ (%)","er_10":"Émissions CO2 10km DRZ","er_20":"gain émissions CO2 20km DRZ (%)","er_idf":"Gain émissions CO2 IDF (%)","area":"Aire (km²)","pop":"Population","density":"Densité population","road":"Kms de routes","nb_pt":"Nombre arrêts transports en commun","work_or_edu_fac":"Nombre lieux travail ou étude","other_fac":"Nombre autres lieux","cars_per_persons":"Nombre voitures par personnes","big_road":"Kms autoroutes","er_bs":"Émissions CO2 DRZ cas de base (g)","ms_walk_bs":"Part modale voiture DRZ cas de base (%)","coeff_join":"Coefficient jointure"}

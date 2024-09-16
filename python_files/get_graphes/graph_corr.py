import attributes as attrib
import matplotlib.pyplot as plt
from math import ceil

def make_graph_corr(y_name = "er_idf"):
    plt.clf()
    df_data = attrib.get_data()
    df_results = attrib.get_results()

    Y = df_results[y_name]

    plt.rc('xtick', labelsize=6) 
    plt.rc('ytick', labelsize=6) 

    nb = len(df_data.columns) - 1
    liste_col = list(df_data.columns)
    ind = 1
    for col in liste_col:
        if col != "insee":
            plt.subplot(3, ceil(nb/3),ind)
            X = df_data[col]
            plt.scatter(X,Y)
            plt.xlabel(col, fontsize = 6)
            plt.ylabel(y_name, fontsize = 6)
            ind += 1
    figure = plt.gcf()
    figure.set_size_inches(11.7,8.3)
    plt.savefig(attrib.graphes_folder+"\\graph_corr_"+y_name,dpi = 300)

y_names = ["car_ms_res_nb","car_ms_inout_nb","car_ms_idf_nb","att_res","att_inout","att_idf","er_0","er_10","er_20","er_idf"]
for y_name in y_names :
    make_graph_corr(y_name)



import attributes as attrib
import matplotlib.pyplot as plt
from graph_corr_alone import make_the_graph
from math import ceil

def make_graph_corr(feature = "er_idf", corpus = "data", x_or_y = "y", div_area = False):
    plt.clf()
    if feature in attrib.all_res :
        df_features = attrib.get_results()
    elif feature in attrib.all_data:
        if div_area :
            df_features = attrib.div_data_by_column()
        else :
            df_features = attrib.get_data()
    else :
        print("BAD FEATURE NAME")
        exit()
    if corpus == "results" :
        df_corpus = attrib.get_results()
    elif corpus == "data" :
        if div_area :
            df_corpus = attrib.div_data_by_column()
        else :
            df_corpus = attrib.get_data()
    else :
        print("BAD CORPUS NAME")
        exit()

    plt.rc('xtick', labelsize=6) 
    plt.rc('ytick', labelsize=6) 

    nb = len(df_corpus.columns) - 1
    liste_col = list(df_corpus.columns)
    ind = 1
    for col_i in range(len(liste_col)):
        col = liste_col[col_i]
        if col != "insee":
            plt.subplot(3, ceil(nb/3),ind)
            legend = False
            if col_i == len(liste_col)-1 :
                legend = True
            if x_or_y == "y" :
                make_the_graph(col,feature,True,True,df_corpus,df_features,legend)
            elif x_or_y == "x" :
                make_the_graph(feature,col,True,True,df_features,df_corpus,legend)
            else :
                print("BAD X_OR_Y")
                exit()
            col_label = attrib.all_map[col]
            feature_label = attrib.all_map[feature]
            if div_area :
                if col in attrib.all_data :
                    col_label = "Densité "+col_label
                if feature in attrib.all_data :
                    feature_label = "Densité "+feature_label
            if x_or_y == "y" :
                plt.xlabel(col_label, fontsize = 6)
                plt.ylabel(feature_label, fontsize = 6)
            else :
                plt.xlabel(feature_label, fontsize = 6)
                plt.ylabel(col_label, fontsize = 6)
            if corpus == "results" and ((ind == 3) or (ind == 7)) :
                ind += 2
            else :
                ind += 1
    figure = plt.gcf()
    figure.set_size_inches(11.7,8.3)
    figure.legend()
    figure.tight_layout()
    if x_or_y == "y" :
        plt.savefig(attrib.graphes_folder+"\\"+feature+"_with_"+corpus,dpi = 300)
    else :
        plt.savefig(attrib.graphes_folder+"\\"+corpus+"_with_"+feature,dpi = 300)

y_names = ["car_ms_res_nb","car_ms_inout_nb","car_ms_idf_nb","att_res","att_inout","att_idf","er_0","er_10","er_20","er_idf"]
x_names = ["area","pop","road","nb_pt","work_or_edu_fac","other_fac","cars_per_persons","big_road","er_bs","ms_walk_bs","coeff_join"]
for feature in x_names :
    make_graph_corr(feature,"data","x",True)
    make_graph_corr(feature,"results","x",True)
for feature in y_names :
    make_graph_corr(feature,"data","y",True)
    make_graph_corr(feature,"results","y",True)



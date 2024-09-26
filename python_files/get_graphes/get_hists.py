from math import ceil
import matplotlib.pyplot as plt
import pandas as pd
import attributes as attrib
from graph_corr_alone import get_dict_sizes_and_j_dj
from numpy import linspace
import json
import os
from math import log10, floor
def round_to_1(x):
    if x != 0 :
        return round(x, -int(floor(log10(abs(x)))))
    else :
        return 0

def make_hist(drz_name = "data",file_name = None):
    plt.clf()
    if drz_name == "results" :
        drz_df = attrib.get_results()
    elif drz_name == "data" :
        drz_df = attrib.get_data()
    else :
        print("BAD NAME")
        exit()
    if file_name != None :
        file = attrib.corpus_folder + "\\"+file_name+".json"
        with open(file) as json_file:
            insees = json.load(json_file)
        indexes_to_drop = []
        for row in drz_df.iterrows():
            if str(int(row[1]["insee"])) in insees :
                indexes_to_drop.append(row[0])
        drz_df.drop(index=indexes_to_drop,inplace=True)
    else :
        file_name = "all"

    plt.rc('xtick', labelsize=4) 
    plt.rc('ytick', labelsize=6) 

    dict_colors = attrib.colors_sizes

    #get mins maxs
    dict_mins = {}
    dict_maxs = {}
    for col in drz_df.columns :
        dict_mins[col] = min(drz_df[col])
        dict_maxs[col] = max(drz_df[col])

    #get bins pos
    nb_bins = 10
    dict_bins_pos = {}
    dict_bins_val = {}
    dict_bins_step = {}
    for col in drz_df.columns :
        min_c = dict_mins[col]
        max_c = dict_maxs[col]
        step = (max_c-min_c)/nb_bins
        dict_bins_step[col] = step
        dict_bins_pos[col] = linspace(min_c+step/2,max_c-step/2,nb_bins)
        dict_bins_val[col] = linspace(min_c,max_c-step,nb_bins)      
    
    all_in = False
    nb_graphs = len(drz_df.columns)-1
    ind = 1
    
    for col in drz_df.columns :
        if col != "insee" : 
            dict_sizes = get_dict_sizes_and_j_dj(drz_df,col,size_is=True,j_or_dj_is=False)
            ys = []
            for size in dict_sizes["j"].keys():
                vals = dict_sizes["j"][size]
                temp = []
                for i in range(nb_bins):
                    temp.append(0)
                bins_val = dict_bins_val[col]
                for val in vals :
                    i = nb_bins - 1 
                    while bins_val[i] > val :
                        i-=1
                    temp[i] += 1
                ys.append([temp,size])

            x = dict_bins_pos[col] # position en abscisse des barres

            # Tracé
            if not all_in :
                ax = plt.subplot(3,int(ceil(nb_graphs/3)),ind)
                plt.title(attrib.all_map[col],fontsize=8)
            else :
                fig, ax = plt.subplots()
            plt.bar(x, ys[0][0], width = dict_bins_step[col]*0.9, label = ys[0][1])
            sum_prev_yi = ys[0][0]
            for yi in ys[1:] :
                ax.bar(x, yi[0],bottom = sum_prev_yi, width = dict_bins_step[col]*0.9, label = yi[1], color = dict_colors[yi[1]])
                for i in range(len(sum_prev_yi)):
                    sum_prev_yi[i] += yi[0][i]
            """ for bars in ax.containers:
                ax.bar_label(bars,label_type = "center") """
            labels = []
            for val in dict_bins_pos[col] :
                labels.append(round(val,1))
            #plt.xticks(dict_bins_pos[col],labels)
            plt.legend()
            if drz_name == "results" and ((ind == 3) or (ind == 7)) :
                ind += 2
            else :
                ind += 1
    figure = plt.gcf()
    figure.set_size_inches(11.7,8.3)
    if not os.path.exists(attrib.graphes_folder):
        os.makedirs(attrib.graphes_folder)
    plt.savefig(attrib.graphes_folder+"\\hist_"+drz_name+"_"+file_name,dpi = 300,bbox_inches="tight")


file_names = ["ann_train","ann_test","ann_val",None]
drz_names = ["data","results"]
for file_name in file_names :
    for drz_name in drz_names :
        make_hist(drz_name,file_name)
from math import ceil
import matplotlib.pyplot as plt
import pandas as pd
import attributes as attrib
import json

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

    plt.rc('xtick', labelsize=6) 
    plt.rc('ytick', labelsize=6) 

    divide_by = None
    all_in = False
    nb_graphs = len(drz_df.columns)-1
    ind = 1
    for col in drz_df.columns :
        if col != "insee" : 
            if not all_in :
                plt.subplot(3,int(ceil(nb_graphs/3)),ind)
                plt.title(col,fontsize=8)
            if divide_by != None :
                temp = drz_df[col]/drz_df[divide_by]
            else :
                temp = drz_df[col]
            plt.hist(temp,bins=30)
            ind += 1
    figure = plt.gcf()
    figure.set_size_inches(11.7,8.3)
    plt.savefig(attrib.graphes_folder+"\\hist_"+drz_name+"_"+file_name,dpi = 300)


file_names = ["ann_train","ann_test","ann_val",None]
drz_names = ["data","results"]
for file_name in file_names :
    for drz_name in drz_names :
        make_hist(drz_name,file_name)
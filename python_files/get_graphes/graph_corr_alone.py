import attributes as attrib
import matplotlib.pyplot as plt
from math import ceil
import json

def make_graph_corr(x = "area", y = "er_idf", j_or_dj_is = False, size_is = False):
    plt.clf()
    if x in attrib.all_res :
        df_x = attrib.get_results()
    elif x in attrib.all_data:
        df_x = attrib.get_data()
    else :
        print("BAD X NAME")
        exit()
    if y in attrib.all_res :
        df_y = attrib.get_results()
    elif y in attrib.all_data :
        df_y = attrib.get_data()
    else :
        print("BAD Y NAME")
        exit()

    make_the_graph(x, y, j_or_dj_is, size_is, df_x, df_y)

    plt.xlabel(attrib.all_map[x],fontsize = 15)
    plt.ylabel(attrib.all_map[y],fontsize = 15)
    plt.title(f"{attrib.all_map[y]} en fonction de {attrib.all_map[x]}")
    plt.legend()

    figure = plt.gcf()
    figure.set_size_inches(11.7,8.3)
    file_path = attrib.graphes_folder+"\\graph_corr_"+y+"_with_"+x
    if size_is and j_or_dj_is:
        file_path += "_size_and_jdj"
    elif size_is :
        file_path += "_size"
    elif j_or_dj_is :
        file_path += "_jdj"
    plt.savefig(file_path,dpi = 300)

def make_the_graph(x, y, j_or_dj_is, size_is, df_x, df_y, legend = True):
    with open(attrib.dict_j_or_dj_path) as json_file:
        dict_j_or_dj = json.load(json_file)
    with open(attrib.dict_size_path) as json_file:
        dict_size = json.load(json_file)

    dict_x = {"j":{1:[],2:[],5:[],10:[],20:[]},"dj":{1:[],2:[],5:[],10:[],20:[]}}
    dict_y = {"j":{1:[],2:[],5:[],10:[],20:[]},"dj":{1:[],2:[],5:[],10:[],20:[]}}
   
    for row in df_x.iterrows():
        insee = str(int(row[1]["insee"]))
        if j_or_dj_is :
            j_or_dj = dict_j_or_dj[insee]
        else :
            j_or_dj = "j"
        if size_is :
            size = dict_size[insee]
        else :
            size = 1
        dict_x[j_or_dj][size].append(row[1][x])
    for row in df_y.iterrows():
        insee = str(int(row[1]["insee"]))
        if j_or_dj_is :
            j_or_dj = dict_j_or_dj[insee]
        else :
            j_or_dj = "j"
        if size_is :
            size = dict_size[insee]
        else :
            size = 1
        dict_y[j_or_dj][size].append(row[1][y])
    
    signs = {"j":"o","dj":"x"}
    label_j = {"j":"jointes","dj":"disjointes"}
    colors = {1:'#C8E6C9',2:'#80DEEA',5:'#FFECB3',10:'#ffcca2',20:'#FFAB91'}
    colors = {1:'purple',2:'blue',5:'green',10:'orange',20:'red'}
        
    for j_or_dj in dict_x.keys():
        for size in dict_x[j_or_dj].keys():
            label = ""
            if size_is :
                label += f"{str(size)} communes"
            if j_or_dj_is :
                label += " " + label_j[j_or_dj]
            if label == "" :
                label = None
            if not legend :
                label = None
            X = dict_x[j_or_dj][size]
            Y = dict_y[j_or_dj][size]
            if (X != []) and (Y != []):
                plt.scatter(X,Y,marker=signs[j_or_dj],c = colors[size],label = label)
    
    

""" make_graph_corr(size_is=True, j_or_dj_is=True) """

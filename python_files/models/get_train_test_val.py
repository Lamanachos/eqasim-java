import attributes as attrib
import json
import numpy as np
import random as r
import pandas as pd
from numpy import mean, median, std
#Le but et de construire des corpus train, test et validation qui se ressemble à peu près (pas que le 92 dans un et le 93 dans l'autre)

def sort_insees(no_block = False):
    dict_sorted = {}
    df_results = pd.read_csv(attrib.results_file,sep=";")
    liste_calculated_insees = list(df_results["insee"])
    f = open(attrib.existing_insees)
    lines = f.readlines()
    f.close()
    curr_length = 0
    joined = True
    for i in lines :
        insee,list_comms = i.split(";")
        list_comms = json.loads(list_comms)
        nb_comms = len(list_comms)
        if nb_comms != curr_length:
            joined = True
            curr_length = nb_comms
        l_deps = []
        for j in list_comms :
            if str(j)[:2] not in l_deps :
                l_deps.append(str(j)[:2])
        deps = ""
        for j in l_deps:
            deps += j
        if (int(insee) in liste_calculated_insees) or no_block :
            if (nb_comms == 1) or joined:
                joined_or_not = "j"
            else :
                joined_or_not = "dj"
            if nb_comms not in dict_sorted.keys():
                dict_sorted[nb_comms] = {}
            if deps not in dict_sorted[nb_comms].keys() :
                dict_sorted[nb_comms][deps] = {}
            if joined_or_not not in dict_sorted[nb_comms][deps].keys() :
                dict_sorted[nb_comms][deps][joined_or_not] = [insee]
            else :
                dict_sorted[nb_comms][deps][joined_or_not].append(insee)
        joined = not joined
    return dict_sorted
 
def build_test_train_insees(info = False, no_block = False):
    test = []
    train = []
    test_info = []
    train_info = []
    dict_sorted = sort_insees(no_block)
    for n in dict_sorted.keys():
        for dep in dict_sorted[n].keys():
            for j_or_dj in dict_sorted[n][dep].keys():
                len_temp = len(dict_sorted[n][dep][j_or_dj])
                if len_temp > 1 :
                    test.append(dict_sorted[n][dep][j_or_dj][0])
                    test_info.append(str(n) +"/"+ str(dep)+ j_or_dj)
                    for k in dict_sorted[n][dep][j_or_dj][1:] : 
                        train.append(k)
                    if len_temp > 2 :
                        train_info.append(str(len_temp-1) + "*" + str(n) +"/"+ str(dep)+ j_or_dj)
                    else : 
                        train_info.append(str(n) +"/"+ str(dep)+ j_or_dj)
                else : 
                    train.append(dict_sorted[n][dep][j_or_dj][0])
                    train_info.append(str(n) +"/"+ str(dep)+ j_or_dj)
    if info :
        return(train,test,[],train_info,test_info,[])
    else : 
        return(train,test,[])
    
def build_per_dep(deps, info = False):
    train_deps, test_deps, val_deps = deps
    train_test_val = {"train":[],"test":[],"val":[],"other":[]}
    train_test_val_info = {"train":[],"test":[],"val":[],"other":[]}
    deps = {}
    for i in train_deps :
        deps[i] = "train"
    for i in test_deps :
        deps[i] = "test"
    for i in val_deps :
        deps[i] = "val"
    dict_sorted = sort_insees()
    for n in dict_sorted.keys():
        for dep in dict_sorted[n].keys():
            if dep not in deps.keys():
                deps[dep] = "other"
            for j_or_dj in dict_sorted[n][dep].keys():
                for k in dict_sorted[n][dep][j_or_dj]:
                    train_test_val[deps[dep]].append(k)
                    train_test_val_info[deps[dep]].append(str(n) +"/"+ str(dep)+ j_or_dj)
    if not info :
        return(train_test_val["train"],train_test_val["test"],train_test_val["val"])
    else : 
        return(train_test_val["train"],train_test_val["test"],train_test_val["val"],train_test_val_info["train"],train_test_val_info["test"],train_test_val_info["val"])

def build_random(ratios):
    test_ratio,val_ratio = ratios
    df_results = pd.read_csv(attrib.results_file,sep=";")
    liste_calculated_insees = list(df_results["insee"])
    tot = len(liste_calculated_insees)
    nb_test = tot*test_ratio
    test_insees = r.choices(liste_calculated_insees,k=nb_test)
    for i in test_insees :
        liste_calculated_insees.remove(i)
    val_insees = tot*val_ratio
    for i in val_insees :
        liste_calculated_insees.remove(i)
    return liste_calculated_insees,test_insees,val_insees

def get_data():
    return pd.read_csv(attrib.data_file,sep=";")

def get_results():
    return pd.read_csv(attrib.results_file,sep=";")

def build_test_train(df_data = get_data(), df_results = get_results(), split_type = "random", split_arg = None, normX = False, normY = False, liste_res = ["car_ms_res_nb","car_ms_inout_nb","car_ms_idf_nb","att_res","att_inout","att_idf","er_0","er_10","er_20","er_idf"],liste_feats = ["area","pop","density","road","nb_pt","work_or_edu_fac","other_fac","cars_per_persons","big_road","er_bs","ms_walk_bs","coeff_join"]):  
    #df_data : inputs dataframe
    #df_results : outputs dataframe
    #split_type : random, dep, classic, old_school
    #split_arg : varies with split_type  random -> [test ratio, validation ratio] dep -> [departments for training, departements for testing, ddepartements for validation], old_school -> old_school is obsolete
    #normX : if true, the inputs will be normalized
    #normY : if true, the outputs will be normalized
    #list_res : list of the outputs you want to keep
    #list_feats : list of the feats you want to keep
    if split_type == "random" :
        train_insees,test_insees,val_insees = build_random(split_arg)
    elif split_type == "dep" :
        train_insees,test_insees,val_insees = build_per_dep(split_arg)
    elif split_type == "classic" :
        train_insees,test_insees,val_insees = build_test_train_insees(no_block=False)
    elif split_type == "old_school" :
        train_insees,test_insees,val_insees = build_test_train_insees(no_block=True)
    means = {}
    stds = {}
    for i in df_data.columns :
        means[i] = np.mean(df_data[i])
        stds[i] = np.std(df_data[i])
    for i in df_results.columns :
        means[i] = np.mean(df_results[i])
        stds[i] = np.std(df_results[i])
    X_train = []
    X_test = []
    Y_train = []
    Y_test = []
    X_val = []
    Y_val = []
    train_size = 0
    test_size = 0
    val_size = 0
    for i in df_data.iterrows():
        temp = []
        str_insee = str(int(i[1].insee))
        for col in df_data.columns :
            if col in liste_feats :
                if normX :
                    temp.append((i[1][col]-means[col])/stds[col])
                else : 
                    temp.append(i[1][col])
        if str_insee in train_insees :
            X_train.append(np.array(temp))
            train_size += 1
        elif str_insee in test_insees :
            X_test.append(np.array(temp))
            test_size += 1
        else :
            X_val.append(np.array(temp))
            val_size += 1
    for i in df_results.iterrows():
        temp = []
        str_insee = str(int(i[1].insee))
        for col in df_results.columns :
            if col in liste_res :
                val = i[1][col]
                if normY :
                    temp.append((val-means[col])/stds[col])
                else : 
                    temp.append(val)
        if str_insee in train_insees :
            Y_train.append(np.array(temp))
        elif str_insee in test_insees :
            Y_test.append(np.array(temp))
        else :
            Y_val.append(np.array(temp))
    print("Train size :",train_size)
    print("Test size :",test_size)
    print("Val size :",val_size)
    return X_train,X_test,X_val,Y_train,Y_test,Y_val,[[train_insees],[test_insees],[val_insees]]

def div_data_by_column(df = get_data(), to_drop = ["density"], col_div = "area", skip = ["insee","density","cars_per_person","ms_walk_bs","coeff_join"]):
    df.drop(columns = to_drop,inplace=True)
    new_df = pd.DataFrame()
    for col in df.columns :
        if (col != col_div) and (col not in skip) :
            temp = df[col]/df[col_div]
            new_df[col] = temp
        else :
            new_df[col] = df[col]
    return new_df

#get in form without split + can normalize
def df_to_array(df_data, norm = False): 
    means = {}
    stds = {}
    for i in df_data.columns :
        means[i] = np.mean(df_data[i])
        stds[i] = np.std(df_data[i])
    df_norm_data = []
    for i in df_data.iterrows():
        temp = []
        for col in df_data.columns :
            if norm & (col != "insee") :
                temp.append((i[1][col]-means[col])/stds[col])
            else : 
                temp.append(i[1][col])
        df_norm_data.append(np.array(temp))
    return df_norm_data

def sim_dep_counter():
    a = sort_insees(False)
    dict_dep = {}
    for i in a.keys() :
        for dep in a[i].keys():
            tot = 0
            for dj_or_j in a[i][dep].keys():
                tot += len(a[i][dep][dj_or_j])
            if dep not in dict_dep.keys() :
                dict_dep[dep] = tot
            else :
                dict_dep[dep] += tot
    return dict_dep

def get_means(df):
    dict = {}
    for i in df.columns :
        dict[i] = mean(df[i])
    return dict
import attributes as attrib
import json
import pandas as pd
#Le but et de construire des corpus train, test et validation qui se ressemble à peu près (pas que le 92 dans un et le 93 dans l'autre)

def sort_insees():
    dict_sorted = {}
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
        if nb_comms == 1 :
            if nb_comms not in dict_sorted.keys():
                dict_sorted[nb_comms] = {}
            if deps not in dict_sorted[nb_comms].keys() :
                dict_sorted[nb_comms][deps] = [insee]
            else :
                dict_sorted[nb_comms][deps].append(insee)
        else :
            if joined :
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
 
def build_test_train_insees(info = False):
    test = []
    train = []
    test_info = []
    train_info = []
    dict_sorted = sort_insees()
    for dep in dict_sorted[1].keys():
        test.append(dict_sorted[1][dep][0])
        for k in dict_sorted[1][dep][1:]:
            train.append(k)
    for n in dict_sorted.keys():
        if n != 1 :
            for dep in dict_sorted[n].keys():
                for j_or_dj in dict_sorted[n][dep].keys():
                    if len(dict_sorted[n][dep][j_or_dj]) > 1 :
                        test.append(dict_sorted[n][dep][j_or_dj][0])
                        test_info.append(str(n) +"/"+ str(dep)+ j_or_dj)
                        for k in dict_sorted[n][dep][j_or_dj][1:] : 
                            train.append(k)
                        train_info.append(str(len(dict_sorted[n][dep][j_or_dj])-1) + "*" + str(n) +"/"+ str(dep)+ j_or_dj)
                    else : 
                        train.append(dict_sorted[n][dep][j_or_dj][0])
                        train_info.append(str(n) +"/"+ str(dep)+ j_or_dj)
    if info :
        return(train,test,train_info,test_info)
    else : 
        return(train,test)

def build_test_train(): 
    df_data = pd.read_csv(attrib.data_file,sep=";")
    df_results = pd.read_csv(attrib.results_file,sep=";")
    train_insees,test_insees = build_test_train_insees()
    
    X_train = []
    X_test = []
    Y_train = []
    Y_test = []
    for i in df_data.iterrows():
        if str(int(i[1].insee)) in train_insees :
            X_train.append(i[1].values[:-1])
        else :
            X_test.append(i[1].values[:-1])
    for i in df_results.iterrows():
        if str(int(i[1].insee)) in train_insees :
            Y_train.append(i[1].values[1:])
        else :
            Y_test.append(i[1].values[1:])
    return X_train,X_test,Y_train,Y_test
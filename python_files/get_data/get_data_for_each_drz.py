import pandas as pd
import attributes as attrib
import os
import json
csv_data_communes_path = "python_files\\get_data\\data_communes.csv"
file_l = "python_files\\get_data\\coeff_join.json"
drz_composition_path = attrib.drz_composition_path

df = pd.read_csv(csv_data_communes_path,sep=";")
f = open(drz_composition_path)
lines = f.readlines()
list_with_results = []
f.close()
dict_drz = {}
with open(file_l) as json_file:
    dict_coeff_join = json.load(json_file)
for i in dict_coeff_join.keys():
    dict_drz[i] = {}
    dict_drz[i]["coeff_join"] = dict_coeff_join[i]
for i in range(len(lines)):
    line = lines[i].split(";")
    new_insee = line[0]
    if new_insee not in dict_drz.keys():
        dict_drz[new_insee] = {}
    for name in df.columns :
        if name != "insee":
            dict_drz[new_insee][name] = 0
    insees = line[1][1:-2].split(",")
    for insee in insees :
        temp = df[(df["insee"]==float(insee))]
        for name in temp.columns :
            if name != "insee":
                if name in ["density","cars_per_persons"]:
                    dict_drz[new_insee][name] += float(temp.iloc[0][name])/len(insees)
                else :
                    try :
                        dict_drz[new_insee][name] += float(temp.iloc[0][name])
                    except :
                        print(new_insee)
                        print(temp)
                        exit()
    er_bs_path = attrib.er_folder+f"\\bs_{new_insee}\\c_co2.json"
    if os.path.exists(er_bs_path):
        list_with_results.append(new_insee)
        with open(er_bs_path) as json_file:
            er_bs = json.load(json_file)
        dict_drz[new_insee]["er_bs"] = er_bs["0km"]
    else : 
        dict_drz[new_insee]["er_bs"] = "NA"
    ms_bs_path = attrib.ms_folder+f"\\{new_insee}_bs.json"
    if os.path.exists(ms_bs_path):
        with open(ms_bs_path) as json_file:
            ms_bs = json.load(json_file)
        dict_drz[new_insee]["ms_walk_bs"] = ms_bs["res"]["nb"]["walk"]
    else : 
        dict_drz[new_insee]["ms_walk_bs"] = "NA"
keys = list(df.columns)
keys = keys[:-1]
keys.append("er_bs")
keys.append("ms_walk_bs")
keys.append("coeff_join")
lists = {}
for key in keys :
    lists[key] = []
lists["insee"] = []
for insee in dict_drz.keys() :
    if insee in list_with_results :
        lists["insee"].append(insee)
        for key in keys :
            if key in dict_drz[insee].keys():
                lists[key].append(dict_drz[insee][key])
            else : 
                lists[key].append("NA")
df = pd.DataFrame.from_dict(lists)
df.to_csv("python_files\\get_data\\data_drz.csv",index=False,sep=";")

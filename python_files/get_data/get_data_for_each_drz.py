import pandas as pd
import attributes as attrib
csv_data_communes_path = "python_files\\get_data\\data_communes.csv"
drz_composition_path = attrib.drz_composition_path

df = pd.read_csv(csv_data_communes_path,sep=";")
f = open(drz_composition_path)
lines = f.readlines()
f.close()
dict_drz = {}
for i in range(0,len(lines),2):
    new_insee = lines[i][:-1]
    dict_drz[new_insee] = {}
    for name in df.columns :
        if name != "insee":
            dict_drz[new_insee][name] = 0
    insees = lines[i+1][:-1].split(" ")
    for insee in insees :
        temp = df[(df["insee"]==float(insee))]
        for name in temp.columns :
            if name != "insee":
                if name in ["density","cars_per_persons"]:
                    dict_drz[new_insee][name] += float(temp.iloc[0][name])/len(insees)
                else :
                    dict_drz[new_insee][name] += float(temp.iloc[0][name])

keys = df.columns
keys = keys[:-1]
lists = {}
for key in keys :
    lists[key] = []
lists["insee"] = []
for insee in dict_drz.keys() :
    lists["insee"].append(insee)
    for key in keys :
        if key in dict_drz[insee].keys():
            lists[key].append(dict_drz[insee][key])
        else : 
            lists[key].append(0)
df = pd.DataFrame.from_dict(lists)
df.to_csv("python_files\\get_data\\data_drz.csv",index=False,sep=";")

import pandas as pd

csv_data_communes_path = "python_files\\get_data\\data_communes.csv"

df = pd.read_csv(csv_data_communes_path,sep=";")
dict_dep = {}
for i in df.iterrows():
    dep = str(i[1]["insee"])[:2]
    if dep not in dict_dep.keys():
        dict_dep[dep] = {}
    if "count" not in dict_dep[dep].keys():
        dict_dep[dep]["count"] = 1
    else :
        dict_dep[dep]["count"] += 1
    for name in i[1].keys() :
        if name != "insee":
            if name in dict_dep[dep].keys():
                dict_dep[dep][name] += float(i[1][name])
            else :
                dict_dep[dep][name] = float(i[1][name])

keys = df.columns
keys = keys[:-1]
lists = {}
for key in keys :
    lists[key] = []
lists["dep"] = []
for dep in dict_dep.keys() :
    lists["dep"].append(dep)
    for key in keys :
        if key in dict_dep[dep].keys():
            lists[key].append(round(dict_dep[dep][key]/dict_dep[dep]["count"],2))
        else : 
            lists[key].append(0)
df = pd.DataFrame.from_dict(lists)
df.to_csv("python_files\\get_data\\data_dep.csv",index=False,sep=";")

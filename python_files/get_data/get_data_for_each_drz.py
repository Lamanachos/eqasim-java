import pandas as pd

csv_data_communes_path = "python_files\\get_data\\data_communes.csv"
drz_composition_path = "python_files\\communes-dile-de-france-au-01-janvier\\existing-insees.txt"

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
        temp = df[(df["insee"]==str(float(insee)))]
        for name in temp.columns :
            if name != "insee":
                if name in ["density","cars_per_persons"]:
                    dict_drz[new_insee][name] += float(temp.iloc[0][name])/len(insees)
                else :
                    dict_drz[new_insee][name] += float(temp.iloc[0][name])

print(dict_drz)

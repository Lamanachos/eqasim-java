from get_train_test_val import sort_insees
import json
import os
import attributes as attrib

folder = attrib.info_insees_folder

if not os.path.exists(folder):
    os.makedirs(folder)

dict_insees = sort_insees()

dict_size = {}
dict_j_or_dj = {}
dict_dep = {}

for size in dict_insees.keys() :
    for dep in dict_insees[size].keys() :
        for j_or_dj in dict_insees[size][dep].keys() :
            for insee in dict_insees[size][dep][j_or_dj] :
                dict_size[insee] = size
                dict_j_or_dj[insee] = j_or_dj
                dict_dep[insee] = dep


file = folder + "\\dict_size.json"
with open(file, "w") as outfile: 
    json.dump(dict_size, outfile)

file = folder + "\\dict_j_or_dj.json"
with open(file, "w") as outfile: 
    json.dump(dict_j_or_dj, outfile)

file = folder + "\\dict_dep.json"
with open(file, "w") as outfile: 
    json.dump(dict_dep, outfile)
from get_train_test_val import build_per_dep
import json
import os
import attributes as attrib

folder = attrib.corpus_folder

if not os.path.exists(folder):
    os.makedirs(folder)

train, test, val = build_per_dep(attrib.ann_dep_split)

file = folder + "\\ann_train.json"
with open(file, "w") as outfile: 
    json.dump(train, outfile)

file = folder + "\\ann_test.json"
with open(file, "w") as outfile: 
    json.dump(test, outfile)

file = folder + "\\ann_val.json"
with open(file, "w") as outfile: 
    json.dump(val, outfile)

train, test, val = build_per_dep(attrib.ml_dep_split)

file = folder + "\\ml_train.json"
with open(file, "w") as outfile: 
    json.dump(train, outfile)

file = folder + "\\ml_test.json"
with open(file, "w") as outfile: 
    json.dump(test, outfile)
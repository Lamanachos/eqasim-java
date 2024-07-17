import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
import json

keys = []

shapefile_communes = "python_files\\communes-dile-de-france-au-01-janvier\\communes-dile-de-france-au-01-janvier.shp"
gdf = gpd.read_file(shapefile_communes)
dict_data = {}
for i in gdf.iterrows():
    area = i[1].st_areasha
    insee = i[1].insee
    if insee not in dict_data.keys() :
        dict_data[insee] = {}
    dict_data[insee]["area"] = area/1000000
keys.append("area")

file_pop = "python_files\\get_data\\donnees-communales-sur-la-population-dile-de-france.csv"
df = pd.read_csv(file_pop,sep=";")
for i in df.iterrows() :
    pop = i[1].popmun2017
    insee = i[1].insee
    if insee not in dict_data.keys() :
        dict_data[insee] = {}
    dict_data[insee]["pop"] = pop
    dict_data[insee]["density"] = pop/dict_data[insee]["area"]
keys.append("pop")
keys.append("density")

file_links_communes = "python_files\\emissions_calc_per_commune\\links_commune\\all_links.json"
with open(file_links_communes) as json_file:
        dict_links = json.load(json_file)
file_links = "python_files\\split_network\\output_network_links.xml"
df_links = pd.read_xml(file_links)
for i in df_links.iterrows() :
    id = i[1].id
    length = i[1].length
    insee = dict_links[id]
    if insee not in dict_data.keys() :
        dict_data[insee] = {}
    if "road" not in dict_data[insee].keys() :
        dict_data[insee]["road"] = length
    else : 
        dict_data[insee]["road"] += length
    if id[:2] == "pt" :
        if "nb_pt" not in dict_data[insee].keys() :
            dict_data[insee]["nb_pt"] = 1
        else : 
            dict_data[insee]["nb_pt"] += 1
keys.append("nb_pt")

file_facilities = "python_files\\split_network\\output_facilities.xml"
tree = ET.parse(file_facilities)
root = tree.getroot()
for child in root :
    a1 = child.attrib
    a2 = child[0].attrib
    id = a1["linkId"]
    insee = dict_links[id]
    if insee not in dict_data.keys() :
        dict_data[insee] = {}
    if a2["type"] in ["work","education"] :
        if "work_or_edu_fac" not in dict_data[insee].keys() :
            dict_data[insee]["work_or_edu_fac"] = 1
        else : 
            dict_data[insee]["work_or_edu_fac"] += 1
    else : 
        if "other_fac" not in dict_data[insee].keys() :
            dict_data[insee]["other_fac"] = 1
        else : 
            dict_data[insee]["other_fac"] += 1 
keys.append("work_or_edu_fac")
keys.append("other_fac")

file_car = "python_files\\get_data\\Menages_semaine.csv"
df = pd.read_csv(file_car,sep=",")
insee_changes_dict = {77028:77433,77166:77316,77299:77316,77399:77504,77491:77316,78251:78551,78524:78158,91182:91228,91222:91390,95259:95040}
persons = {}
cars = {}
for i in df.iterrows() :
    insee = i[1].RESCOMM
    if insee in insee_changes_dict.keys():
        insee = insee_changes_dict[insee]
    nb_car = i[1].NB_VD
    nb_person = i[1].MNP
    if insee not in dict_data.keys() :
        dict_data[insee] = {}
    if insee not in persons.keys() :
        persons[insee] = nb_person
        cars[insee] = nb_car
    else : 
        persons[insee] += nb_person
        cars[insee] += nb_car
for insee in persons.keys():
    if persons[insee] != 0 :
        dict_data[insee]["cars_per_persons"] = cars[insee]/persons[insee]
    else :
        dict_data[insee]["cars_per_persons"] = "NA" 
keys.append("cars_per_persons")

file_links = "python_files\\split_network\\output_network_links.xml"
tree = ET.parse(file_links)
root = tree.getroot()
for child in root :
    a = child.attrib
    length = a["length"]
    id = a["id"]
    if len(child) != 0 :
        if len(child[0]) != [] :
            type = child[0][0].text
    insee = dict_links[id]
    if (type == "motorway") or (type == "motorway_link") or (type == "motorway_junction") or (type == "trunk") or (type == "trunk_link"):
        if insee not in dict_data.keys() :
            dict_data[insee] = {}
        if "big_road" not in dict_data[insee].keys():
            dict_data[insee]["big_road"] = float(length)
        else :
            dict_data[insee]["big_road"] += float(length)
keys.append("big_road")

lists = {}

for key in keys :
    lists[key] = []
lists["insee"] = []
for insee in dict_data.keys() :
    if insee != "outside" :
        lists["insee"].append(insee)
        for key in keys :
            if key in dict_data[insee].keys():
                lists[key].append(dict_data[insee][key])
            else : 
                lists[key].append(0)
df = pd.DataFrame.from_dict(lists)
df.to_csv("python_files\\get_data\\data_communes.csv",index=False,sep=";")

    

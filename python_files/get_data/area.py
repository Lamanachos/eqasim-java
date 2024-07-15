import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
import json

shapefile_communes = "python_files\\communes-dile-de-france-au-01-janvier\\communes-dile-de-france-au-01-janvier.shp"
gdf = gpd.read_file(shapefile_communes)
dict_data = {}
for i in gdf.iterrows():
    area = i[1].st_areasha
    insee = i[1].insee
    if insee not in dict_data.keys() :
        dict_data[insee] = {}
    dict_data[insee]["area"] = area/1000000

file_pop = "python_files\\get_data\\donnees-communales-sur-la-population-dile-de-france.csv"
df = pd.read_csv(file_pop,sep=";")
for i in df.iterrows() :
    pop = i[1].popmun2017
    insee = i[1].insee
    if insee not in dict_data.keys() :
        dict_data[insee] = {}
    dict_data[insee]["pop"] = pop
    dict_data[insee]["density"] = pop/dict_data[insee]["area"]

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
    if a2["type"] not in dict_data[insee].keys() :
        dict_data[insee][a2["type"]] = 1
    else : 
        dict_data[insee][a2["type"]] += 1
    
print(dict_data[75105])
""" file_car = "python_files\\get_data\\Menages_semaine.csv"
df = pd.read_csv(file_car,sep=",")
print(df)
for i in df.iterrows() :
    insee = i[1].RESCOMM
    nb_car = i[1].NB_VD """
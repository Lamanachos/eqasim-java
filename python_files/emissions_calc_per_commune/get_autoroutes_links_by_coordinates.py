import attributes as attrib
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from pyproj import Transformer
import json

route_path = attrib.origin_of_the_project + "python_files\\rrir_national_iledefrance_wgs84.csv"
gdf = gpd.read_file(route_path)
gdf = gdf["geo_shape"]
transformer = Transformer.from_crs("WGS84", "EPSG:2154")
liste_roads_coordinates = []
for i in gdf :
    l = json.loads(i)
    no_add = False
    temp = []
    for j in l["coordinates"] :
        if type(j) == list :
            no_add = True
        temp.append(transformer.transform(j[1],j[0]))
    if not no_add :
        liste_roads_coordinates.append(temp)
path_nodes = attrib.nodes_file
df_nodes = pd.read_xml(path_nodes)
dict_nodes = {}
for i in df_nodes.iterrows() :
    dict_nodes[i[1]["id"]] = [i[1]["x"],i[1]["y"]]

path_links = attrib.links_file
df_links = pd.read_xml(path_links)
x_froms = []
x_tos = []
y_froms = []
y_tos = []
for i in df_links.iterrows() :
    x_froms.append(dict_nodes[i[1]["from"]][0])
    y_froms.append(dict_nodes[i[1]["from"]][1])
    x_tos.append(dict_nodes[i[1]["to"]][0])
    y_tos.append(dict_nodes[i[1]["to"]][1])
df_links.insert(10,"x_from",x_froms,True)
df_links.insert(11,"y_from",y_froms,True)
df_links.insert(12,"x_to",x_tos,True)
df_links.insert(13,"y_to",y_tos,True)

autoroute_links = []
for i in liste_roads_coordinates :
    for j in range(len(i)-1):
        f = i[j]
        t = i[j+1]
        links = df_links[(df_links["x_from"] == f[0]) & (df_links["x_from"] == f[1]) & (df_links["x_from"] == t[0]) & (df_links["x_from"] == t[1])]
        for link in links.iterrows() :
            autoroute_links.append(link[1]["id"])
print(autoroute_links)
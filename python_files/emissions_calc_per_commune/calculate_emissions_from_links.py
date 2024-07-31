import json
import pandas as pd
import geopandas as gpd
import xml.etree.ElementTree as ET
import time as t
from shapely.geometry import Point
import multiprocessing as mp
import os
import attributes as attrib
from math import floor
import gzip

true_start = t.time()
#Get links commune and links len
with open(attrib.links_commune_file) as json_file:
    links_commune = json.load(json_file)
with open(attrib.links_emissions_basecase_file) as json_file:
    co2_per_links = json.load(json_file)

results_dir = attrib.results_dir
if not os.path.exists(results_dir):
    os.makedirs(results_dir)
results_file = attrib.results_file
if attrib.clean :
    f = open(results_file, "w")
else :
    f = open(results_file,"a")
co2_all = 0
communes_co2 = {}
for i in links_commune.values():
    communes_co2[i] = 0

for link in co2_per_links.keys() :
    temp_co2 = float()
    link_commune = links_commune[link]
    if link_commune != None :
        communes_co2[link_commune] += temp_co2
    co2_all += temp_co2
    
print("Emissions calculated (from links) in",t.time()-true_start,"seconds")
file_c = attrib.communes_co2_file
communes_co2["IDF"] = co2_all
with open(file_c, "w") as outfile: 
    json.dump(communes_co2, outfile)


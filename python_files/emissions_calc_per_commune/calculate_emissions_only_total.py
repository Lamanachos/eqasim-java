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

def init_pEvents(dict_links_commune):
    global links_commune
    links_commune = dict_links_commune

def treat_file(file):
    #Setup variables
    idf_co2 = 0
    communes_co2 = {}
    for i in links_commune.values():
        communes_co2[i] = 0
    #Parsing file
    start = t.time()
    #print(f"Parsing {file}...")
    unzip_file = gzip.open(file)
    tree = ET.parse(unzip_file)
    #print("Parsing of ",file," done in ",t.time()-start," seconds")
    root = tree.getroot()
    start = t.time()
    #print(f"Calculating emissions...")
    for child in root :
        dict_c = child.attrib
        temp_co2 = float(dict_c["CO2_TOTAL"])
        link_id = dict_c["linkId"]
        link_commune = links_commune[link_id]
        if link_commune != None :
            communes_co2[link_commune] += temp_co2
        idf_co2 += temp_co2
    print("Emissions for",file,"calculated in",t.time()-start,"seconds")
    #Return
    return [idf_co2,communes_co2]

if __name__ == "__main__" : 
    true_start = t.time()
   
    #Get links commune and links len
    with open(attrib.links_commune_file) as json_file:
        links_commune = json.load(json_file)

    #Multiprocessing
    p = mp.Pool(min(10,mp.cpu_count()),initializer=init_pEvents, initargs=(links_commune,))
    emissions_folder = attrib.emissions_folder
    t_files = os.listdir(emissions_folder)
    files = []
    for i in t_files:
        files.append(emissions_folder + "\\" + i)
    try:
        liste_co2 = p.map(treat_file, files)
    finally:
        p.close()
        p.join()
    results_dir = attrib.results_dir
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    
    co2_all = 0
    communes_co2 = {}
    for i in links_commune.values():
        communes_co2[i] = 0

    for i in liste_co2 :
        #get total co2
        co2_all += float(i[0])
        for commune in i[1].keys() :
            communes_co2[commune] += float(i[1][commune])

    file_c = attrib.communes_co2_file
    communes_co2["IDF"] = co2_all
    with open(file_c, "w") as outfile: 
        json.dump(communes_co2, outfile)
    file_c = attrib.communes_hdist_file

    print("Emissions calculated in",t.time()-true_start,"seconds")
    
    """ if not attrib.basecase :
        list_dir = os.listdir(emissions_folder)
        for file in list_dir :
            os.remove(emissions_folder + "\\" + file)
        os.rmdir(emissions_folder) """


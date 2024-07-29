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

def treat_file(file):
    #Setup variables
    links_co2 = {}
    #Parsing file
    unzip_file = gzip.open(file)
    tree = ET.parse(unzip_file)
    root = tree.getroot()
    start = t.time()
    #Calculating emissions
    for child in root :
        dict_c = child.attrib
        temp_co2 = float(dict_c["CO2_TOTAL"])
        link_id = dict_c["linkId"]
        if link_id not in links_co2.keys():
            links_co2[link_id] = temp_co2
        else :
            links_co2[link_id] += temp_co2
    print("Emissions for",file,"calculated in",t.time()-start,"seconds")
    #Return
    return links_co2

if __name__ == "__main__" : 
    true_start = t.time()

    #Multiprocessing
    p = mp.Pool(14) #(mp.cpu_count())
    #emissions_folder = attrib.emissions_folder
    emissions_folder = attrib.origin_of_the_project + "python_files\\emissions_calc_per_commune\\emissions\\basecase_split"
    t_files = os.listdir(emissions_folder)
    files = []
    for i in t_files:
        files.append(emissions_folder + "\\" + i)
    try:
        liste_links_co2 = p.map(treat_file, files)
    finally:
        p.close()
        p.join()
    #results_dir = attrib.results_dir
    results_dir = attrib.origin_of_the_project + "python_files\\emissions_calc_per_commune\\emissions\\bc_emissions_per_link"
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    #results_file = attrib.results_file
    results_file = attrib.origin_of_the_project + "python_files\\emissions_calc_per_commune\\emissions\\bc_emissions_per_link\\bc_emissions_per_link.json"
    if attrib.clean :
        f = open(results_file, "w")
    else :
        f = open(results_file,"a")
    
    aggreg_links_co2 = {}
    for i in liste_links_co2 :
        for key in i.keys():
            if key not in aggreg_links_co2.keys():
                aggreg_links_co2[key] = i[key]
            else :
                aggreg_links_co2[key] += i[key]
    with open(results_file, "w") as outfile: 
        json.dump(aggreg_links_co2, outfile)
        
    # if not attrib.basecase :
    #     list_dir = os.listdir(emissions_folder)
    #     for file in list_dir :
    #         os.remove(emissions_folder + "\\" + file)
    #     os.rmdir(emissions_folder)




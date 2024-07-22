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

def init_pEvents(dict_links_commune,dict_len_links,list_communes_in_paris):
    global links_commune
    links_commune = dict_links_commune
    global links_len
    links_len = dict_len_links
    global communes_in_paris
    communes_in_paris = list_communes_in_paris

def treat_file(file):
    #Setup variables
    paris_co2 = 0
    idf_co2 = 0
    nb_bins_dist = attrib.nb_bins_dist
    nb_bins_heure = attrib.nb_bins_heure
    paris_hist_dist = [0 for i in range(nb_bins_dist)]
    paris_hist_heure = [0 for i in range(nb_bins_heure)]
    idf_hist_dist = [0 for i in range(nb_bins_dist)]
    idf_hist_heure = [0 for i in range(nb_bins_heure)]
    communes_hist_dist = {}
    communes_hist_heure = {}
    communes_co2 = {}
    for i in links_commune.values():
        communes_co2[i] = 0
        communes_hist_dist[i] = [0 for i in range(nb_bins_dist)]
        communes_hist_heure[i] = [0 for i in range(nb_bins_heure)]
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
        bin_heure = int(float(dict_c["time"]))//attrib.size_heure
        if bin_heure >= attrib.nb_bins_heure :
            bin_heure = attrib.nb_bins_heure - 1
        bin_dist = floor(float(links_len[link_id]))//attrib.size_dist
        if bin_dist >= attrib.nb_bins_dist :
            bin_dist = attrib.nb_bins_dist - 1
        link_commune = links_commune[link_id]
        if link_commune in communes_in_paris  :
            paris_co2 += temp_co2
            paris_hist_heure[bin_heure] += temp_co2
            paris_hist_dist[bin_dist] += temp_co2
        if link_commune != None :
            communes_co2[link_commune] += temp_co2
            communes_hist_heure[link_commune][bin_heure] += temp_co2
            communes_hist_dist[link_commune][bin_dist] += temp_co2
        idf_co2 += temp_co2
        idf_hist_heure[bin_heure] += temp_co2
        idf_hist_dist[bin_dist] += temp_co2
    print("Emissions for",file,"calculated in",t.time()-start,"seconds")
    #Return
    return [idf_co2,paris_co2,communes_co2],[idf_hist_dist,idf_hist_heure],[paris_hist_dist,paris_hist_heure],[communes_hist_dist,communes_hist_heure]

if __name__ == "__main__" : 
    true_start = t.time()
   
    #Get links commune and links len
    with open(attrib.links_commune_file) as json_file:
        links_commune = json.load(json_file)
    with open(attrib.links_len_file) as json_file:
        links_len = json.load(json_file)

    #Multiprocessing
    p = mp.Pool(mp.cpu_count(),initializer=init_pEvents, initargs=(links_commune,links_len,attrib.liste_communes_in_paris,))
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
    results_file = attrib.results_file
    if attrib.clean :
        f = open(results_file, "w")
    else :
        f = open(results_file,"a")
    co2_inside = 0
    co2_all = 0
    nb_bins_dist = attrib.nb_bins_dist
    nb_bins_heure = attrib.nb_bins_heure
    paris_hist_dist = [0 for i in range(nb_bins_dist)]
    paris_hist_heure = [0 for i in range(nb_bins_heure)]
    idf_hist_dist = [0 for i in range(nb_bins_dist)]
    idf_hist_heure = [0 for i in range(nb_bins_heure)]

    communes_hist_dist = {}
    communes_hist_heure = {}
    communes_co2 = {}
    for i in links_commune.values():
        communes_co2[i] = 0
        communes_hist_dist[i] = [0 for i in range(nb_bins_dist)]
        communes_hist_heure[i] = [0 for i in range(nb_bins_heure)]

    for i in liste_co2 :
        #get total co2
        co2_all += float(i[0][0])
        co2_inside += float(i[0][1])
        for commune in i[0][2].keys() :
            communes_co2[commune] += float(i[0][2][commune])
            for j in range(len(i[1][0])):
                communes_hist_dist[commune][j] += i[3][0][commune][j]
            for k in range(len(i[1][1])):
                communes_hist_heure[commune][k] += i[3][1][commune][k]
        for j in range(len(i[1][0])):
            idf_hist_dist[j] += i[1][0][j]
            paris_hist_dist[j] += i[2][0][j]
        for k in range(len(i[1][1])):
            idf_hist_heure[k] += i[1][1][k]
            paris_hist_heure[k] += i[2][1][k]
    f.write("Folder :\n"+emissions_folder+"\n")
    f.write("All :\n"+str(co2_all)+"\n")
    f.write("Inside :\n"+str(co2_inside)+"\n")
    f.write("All dist :\n"+str(idf_hist_dist)+"\n")
    f.write("Inside dist :\n"+str(paris_hist_dist)+"\n")
    f.write("All heure :\n"+str(idf_hist_heure)+"\n")
    f.write("Inside heure :\n"+str(paris_hist_heure)+"\n")
    f.write("Total time :\n"+str(t.time()-true_start)+"\n")
    file_c = attrib.communes_co2_file
    communes_co2["IDF"] = co2_all
    with open(file_c, "w") as outfile: 
        json.dump(communes_co2, outfile)
    file_c = attrib.communes_hdist_file
    communes_hist_dist["IDF"] = idf_hist_dist
    with open(file_c, "w") as outfile: 
        json.dump(communes_hist_dist, outfile)
    file_c = attrib.communes_hheure_file
    communes_hist_heure["IDF"] = idf_hist_heure
    with open(file_c, "w") as outfile: 
        json.dump(communes_hist_heure, outfile)
    f.close()
    if not attrib.basecase :
        list_dir = os.listdir(emissions_folder)
        for file in list_dir :
            os.remove(emissions_folder + "\\" + file)
        os.rmdir(emissions_folder)


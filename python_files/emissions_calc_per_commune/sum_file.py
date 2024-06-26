import pandas as pd
import geopandas as gpd
import xml.etree.ElementTree as ET
import time as t
import gzip
from shapely.geometry import Point, Polygon
from multiprocessing import Pool
import multiprocessing as mp
import os

idf_results_file = "emissions_results\\idf_split_sums.txt"
emissions_folder = "emissions\\idf_1pct_split"

def init(lock1,co2):
    global irf_lock
    irf_lock = lock1
    global tot_co2
    tot_co2 = co2

def treat_file(file):
    start = t.time()
    #Get the db
    events_db = pd.read_xml(emissions_folder + "\\" + str(file))
    #print("Parsing of",file,"done in",t.time()-start,"seconds")
    start = t.time()
    #get the emissions
    idf_co2 = events_db["CO2_TOTAL"].sum()
    #write the emissions
    irf_lock.acquire()
    irf = open(idf_results_file,"a")
    tot_co2.value += idf_co2
    irf.write(file + " : " + str(idf_co2) + "\n")
    irf.write( "Tot : " + str(tot_co2.value) + "\n")
    irf.close()
    irf_lock.release()
    #print("Emissions for",file,"calculated in",t.time()-start,"seconds")
    

if __name__ == '__main__':
    
    true_start = t.time()

    #Setting up results files
    clean = True
    if clean :
        open(idf_results_file, "w").close()

    #Doing the job
    co2 =  mp.Value('d', 0)
    #Multiprocessing
    lock1 = mp.Lock()
    p = mp.Pool(mp.cpu_count(),initializer=init, initargs=(lock1,co2,))
    files = os.listdir(emissions_folder)
    """ temp_files = os.listdir(emissions_folder)
    files = []
    for i in temp_files :
        files.append(emissions_folder+"\\"+i) """
    try:
        p.map(treat_file, files)
    finally:
        p.close()
        p.join()
    print("Total time : ",t.time()-true_start)

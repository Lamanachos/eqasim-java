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

def init_pNodes(spd):
    global shapedict
    shapedict = spd

def init_pLinks(dict_nodes, spd):
    global nodes_commune
    nodes_commune = dict_nodes
    global shapedict
    shapedict = spd


def link_in_which_commune(t_link):
    link = t_link[1]
    node_from = link["from"]
    node_to = link["to"]
    commune_from = nodes_commune[node_from][0]
    commune_to = nodes_commune[node_to][0]
    communes = list(shapedict.keys())
    commune_of_link = commune_from
    if commune_from != commune_to :
        if commune_from == None :
            commune_of_link = commune_to
        elif commune_to == None :
            commune_of_link = commune_from
        elif attrib.precise_links :
            pos_from = nodes_commune[node_from][1]
            pos_to = nodes_commune[node_to][1]
            pos_center = [(pos_from[0]+pos_to[0])/2,(pos_from[1]+pos_to[1])/2]
            i = 0
            while (i < len(communes)) and (commune_of_link == None):
                if Point(pos_center[0],pos_center[1]).within(shapedict[communes[i]]):
                    commune_of_link = communes[i]
    if commune_of_link == None :
        commune_of_link = "outside"
    return [link["id"],commune_of_link,link["length"]]

def node_get_c(t_node):
    node = t_node[1]
    communes = list(shapedict.keys())
    commune_of_node = None
    i = 0
    point = Point(node["x"],node["y"])
    while (i < len(communes)) and (commune_of_node == None):
        if point.within(shapedict[communes[i]]):
            commune_of_node = communes[i]
        i += 1
    return [node["id"],[commune_of_node,[node["x"],node["y"]]]]
    
if __name__ == "__main__" : 
    true_start = t.time()
    #Getting networks dbs
    print("Putting the network in databases...")
    links_file = attrib.links_file 
    links_db = pd.read_xml(links_file)
    links_db = links_db[["id","from","to","length"]]
    nodes_file = attrib.nodes_file 
    nodes_db = pd.read_xml(nodes_file)
    nodes_db = nodes_db[["id","x","y"]]
    print("Done in ",t.time()-true_start," seconds")

    #Getting communes shape dict
    if attrib.just_drz :    
        shapefile_communes = attrib.shapefile_communes_for_links
    else :
        shapefile_communes = attrib.shapefile_communes
    shape_communes = gpd.read_file(shapefile_communes)
    shape = shape_communes.to_crs(epsg=2154)
    if attrib.just_drz :
        shapedict = dict(zip(shape.buffer_km, shape.geometry))
    else : 
        shapedict = dict(zip(shape.insee, shape.geometry))

    #Getting position of each node
    start = t.time()
    print("Getting position of each node...")
    inputs = nodes_db.iterrows()
    count = 0
    pNodes = mp.Pool(mp.cpu_count(),initializer=init_pNodes, initargs=(shapedict,))
    try:
        liste_nodes_c = pNodes.map(node_get_c, inputs)
    finally:
        pNodes.close()
        pNodes.join()
    nodes_c = {}
    for i in liste_nodes_c :
        nodes_c[i[0]]=i[1]
    print("Number of nodes :",len(nodes_c.keys()))
    print("Done in ",t.time()-start," seconds")
    file_nc = attrib.nodes_commune_file
    with open(file_nc, "w") as outfile: 
        json.dump(nodes_c, outfile)
    #Getting in what commune is each link
    start = t.time()
    print("Getting in what commune is each link...")
    inputs = links_db.iterrows()
    count = 0
    pLinks = mp.Pool(mp.cpu_count(),initializer=init_pLinks, initargs=(nodes_c, shapedict,))
    try:
        liste_inout = pLinks.map(link_in_which_commune, inputs)
    finally:
        pLinks.close()
        pLinks.join()
    links_commune = {}
    links_len = {}
    for i in liste_inout :
        links_commune[i[0]]=i[1]
        links_len[i[0]]=i[2]
    print("Number of links :",len(links_commune.keys()))
    print("Done in ",t.time()-start," seconds")

    folder_c = attrib.links_commune_folder
    if not os.path.exists(folder_c):
        os.makedirs(folder_c)
    file_c = attrib.links_commune_file
    with open(file_c, "w") as outfile: 
        json.dump(links_commune, outfile)
    file_l = attrib.links_len_file
    with open(file_l, "w") as outfile: 
        json.dump(links_len, outfile)
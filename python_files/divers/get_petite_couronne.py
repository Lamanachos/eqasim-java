import geopandas as gpd
import pandas as pd
import sys
import os

shapefile_communes = "python_files\\communes-dile-de-france-au-01-janvier\\communes-dile-de-france-au-01-janvier.shp"
dest_folder = "python_files\\petite_couronne\\"

def get_in_zone(zone,dest):
    dest = dest_folder + dest
    if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)
    shape_communes = gpd.read_file(shapefile_communes)
    liste_communes = []
    for i in shape_communes["insee"] :
        if str(i)[:2] not in zone:
            liste_communes.append(i)
    liste_shapes = []
    for i in liste_communes:
        ind = shape_communes[(shape_communes["insee"] == i)].index
        shape_communes.drop(ind, inplace = True)
    shape_communes.to_file(dest)

get_in_zone(["92","93","94","75"],"petite_couronne.shp")
get_in_zone(["92"],"92.shp")
get_in_zone(["93"],"93.shp")
get_in_zone(["94"],"94.shp")
get_in_zone(["75"],"75.shp")

    
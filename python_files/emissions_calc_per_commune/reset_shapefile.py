import geopandas as gpd
import os 
import attributes as attrib

shapefile_communes = attrib.origin_of_the_project + "python_files\\communes-dile-de-france-au-01-janvier\\communes-dile-de-france-au-01-janvier.shp"
shapefile_fusions = attrib.origin_of_the_project + "python_files\\communes-dile-de-france-au-01-janvier\\communes-dile-de-france-au-01-janvier-with-fusions.shp"
all_insee_files = attrib.origin_of_the_project + "python_files\\communes-dile-de-france-au-01-janvier\\existing-insees.txt"
gis_folder = attrib.origin_of_the_project + "gis"

f = open(all_insee_files,"w")
f.close()
gdf = gpd.read_file(shapefile_communes)
gdf.to_file(shapefile_fusions)
list_dir = os.listdir(gis_folder)
for directory in list_dir :
    if os.path.isdir(gis_folder + "\\" + directory):
        for i in os.listdir(gis_folder + "\\" + directory):
            os.remove(gis_folder + "\\" + directory + "\\" + i)
        os.rmdir(gis_folder + "\\" + directory)

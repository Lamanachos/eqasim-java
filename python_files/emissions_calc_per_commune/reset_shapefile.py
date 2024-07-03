import geopandas as gpd
import os 

shapefile_communes = "python_files\\communes-dile-de-france-au-01-janvier\\communes-dile-de-france-au-01-janvier.shp"
shapefile_fusions = "python_files\\communes-dile-de-france-au-01-janvier\\communes-dile-de-france-au-01-janvier-with-fusions.shp"
all_insee_files = "python_files\\communes-dile-de-france-au-01-janvier\\existing-insees.txt"
gis_folder = "gis"

f = open(all_insee_files,"w")
f.close()
gdf = gpd.read_file(shapefile_communes)
gdf.to_file(shapefile_fusions)
list_dir = os.listdir(gis_folder)
for directory in list_dir :
    if os.path.isdir(directory):
        for i in os.listdir(directory):
            os.remove(i)
        os.rmdir(directory)

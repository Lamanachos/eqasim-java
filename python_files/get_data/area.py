import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

shapefile_communes = "python_files\\communes-dile-de-france-au-01-janvier\\communes-dile-de-france-au-01-janvier.shp"
gdf = gpd.read_file(shapefile_communes)
dict_data = {}
for i in gdf.iterrows():
    area = i[1].st_areasha
    insee = i[1].insee
    if insee not in dict_data.keys() :
        dict_data[insee] = {}
    dict_data[insee]["area"] = area
file_pop = "python_files\\get_data\donnees-communales-sur-la-population-dile-de-france.csv"


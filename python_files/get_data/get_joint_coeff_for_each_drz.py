import geopandas as gpd
import json

drz_composition_path = "python_files\\communes-dile-de-france-au-01-janvier\\existing-insees.txt"
gis_path = "C:\\Users\\ulysse.marcandella\\Desktop\\eqasim-java-pr\\gis"
f = open(drz_composition_path)
lines = f.readlines()
f.close()
dict_drz = {}
for i in range(0,len(lines),2):
    insee = lines[i][:-1]
    gdf = gpd.read_file(gis_path+f"\\{insee}\\{insee}.shp")
    gdf = gdf["geometry"]
    conv_pol = gdf.convex_hull
    coeff = (gdf.area/conv_pol.area).iloc[0]
    dict_drz[insee] = coeff
print(dict_drz)
file_l = "python_files\\get_data\\coeff_join.json"
with open(file_l, "w") as outfile: 
    json.dump(dict_drz, outfile)


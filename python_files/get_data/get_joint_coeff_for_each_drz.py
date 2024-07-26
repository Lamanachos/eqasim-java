import geopandas as gpd
import json

min_insee = 100001
max_insee = 100092
gis_path = "C:\\Users\\ulysse.marcandella\\Desktop\\eqasim-java-pr\\gis"
dict_drz = {}
for i in range(min_insee,max_insee):
    insee = i
    gdf = gpd.read_file(gis_path+f"\\{insee}\\{insee}.shp")
    gdf = gdf["geometry"]
    conv_pol = gdf.convex_hull
    coeff = (gdf.area/conv_pol.area).iloc[0]
    dict_drz[insee] = coeff
print(dict_drz)
file_l = "python_files\\get_data\\coeff_join.json"
with open(file_l, "w") as outfile: 
    json.dump(dict_drz, outfile)


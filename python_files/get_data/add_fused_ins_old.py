import os
import geopandas as gpd
import pandas as pd
insees_file = "python_files\\get_data\\DRZs_shp_G1.csv"
gis_folder = "gis_clean"
f = open(insees_file)
lines = f.readlines()
f.close()
dict_insees = {}
for i in lines[1:]:
    insee_list = i.split(",")
    insee = 100000 + int(insee_list[0].replace('"','')) 
    fused_ins = ""
    for j in range(1,len(insee_list)):
        temp = insee_list[j]
        temp = temp.replace('"','')
        temp = temp.replace('[','')
        temp = temp.replace(']','')
        temp = temp.replace("\n",'')
        fused_ins += " "+temp
    fused_ins = fused_ins[1:]
    dict_insees[insee] = fused_ins
list_dir = os.listdir(gis_folder)
for insee in dict_insees.keys() :
    file = f"gis_clean\\{insee}\\{insee}.shp"
    gdf = gpd.read_file(file)
    df = pd.DataFrame()
    df["insee"] = gdf["insee"]
    df["geometry"] = gdf["geometry"]
    df["fused_ins"] = [dict_insees[insee]]
    gdf2 = gpd.GeoDataFrame(df)
    print(gdf2)
    dest = f"{gis_folder}\\{insee}"
    gdf2.to_file(dest)


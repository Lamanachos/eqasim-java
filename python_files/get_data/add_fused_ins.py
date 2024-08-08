import os
import shutil
import geopandas as gpd
import pandas as pd
import reset_shapefile
reset_shapefile.main()
insees_file = "python_files\\get_data\\DRZs_shp_G1_G3.csv"
g1_folder = "gis_G1"
g3_folder = "gis_G3"
gis_folder = "gis_clean"
f = open(insees_file)
lines = f.readlines()
f.close()
dict_insees = {}
for i in lines[1:]:
    insee_list = i.split(";")
    g1_or_g3 = g3_folder
    insee = 100000 + int(insee_list[1]) 
    print(insee)
    if insee_list[2] == "G1":
        temp = insee_list[4]
        temp = temp.replace(',',' ')
        temp = temp.replace('[','')
        temp = temp.replace(']','')
        temp = temp.replace("\n",'')
        dict_insees[insee] = temp
        g1_or_g3 = g1_folder
    else :
        gdf = gpd.read_file(f"{g3_folder}\\{insee}\\{insee}.shp")
        dict_insees[insee] = gdf["fused_ins"][0] 
    source_dir = f"{g1_or_g3}\\{insee}"
    list_dir = os.listdir(source_dir)
    dest_dir = f"{gis_folder}\\{insee}"
    os.mkdir(dest_dir)
    for file in list_dir :
        source = source_dir + "\\" + file
        if os.path.isfile(source):
            shutil.copy(source, dest_dir)
    source_dir = f"{g1_or_g3}\\{insee}_buffered"
    list_dir = os.listdir(source_dir)
    dest_dir = f"{gis_folder}\\{insee}_buffered"
    os.mkdir(dest_dir)
    for file in list_dir :
        source = source_dir + "\\" + file
        if os.path.isfile(source):
            shutil.copy(source, dest_dir)

for insee in dict_insees.keys() :
    file = f"gis_clean\\{insee}\\{insee}.shp"
    gdf = gpd.read_file(file)
    df = pd.DataFrame()
    df["insee"] = gdf["insee"]
    df["geometry"] = gdf["geometry"]
    dict_fused_ins = {}
    temp = dict_insees[insee]
    if temp == "" :
        print(insee)
        exit()
    count = 0
    while len(temp) > 252 :
        dict_fused_ins["fi"+str(count)] = temp[:252]
        temp = temp[252:]
        count += 1
    dict_fused_ins["fi"+str(count)] = temp
    for key in dict_fused_ins.keys() :
        df[key] = [dict_fused_ins[key]]
    gdf2 = gpd.GeoDataFrame(df)
    print(gdf2)
    dest = f"{gis_folder}\\{insee}"
    gdf2.to_file(dest)
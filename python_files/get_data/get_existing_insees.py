import os
import geopandas as gpd

def main():
    gis_folder = "gis"
    list_dir = os.listdir(gis_folder)
    list_existing_insees = []
    for i in list_dir :
        if os.path.isdir(gis_folder + "\\" + i):
            if len(i) == 6 :
                list_existing_insees.append(int(i))
    dest_file = "python_files\\get_data\\existing_insees.txt"
    f = open(dest_file,"w")
    for i in list_existing_insees :
        f.write(str(i)+"\n")
        gdf = gpd.read_file(f"{gis_folder}\\{i}\\{i}.shp")
        f.write(gdf["fused_ins"][0]+"\n")
    f.close()

if __name__ == "__main__" :
    main()
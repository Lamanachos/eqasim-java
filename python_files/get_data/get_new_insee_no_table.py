
import geopandas as gpd
import pandas as pd
import get_buffer
import os

#args : insee codes of municipalities you want to fuse separated by spaces, the last one being the new insee, ex : 75105 93048 100001
def main(argv):
    print(argv)
    shapefile_paris = "gis\\paris.shp"
    shapefile_paris = gpd.read_file(shapefile_paris)
    shapefile_communes = "python_files\\communes-dile-de-france-au-01-janvier\\communes-dile-de-france-au-01-janvier-with-fusions.shp"
    dest_folder = "gis"
    shape_communes = gpd.read_file(shapefile_communes)
    liste_communes = []
    for com in argv :
        liste_communes.append(int(com))
    list_dir = os.listdir(dest_folder)
    list_existing_insee = []
    for i in list_dir :
        if os.path.isdir(dest_folder + "\\" + i):
            if len(i) == 6 :
                list_existing_insee.append(int(i))
    if list_existing_insee == [] :
        new_insee = "100001"
    else :
        new_insee = str(max(list_existing_insee)+1)
    liste_shapes = []
    for i in liste_communes:
        shape = shape_communes[(shape_communes["insee"] == int(i))]
        liste_shapes.append(shape)
    union_shape = liste_shapes[0]
    if len(liste_shapes) == 1 :
        union_shape = union_shape["geometry"]
    for i in range(1,len(liste_shapes)):
        union_shape = union_shape.union(liste_shapes[i],align=False)
    union_shape = union_shape.to_crs(shapefile_paris.crs)
    all_insee= ""
    for i in liste_communes :
        all_insee += " "+str(i)
    all_insee = all_insee[1:]
    df = pd.DataFrame()
    df["insee"] = [new_insee]
    df["geometry"] = [union_shape[union_shape.index[0]]]
    fused_communes = ""
    for i in liste_communes :
        fused_communes += str(i) + " "
    fused_communes = fused_communes[:-1]
    df["fused_ins"] = [fused_communes]
    gdf = gpd.GeoDataFrame(df,crs = shapefile_paris.crs)
    dest = f"{dest_folder}\\{new_insee}"
    gdf.to_file(dest)
    print("new_insee :",new_insee)
    get_buffer.main([str(new_insee)])
    
if __name__ == "__main__":
   #main(sys.argv[1:])
    main(["75105","75106"])
import attributes as attrib
import geopandas as gpd
import pandas as pd
import convert_espg
import sys

#args : insee codes of municipalities you want to fuse separated by spaces, ex : 75105 93048
def main(argv):
    print(argv)
    shapefile_communes = "python_files\\communes-dile-de-france-au-01-janvier\\communes-dile-de-france-au-01-janvier.shp"
    dest = "python_files\\communes-dile-de-france-au-01-janvier\\communes-dile-de-france-au-01-janvier-with-fusions.shp"
    shape_communes = gpd.read_file(shapefile_communes)
    liste_communes = []
    for com in argv :
        liste_communes.append(int(com))
    liste_shapes = []
    for i in liste_communes:
        shape = shape_communes[(shape_communes["insee"] == i)]
        liste_shapes.append(shape)
    union_shape = liste_shapes[0]
    for i in range(1,len(liste_shapes)):
        union_shape = union_shape.union(liste_shapes[i],align=False)
    new_insee= ""
    for i in liste_communes :
        new_insee += str(i)
    new_insee = int(new_insee)
    df = pd.DataFrame()
    keys = shape_communes.keys().tolist()
    for i in range(len(keys)):
        key = keys[i]
        temp = shape_communes[key].tolist()
        if key == "insee":
            temp.append(new_insee)
        elif key == "objectid" :
            temp.append(max(temp)+1)
        elif key == "geometry" :
            temp.append(union_shape[union_shape.index[0]])
        else :
            temp.append(None)
        df[key] = temp
    gdf = gpd.GeoDataFrame(df,crs = shape_communes.crs)
    gdf.to_file(dest)
    convert_espg.main([str(new_insee)])
    
if __name__ == "__main__":
   main(sys.argv[1:])
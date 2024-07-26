import geopandas as gpd
import pandas as pd
import sys

def main(argv):
    shapefile_communes = "python_files\\communes-dile-de-france-au-01-janvier\\communes-dile-de-france-au-01-janvier-with-fusions.shp"
    shapefile_paris = "gis\\paris.shp"
    shape_communes = gpd.read_file(shapefile_communes)
    shapefile_paris = gpd.read_file(shapefile_paris)
    liste_communes = []
    for com in argv :
        liste_communes.append(com)
    for i in liste_communes:
        a_shape = shape_communes[(shape_communes["insee"] == int(i))]
        shape = a_shape.to_crs(shapefile_paris.crs)
        shape.to_file("gis\\"+str(int(i)))
        insee = shape["insee"][shape.index[0]]
        df = pd.DataFrame()
        df["insee"] = [insee,insee,insee]
        df["buffer_km"] = ["0km","10km","20km"]
        temp_shape = shape.to_crs("EPSG:32634")
        temp_shape = temp_shape["geometry"]
        ten_k = temp_shape.buffer(10000)
        twenty_k = temp_shape.buffer(20000)
        temp_shape = temp_shape.to_crs(shapefile_paris.crs)
        ten_k = ten_k.to_crs(shapefile_paris.crs)
        twenty_k = twenty_k.to_crs(shapefile_paris.crs)
        ten_k = ten_k.difference(temp_shape)
        twenty_k = twenty_k.difference(temp_shape)
        twenty_k = twenty_k.difference(ten_k)
        df["geometry"] = [temp_shape[temp_shape.index[0]],ten_k[ten_k.index[0]],twenty_k[twenty_k.index[0]]]
        gdf = gpd.GeoDataFrame(df,crs = shapefile_paris.crs)
        gdf.to_file("gis\\"+str(int(i))+"_buffered")

if __name__ == "__main__":
   main(sys.argv[1:])
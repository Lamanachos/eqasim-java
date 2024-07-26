import geopandas as gpd
import pandas as pd
import sys

def main(argv):
    shape_folder = "gis"
    liste_communes = []
    shapefile_paris = "gis\\paris.shp"
    shapefile_paris = gpd.read_file(shapefile_paris)
    for com in argv :
        liste_communes.append(com)
    for i in liste_communes:
        shape_file = f"{shape_folder}\\{i}\\{i}.shp"
        shape = gpd.read_file(shape_file)
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

import geopandas as gpd
import pandas as pd
import sys


shapefile_communes = "..\\communes-dile-de-france-au-01-janvier\\communes-dile-de-france-au-01-janvier.shp"
dest = "..\\petite_couronne\\petite_couronne.shp"
shape_communes = gpd.read_file(shapefile_communes)
liste_communes = []
for i in shape_communes["insee"] :
    if str(i)[:2] in ["92","93","94","75"]:
        liste_communes.append(i)
print(len(liste_communes))
liste_shapes = []
for i in liste_communes:
    shape = shape_communes[(shape_communes["insee"] == i)]
    liste_shapes.append(shape)
df = pd.DataFrame
#TODO
print(df)
gdf = gpd.GeoDataFrame(df,crs = shape_communes.crs)
gdf.to_file(dest)
    
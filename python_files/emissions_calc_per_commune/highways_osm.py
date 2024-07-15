import attributes as attrib
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from pyproj import Transformer
import json

route_path = attrib.origin_of_the_project + "python_files\\highways\\highway.shp"
gdf = gpd.read_file(route_path)
gdf = gdf["osm_id"]
liste_ids = []
for i in gdf :
    liste_ids.append(i)
print(liste_ids)
path_links = attrib.links_file

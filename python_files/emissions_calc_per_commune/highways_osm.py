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
path_links = attrib.links_file
df_links = pd.read_xml(path_links)
df_links = df_links["id"]
existing_highway_links = []
for i in df_links:
    print(i)
    if i in liste_ids :
        existing_highway_links.append(i)
print(existing_highway_links)

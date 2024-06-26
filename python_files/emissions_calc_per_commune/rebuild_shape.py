import json
import attributes as attrib
import geopandas as gpd
import pandas as pd

compare = True
shapefile_communes = attrib.shapefile_communes
shape_communes = gpd.read_file(shapefile_communes)
shape = shape_communes.to_crs(epsg=2154)
with open(attrib.communes_co2_file) as json_file:
    communes_co2 = json.load(json_file)
if compare:
    with open(attrib.file_to_compare) as json_file:
        compare_co2 = json.load(json_file)
liste_co2 = []
temp = shape["insee"]
for i in temp:
    if compare :
        print((communes_co2[str(i)]-compare_co2[str(i)])/max(compare_co2[str(i)],1))
        liste_co2.append((communes_co2[str(i)]-compare_co2[str(i)])/max(compare_co2[str(i)],1))
    else :    
        liste_co2.append(communes_co2[str(i)])
shape.insert(10, "Co2", liste_co2, True)
shape.to_file(attrib.new_shapefilename)

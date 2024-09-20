import geopandas as gpd
import json
import os
import attributes as attrib

#dossier contenant les tracés des DRZ
gis_folder = "C:\\Users\\ulysse.marcandella\\Desktop\\eqasim-java-pr\\gis_clean"
#pour calculer les aires, il y a besoin de convertir les tracés des drz en ploygones, et ceux-ci sont stockés dans ce dossier
conv_pol_folder = "C:\\Users\\ulysse.marcandella\\Desktop\\eqasim-java-pr\\python_files\\get_data\\conv_pol"
dict_drz = {}
for i in os.listdir(gis_folder):
    if os.path.isdir(gis_folder + "\\" + i) : 
        if len(i) == 6 :
            insee = i
            gdf = gpd.read_file(gis_folder+f"\\{insee}\\{insee}.shp")
            gdf = gdf["geometry"]
            conv_pol = gdf.convex_hull
            conv_pol.to_file(conv_pol_folder+"\\"+str(i))
            coeff = (gdf.area/conv_pol.area).iloc[0]
            dict_drz[insee] = coeff
print(dict_drz)
file_l = attrib.file_coeff
with open(file_l, "w") as outfile: 
    json.dump(dict_drz, outfile)


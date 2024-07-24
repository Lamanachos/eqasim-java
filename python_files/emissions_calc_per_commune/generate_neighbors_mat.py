import geopandas as gpd
import random as r
import new_insee
import json
import time as t

start = t.time()
folder_p = "python_files\\petite_couronne\\"
petite_couronne = folder_p + "petite_couronne.shp"
network_file = "python_files\\output_5pc\\output_file.shp"
network_shape = gpd.read_file(network_file)
print("Open in :",t.time()-start)
shape_communes = gpd.read_file(petite_couronne)
shape_communes = shape_communes.to_crs("EPSG:2154")
liste_communes = []
for i in shape_communes["insee"] :
    liste_communes.append(i)
liste_shapes = []
for i in shape_communes["geometry"]:
    liste_shapes.append(i)
mat = {}
for i in liste_communes :
    mat[i] = []
    
for i in range(len(liste_communes)) :
    for j in range(i+1,len(liste_communes)) :
        if liste_shapes[i].touches(liste_shapes[j]) :
            a = (liste_shapes[i].intersection(liste_shapes[j])).intersection(network_shape["geometry"])
            empty = True
            k = 0
            while empty and (k < len(a)):
                if not a[k].is_empty :
                    empty = False
                    print(liste_communes[i],"is connected to",liste_communes[j])
                    mat[liste_communes[i]].append(liste_communes[j])
                    mat[liste_communes[j]].append(liste_communes[i])
                k += 1
                
print("Neighbors in :",t.time()-start)
file_l = "C:\\Users\\ulysse.marcandella\\Desktop\\eqasim-java-pr\\python_files\\emissions_calc_per_commune\\links_commune\\mat.json"
with open(file_l, "w") as outfile: 
    json.dump(mat, outfile)
print("Total time taken :",t.time()-start)
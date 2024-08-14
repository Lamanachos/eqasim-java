import geopandas as gpd
import random as r
import json
import time as t

mat_file = "C:\\Users\\ulysse.marcandella\\Desktop\\eqasim-java-pr\\python_files\\emissions_calc_per_commune\\links_commune\\mat.json"
with open(mat_file) as json_file:
    mat = json.load(json_file)
communes_idf_file = "python_files\\communes-dile-de-france-au-01-janvier\\communes-dile-de-france-au-01-janvier.shp"

start = t.time()
network_file = "python_files\\output_5pc\\output_file.shp"
network_shape = gpd.read_file(network_file)
print("Open in :",t.time()-start)
shape_communes = gpd.read_file(communes_idf_file)
shape_communes = shape_communes.to_crs("EPSG:2154")

liste_communes_outside = []
liste_shapes_outside = []
liste_shapes_petite_couronne = []
liste_communes_petite_couronne = []
for i in shape_communes.iterrows():
    insee = str(i[1]["insee"])
    if insee not in mat.keys() :
        liste_communes_outside.append(insee)
        liste_shapes_outside.append(i[1]["geometry"])
    else : 
        liste_communes_petite_couronne.append(insee)
        liste_shapes_petite_couronne.append(i[1]["geometry"])
new_mat = {}
for i in liste_communes_petite_couronne :
    temp = []
    for j in mat[i]:
        temp.append(j)
    new_mat[i] = temp

for i in range(len(liste_communes_petite_couronne)) :
    for j in range(len(liste_communes_outside)) :
        if liste_shapes_petite_couronne[i].touches(liste_shapes_outside[j]) :
            a = (liste_shapes_petite_couronne[i].intersection(liste_shapes_outside[j])).intersection(network_shape["geometry"])
            empty = True
            k = 0
            ci = liste_communes_petite_couronne[i]
            cj = liste_communes_outside[j]
            while empty and (k < len(a)):
                if not a[k].is_empty :
                    empty = False
                    print(ci,"is connected to",cj)
                    new_mat[ci].append(cj)
                    if cj not in new_mat.keys():
                        new_mat[cj] = []
                    new_mat[cj].append(ci)
                k += 1

print("Neighbors in :",t.time()-start)
file_l = "C:\\Users\\ulysse.marcandella\\Desktop\\eqasim-java-pr\\python_files\\emissions_calc_per_commune\\links_commune\\mat_extended.json"
with open(file_l, "w") as outfile: 
    json.dump(mat, outfile)
print("Total time taken :",t.time()-start)
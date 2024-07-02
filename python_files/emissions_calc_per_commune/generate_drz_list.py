import geopandas as gpd
import pandas as pd
import sys
import os
import random as r
import new_insee
import convert_espg

folder_p = "python_files\\petite_couronne\\"
petite_couronne = folder_p + "petite_couronne.shp"
shape_communes = gpd.read_file(petite_couronne)
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
    for j in range(len(liste_communes)) :
        if liste_shapes[i].touches(liste_shapes[j]) :
            mat[liste_communes[i]].append(liste_communes[j])

departements = ["92","93","94","75"]
dict_comms = {}
for i in departements :
    shape_comms = gpd.read_file(folder_p + i +".shp")
    liste_comms = []
    for j in shape_comms["insee"] :
        liste_comms.append(j)
    dict_comms[i] = liste_comms

def get_list_comms(number, departement, joint_or_not = True, max = False):
    number = int(number)
    liste_comms = []
    liste_dep = dict_comms[departement]
    if max :
        return liste_dep
    liste_comms.append(r.choice(liste_dep))
    for i in range(number-1):
        touching_comms = []
        for j in liste_comms :
            for k in mat[j]:
                if k in liste_dep :
                    if k not in liste_comms :
                        touching_comms.append(k)
        if joint_or_not :
            liste_comms.append(r.choice(touching_comms))
        else :
            not_touching_comms = []
            for l in liste_dep :
                if l not in touching_comms :
                    if l not in liste_comms :
                        not_touching_comms.append(l)
            if not_touching_comms != [] :
                liste_comms.append(r.choice(not_touching_comms))
            else : 
                liste_comms.append(r.choice(touching_comms))
    return liste_comms

def number_of_parts(drz):
    drz_copy = []
    for i in drz :
        drz_copy.append(i)
    pile = []
    checked = []
    current = []
    list_parts= []
    while (drz_copy != []) | (pile != []) :
        if pile == [] :
            if current != []:
                list_parts.append(current)
            current = []
            pile.append(drz_copy.pop(0))
        temp = pile.pop(0)
        """ print("temp :",temp)
        print("pile : ",pile)
        print("copy :",drz_copy)
        print("checked :",checked)
        print("current : ",current) """
        for i in drz :
            if i in drz_copy :
                if i in mat[temp] :
                    if i not in checked :
                        drz_copy.remove(i)
                        pile.append(i)
        checked.append(temp)
        current.append(temp)
    list_parts.append(current)
    return list_parts

def create_shapefiles(number_per_number,force_disjoint = False):
    for departement in departements :
        for i in range(len(number_per_number)) :
            for j in range(number_per_number[i]) :
                if i != 0 :
                    temp_j = get_list_comms(i+1,departement,True)
                    new_temp_j = []
                    for k in temp_j : 
                        new_temp_j.append(str(int(k)))
                    new_insee.main(new_temp_j)
                    temp_d = get_list_comms(i+1,departement,False)
                    if force_disjoint :
                        c = 0
                        while (len(number_of_parts(temp_d)) == 1) and (c<100):
                            temp_d = get_list_comms(i+1,departement,False)
                            c += 1
                    new_temp_d = []
                    for k in temp_d :
                        new_temp_d.append(str(int(k)))
                    new_insee.main(new_temp_d)
                else :
                    temp_j = get_list_comms(i+1,departement,True)
                    convert_espg.main(temp_j[0])
        temp_j = get_list_comms(0,departement,True,True)
        new_temp_j = []
        for j in temp_j : 
            new_temp_j.append(str(int(j)))
        new_insee.main(new_temp_j)


create_shapefiles([0,2,2,2,2,2,2,2,2,2],True)
                

            

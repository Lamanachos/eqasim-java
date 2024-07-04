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

frontiers = {}
for i in departements :
    frontiers[i] = {}
    for j in departements :
        if i != j :
            frontiers[i][j] = {}

for i in range(len(departements)) :
    for j in range(len(departements)) :
        if i != j :
            for k in dict_comms[departements[i]] :
                for l in dict_comms[departements[j]] :
                    if l in mat[k] :
                        if k not in frontiers[departements[i]][departements[j]].keys():
                            frontiers[departements[i]][departements[j]][k] = [l]
                        else :
                            frontiers[departements[i]][departements[j]][k].append(l)
print(frontiers)                 

def get_list_comms(number, liste_dep, joint_or_not = True, max = False, full_random = False, base_list = []):
    number = int(number)
    liste_comms = base_list
    if max :
        return liste_dep
    if full_random :
        return r.sample(liste_dep, number)
    if liste_comms == []:
        liste_comms.append(r.choice(liste_dep))
    nb_already = len(liste_comms)
    for i in range(number-nb_already):
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
    new_liste_comms = []
    for i in liste_comms :
        new_liste_comms.append(str(int(i)))
    return new_liste_comms

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

def create_shapefiles(departements,number_per_number,force_disjoint = False, disjoint_random = False, full_dep = False):
    for departement in departements :
        for i in range(len(number_per_number)) :
            for j in range(number_per_number[i]) :
                if i != 0 :
                    temp_j = get_list_comms(i+1,dict_comms[departement],True)
                    new_insee.main(temp_j)
                    temp_d = get_list_comms(i+1,dict_comms[departement],False,full_random=disjoint_random)
                    if force_disjoint :
                        c = 0
                        while (len(number_of_parts(temp_d)) == 1) and (c<100):
                            temp_d = get_list_comms(i+1,dict_comms[departement],False,full_random=disjoint_random)
                            c += 1
                    t = len(number_of_parts(temp_d))
                    print("nb_parts :",t)
                    new_insee.main(temp_d)
                else :
                    temp_j = get_list_comms(i+1,dict_comms[departement],True)
                    print(temp_j)
                    list_file = "python_files\\communes-dile-de-france-au-01-janvier\\existing-insees.txt"
                    new_insee.main([temp_j[0]])
                    #convert_espg.main([str(int(temp_j[0]))])
        if full_dep :
            temp_j = get_list_comms(0,dict_comms[departement],True,True)
            new_insee.main(temp_j)

def create_shapefiles_again(departements,number_per_number,force_disjoint = False, disjoint_random = False):
    liste_comms = []
    dep1 = departements[0]
    dep2 = departements[1]
    for i in departements :
        for j in dict_comms[i] :
            liste_comms.append[j]
    liste_dep_1 = liste_comms[departements[0]]
    liste_dep_2 = liste_comms[departements[1]]
    for i in range(len(number_per_number)):
        for j in range(number_per_number[i]):
            base_list_j = []
            base_list_j.append(r.choice(frontiers[dep1][dep2].keys()))
            base_list_j.append(r.choice(frontiers[dep1][dep2][base_list_j[0]]))
            temp_j = get_list_comms(i+1,liste_comms,True,base_list=base_list_j)
            new_insee.main(temp_j)
            base_list_dj = []
            base_list_dj.append(r.choice(liste_dep_1))
            base_list_dj.append(r.choice(liste_dep_2))
            temp_d = get_list_comms(i+1,liste_comms,False,full_random=disjoint_random,base_list=base_list_dj)
            if force_disjoint :
                c = 0
                while (len(number_of_parts(temp_d)) == 1) and (c<100):
                    temp_d = get_list_comms(i+1,liste_comms,False,full_random=disjoint_random,base_list=base_list_dj)
                    c += 1
            t = len(number_of_parts(temp_d))
            print("nb_parts :",t)
            new_insee.main(temp_d)

#create_shapefiles(departements,[5,1,1,1,1,1,1,1,1,1],force_disjoint=True,disjoint_random=True,full_dep=True)
create_shapefiles_again(["75","92"],[0,1,1,1,1,1,1,1,1,1],force_disjoint=True,disjoint_random=True)
create_shapefiles_again(["75","94"],[0,1,1,1,1,1,1,1,1,1],force_disjoint=True,disjoint_random=True)
create_shapefiles_again(["92","93"],[0,1,1,1,1,1,1,1,1,1],force_disjoint=True,disjoint_random=True)
create_shapefiles_again(["93","94"],[0,1,1,1,1,1,1,1,1,1],force_disjoint=True,disjoint_random=True)
                

            

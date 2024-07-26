import geopandas as gpd
import random as r
import get_new_insee_no_table
import json
import time as t
import get_existing_insees

start = t.time()
mat_file = "C:\\Users\\ulysse.marcandella\\Desktop\\eqasim-java-pr\\python_files\\emissions_calc_per_commune\\links_commune\\mat.json"
new_mat_file = "C:\\Users\\ulysse.marcandella\\Desktop\\eqasim-java-pr\\python_files\\emissions_calc_per_commune\\links_commune\\mat_extended.json"
folder_p = "python_files\\petite_couronne\\"

with open(mat_file) as json_file:
    pc_mat = json.load(json_file)
petite_couronne_mat = {}
for i in pc_mat.keys():
    temp = []
    for j in pc_mat[i] :
        temp.append(j)
    petite_couronne_mat[float(i)] = temp

with open(new_mat_file) as json_file:
    ex_mat = json.load(json_file)
extended_mat = {}
for i in ex_mat.keys():
    temp = []
    for j in ex_mat[i] :
        temp.append(j)
    extended_mat[float(i)] = temp

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

#get frontier of departements (used as basis for joint in 2 deps)
for i in range(len(departements)) :
    for j in range(len(departements)) :
        if i != j :
            for k in dict_comms[departements[i]] :
                for l in dict_comms[departements[j]] :
                    if l in petite_couronne_mat[k] :
                        if k not in frontiers[departements[i]][departements[j]].keys():
                            frontiers[departements[i]][departements[j]][k] = [l]
                        else :
                            frontiers[departements[i]][departements[j]][k].append(l)    

all_file = "python_files\\communes-dile-de-france-au-01-janvier\\communes-dile-de-france-au-01-janvier.shp"
communes_all = gpd.read_file(all_file)
liste_communes_all = []
for i in communes_all["insee"] :
    liste_communes_all.append(i)

def donut_or_not(drz):
    communes_outside = []
    for i in liste_communes_all :
        if str(int(i)) not in drz :
            if i in extended_mat.keys():
                communes_outside.append(str(int(i)))
    return len(number_of_parts(communes_outside,extended_mat)) > 1

def get_list_comms(number, liste_dep, joint_or_not = True, full_random = False, base_list = []):
    number = int(number)
    liste_comms = []
    for i in base_list :
        liste_comms.append(i)
    if liste_comms == []:
        liste_comms.append(r.choice(liste_dep))
    nb_already = len(liste_comms)
    if full_random :
        temp_liste_dep = []
        for i in liste_dep :
            if i not in liste_comms :
                temp_liste_dep.append(i)
        l = len(temp_liste_dep)
        for i in range(min(l,number-nb_already)):
            temp_comm = r.choice(temp_liste_dep)
            liste_comms.append(temp_comm)
            temp_liste_dep.remove(temp_comm)
        new_liste_comms = []
        for i in liste_comms :
            new_liste_comms.append(str(int(i)))
        return new_liste_comms
    for i in range(number-nb_already):
        touching_comms = []
        for j in liste_comms :
            for k in petite_couronne_mat[j]:
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

def number_of_parts(drz,mat=petite_couronne_mat):
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
        for i in drz :
            if i in drz_copy :
                if float(i) in mat[float(temp)] :
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
                    c = 0
                    while donut_or_not(temp_j) and (c<100):
                        temp_j = get_list_comms(i+1,dict_comms[departement],True)
                        c += 1
                    get_new_insee_no_table.main(temp_j)
                    temp_d = get_list_comms(i+1,dict_comms[departement],False,full_random=disjoint_random)
                    if force_disjoint :
                        c = 0
                        while ((len(number_of_parts(temp_d)) == 1) or donut_or_not(temp_j)) and (c<100):
                            temp_d = get_list_comms(i+1,dict_comms[departement],False,full_random=disjoint_random)
                            c += 1
                    t = len(number_of_parts(temp_d))
                    print("nb_parts :",t)
                    get_new_insee_no_table.main(temp_d)
                else :
                    temp_j = get_list_comms(i+1,dict_comms[departement],True)
                    get_new_insee_no_table.main([temp_j[0]])
        get_new_insee_no_table.main(dict_comms[departement])

def create_shapefiles_again(departements,number_per_number,force_disjoint = False, disjoint_random = False):
    liste_comms = []
    dep1 = departements[0]
    dep2 = departements[1]
    for i in departements :
        for j in dict_comms[i] :
            liste_comms.append(j)
    liste_dep_1 = dict_comms[departements[0]]
    liste_dep_2 = dict_comms[departements[1]]
    for i in range(len(number_per_number)):
        for j in range(number_per_number[i]):
            if i != 0 :
                base_list_j = []
                base_list_j.append(r.choice(list(frontiers[dep1][dep2].keys())))
                base_list_j.append(r.choice(frontiers[dep1][dep2][base_list_j[0]]))
                temp_j = get_list_comms(i+1,liste_comms,True,base_list=base_list_j)
                c = 0
                while donut_or_not(temp_j) and (c<100):
                    base_list_j = []
                    base_list_j.append(r.choice(list(frontiers[dep1][dep2].keys())))
                    base_list_j.append(r.choice(frontiers[dep1][dep2][base_list_j[0]]))
                    temp_j = get_list_comms(i+1,liste_comms,True,base_list=base_list_j)
                    c += 1
                get_new_insee_no_table.main(temp_j)
                base_list_dj = []
                base_list_dj.append(r.choice(liste_dep_1))
                base_list_dj.append(r.choice(liste_dep_2))
                temp_d = get_list_comms(i+1,liste_comms,False,full_random=disjoint_random,base_list=base_list_dj)
                if force_disjoint :
                    c = 0
                    while ((len(number_of_parts(temp_d)) == 1) or donut_or_not(temp_d)) and (c<100):
                        base_list_dj = []
                        base_list_dj.append(r.choice(liste_dep_1))
                        base_list_dj.append(r.choice(liste_dep_2))
                        temp_d = get_list_comms(i+1,liste_comms,False,full_random=disjoint_random,base_list=base_list_dj)
                        c += 1
                t = len(number_of_parts(temp_d))
                print("nb_parts :",t)
                get_new_insee_no_table.main(temp_d)
    get_new_insee_no_table.main(liste_comms)


create_shapefiles(departements,[5,1,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1],force_disjoint=True,disjoint_random=True,full_dep=True)
create_shapefiles_again(["75","92"],[0,1,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1],force_disjoint=True,disjoint_random=True)
create_shapefiles_again(["75","94"],[0,1,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1],force_disjoint=True,disjoint_random=True)
create_shapefiles_again(["92","93"],[0,1,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1],force_disjoint=True,disjoint_random=True)
create_shapefiles_again(["93","94"],[0,1,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1],force_disjoint=True,disjoint_random=True)              
get_existing_insees.main()
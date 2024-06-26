import matplotlib.pyplot as plt
import attributes as attrib
import json

att_files = []
ms_files = []
ms_names = []

for i in range(len(attrib.insees)) :
    att_files.append(attrib.att_file + str(attrib.insees[i]) + "_bs.json")
    ms_files.append(attrib.ms_file + str(attrib.insees[i]) + "_bs.json")
    ms_names.append(str(attrib.insees[i]) + "_bs")

for i in range(len(attrib.scenario_names)) :
    att_files.append(attrib.att_file + attrib.scenario_names[i] + ".json")
    ms_files.append(attrib.ms_file + attrib.scenario_names[i] + ".json")
    ms_names.append(attrib.scenario_names[i])

mss = []
for ms_file in ms_files:
    with open(ms_file) as json_file:
        ms = json.load(json_file)
        mss.append(ms)

dict_colors = {"walk":'#C8E6C9',"bike":'#80DEEA',"pt":'#FFECB3',"car_pt":'#ffcca2',"car_passenger":'#FFAB91',"car":'#E57373'}

largeur_barre = 0.8
types = attrib.types
modes = dict_colors.keys()

#regroup car_pt with pt_car and car with carInternal
for ms in mss :
    for type in types :
        if "car_pt" in  ms[type]["nb"].keys():
            #nb
            tot_car_pt_nb = ms[type]["nb"]["car_pt"] + ms[type]["nb"]["pt_car"]
            del ms[type]["nb"]["pt_car"]
            ms[type]["nb"]["car_pt"] = tot_car_pt_nb
            #dist
            tot_car_pt_dist = ms[type]["dist"]["car_pt"] + ms[type]["dist"]["pt_car"]
            del ms[type]["dist"]["pt_car"]
            ms[type]["dist"]["car_pt"] = tot_car_pt_dist
        if "carInternal" in  ms[type]["nb"].keys():
            #nb
            tot_car_nb = ms[type]["nb"]["car"] + ms[type]["nb"]["carInternal"]
            del ms[type]["nb"]["carInternal"]
            ms[type]["nb"]["car"] = tot_car_nb
            #dist
            tot_car_dist = ms[type]["dist"]["car"] + ms[type]["dist"]["carInternal"]
            del ms[type]["dist"]["carInternal"]
            ms[type]["dist"]["car"] = tot_car_dist

ys = []
for mode in dict_colors.keys() :
    yi = []
    for type in types :
        for ms in mss :
            if mode not in ms[type]["nb"].keys() :
                yi.append(0)
            else : 
                yi.append(round(ms[type]["nb"][mode]*100,ndigits=1))
    ys.append([yi,mode])
x = range(len(types)*len(ms_names)) # position en abscisse des barres
# Tracé
fig, ax = plt.subplots()
plt.bar(x, ys[0][0], width = largeur_barre, label = ys[0][1])
sum_prev_yi = ys[0][0]
for yi in ys[1:] :
    ax.bar(x, yi[0],bottom = sum_prev_yi, width = largeur_barre, label = yi[1], color = dict_colors[yi[1]])
    for i in range(len(sum_prev_yi)):
        sum_prev_yi[i] += yi[0][i]
for bars in ax.containers:
    ax.bar_label(bars,label_type = "center")
plt.legend()
ticks = []
for type in types :
    for ms_name in ms_names :
            ticks.append(ms_name + " " + type)
plt.xticks(range(len(types)*len(ms_names)),ticks)
plt.title("MS_"+attrib.nom_graphe)
#plt.show()
a = plt.gcf()
a.set_size_inches(20,10)
plt.savefig("Traitement_sorties\\Graphes\\MS_"+attrib.nom_graphe,bbox_inches="tight")

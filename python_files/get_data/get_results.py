import attributes as attrib
import json
import pandas as pd
import os
existing_insees_file = attrib.drz_composition_path
f = open(existing_insees_file)
lines = f.readlines()
f.close()
dict_drz = {}
dict_drz["insee"] = []
dict_drz["car_ms_res_nb"] = []
dict_drz["car_ms_inout_nb"] = []
dict_drz["car_ms_idf_nb"] = []
""" dict_drz["walk_ms_res_nb"] = []
dict_drz["walk_ms_inout_nb"] = []
dict_drz["walk_ms_idf_nb"] = [] """
dict_drz["att_res"] = []
dict_drz["att_inout"] = []
dict_drz["att_idf"] = []
dict_drz["er_0"] = []
dict_drz["er_10"] = []
dict_drz["er_20"] = []
dict_drz["er_idf"] = []

for i in range(len(lines)):
    insee = int(lines[i].split(";")[0])
    if os.path.exists(attrib.er_folder+f"\\bs_{insee}\\c_co2.json"):
        with open(attrib.er_folder+f"\\bs_{insee}\\c_co2.json") as json_file:
            er_bs = json.load(json_file)
        with open(attrib.er_folder+f"\\drz{insee}\\c_co2.json") as json_file:
            er = json.load(json_file)
        with open(attrib.att_folder+f"\\{insee}_bs.json") as json_file:
            att_bs = json.load(json_file)
        with open(attrib.att_folder+f"\\drz{insee}.json") as json_file:
            att = json.load(json_file)
        with open(attrib.ms_folder+f"\\{insee}_bs.json") as json_file:
            ms_bs = json.load(json_file)
        with open(attrib.ms_folder+f"\\drz{insee}.json") as json_file:
            ms = json.load(json_file)
        dict_drz["insee"].append(insee)
        dict_drz["car_ms_res_nb"].append(((ms["res"]["nb"]["car"]/ms_bs["res"]["nb"]["car"])-1)*100)
        dict_drz["car_ms_inout_nb"].append(((ms["inout"]["nb"]["car"]/ms_bs["inout"]["nb"]["car"])-1)*100)
        dict_drz["car_ms_idf_nb"].append(((ms["idf"]["nb"]["car"]/ms_bs["idf"]["nb"]["car"])-1)*100)
        """ dict_drz["walk_ms_res_nb"].append(((ms["res"]["nb"]["walk"]/ms_bs["res"]["nb"]["walk"])-1)*100)
        dict_drz["walk_ms_inout_nb"].append(((ms["inout"]["nb"]["walk"]/ms_bs["inout"]["nb"]["walk"])-1)*100)
        dict_drz["walk_ms_idf_nb"].append(((ms["idf"]["nb"]["walk"]/ms_bs["idf"]["nb"]["walk"])-1)*100) """
        dict_drz["att_res"].append(((att["res"]/att_bs["res"])-1)*100)
        dict_drz["att_inout"].append(((att["inout"]/att_bs["inout"])-1)*100)
        dict_drz["att_idf"].append(((att["idf"]/att_bs["idf"])-1)*100)
        dict_drz["er_0"].append(((er["0km"]/er_bs["0km"])-1)*100)
        dict_drz["er_10"].append(((er["10km"]/er_bs["10km"])-1)*100)
        dict_drz["er_20"].append(((er["20km"]/er_bs["20km"])-1)*100)
        dict_drz["er_idf"].append(((er["IDF"]/er_bs["IDF"])-1)*100)

df = pd.DataFrame.from_dict(dict_drz)
df.to_csv("python_files\\get_data\\res_drz.csv",index=False,sep=";")

import json
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import attributes as attrib
import os

commune = attrib.insee
shapefile_communes = attrib.shapefile_communes
shapefile_paris = "C:\\Users\\ulysse.marcandella\\Desktop\\eqasim-java-pr\\gis\\paris.shp"
shapefile_paris = gpd.read_file(shapefile_paris)
if attrib.basecase :
    trips_file_path = "..\\..\\simulation_output\\"+attrib.basecase_scenario+"\\eqasim_trips.csv"
else :
    trips_file_path = "..\\..\\simulation_output\\"+attrib.scenario_name+"\\eqasim_trips.csv"
shape_communes = gpd.read_file(shapefile_communes)
shape = shape_communes[(shape_communes["insee"] == commune)]
shape = shape.to_crs(shapefile_paris.crs)
shape = shape.geometry
shape =shape[shape.index[0]]

trips_df = pd.read_csv(trips_file_path, sep=";")

#get who is where
residents = {}
inout = {}
for j in trips_df.iterrows() :
    trip = j[1]
    origin = Point(trip["origin_x"],trip["origin_y"])
    dest = Point(trip["destination_x"],trip["destination_y"])
    person = trip["person_id"]
    if trip["person_trip_id"] == 0 :
        inout[person] = False
        if origin.within(shape) :
            residents[person] = True
        else :
            residents[person] = False
    if not residents[person] :
        if not inout[person] :
            if origin.within(shape) or dest.within(shape):
                inout[person] = True
print("Persons classified.")
#get ms and att
trips_df = trips_df[(trips_df["routed_distance"] != 0)]
ms = {"idf":{"nb":{},"dist":{}},"res":{"nb":{},"dist":{}},"inout":{"nb":{},"dist":{}}}
att = {"idf":0,"res":0,"inout":0}
count_idf = 0
count_res = 0
count_inout = 0
tot_dist_idf = 0
tot_dist_idf = 0
tot_dist_res = 0
tot_dist_inout = 0
for j in trips_df.iterrows() :
    trip = j[1]
    person = trip["person_id"]
    tt = trip["travel_time"]
    mode = trip["mode"]
    dist = trip["routed_distance"]
    #idf
    att["idf"] += tt
    if mode not in ms["idf"]["nb"].keys():
        ms["idf"]["nb"][mode] = 0
    if mode not in ms["idf"]["dist"].keys():
        ms["idf"]["dist"][mode] = 0
    ms["idf"]["nb"][mode] += 1
    ms["idf"]["dist"][mode] += dist
    count_idf += 1
    tot_dist_idf += dist
    #res
    if residents[person] :
        att["res"] += tt
        if mode not in ms["res"]["nb"].keys():
            ms["res"]["nb"][mode] = 0
        if mode not in ms["res"]["dist"].keys():
            ms["res"]["dist"][mode] = 0
        ms["res"]["nb"][mode] += 1
        ms["res"]["dist"][mode] += dist
        count_res += 1
        tot_dist_res += dist
    #inout
    elif inout[person]:
        att["inout"] += tt
        if mode not in ms["inout"]["nb"].keys():
            ms["inout"]["nb"][mode] = 0
        if mode not in ms["inout"]["dist"].keys():
            ms["inout"]["dist"][mode] = 0
        ms["inout"]["nb"][mode] += 1
        ms["inout"]["dist"][mode] += dist
        count_inout += 1
        tot_dist_inout += dist
#to percentage
#idf
att["idf"] = att["idf"]/count_idf
for mode in ms["idf"]["nb"].keys():
    ms["idf"]["nb"][mode] = ms["idf"]["nb"][mode]/count_idf
    ms["idf"]["dist"][mode] = ms["idf"]["dist"][mode]/tot_dist_idf
#res
att["res"] = att["res"]/count_res
for mode in ms["res"]["nb"].keys():
    ms["res"]["nb"][mode] = ms["res"]["nb"][mode]/count_res
    ms["res"]["dist"][mode] = ms["res"]["dist"][mode]/tot_dist_res
#inout
att["inout"] = att["inout"]/count_inout
for mode in ms["inout"]["nb"].keys():
    ms["inout"]["nb"][mode] = ms["inout"]["nb"][mode]/count_inout
    ms["inout"]["dist"][mode] = ms["inout"]["dist"][mode]/tot_dist_inout
#to file  
file_l = attrib.att_file
file_m = attrib.ms_file
if not os.path.exists(file_l):
        os.makedirs(file_l)
if not os.path.exists(file_m):
        os.makedirs(file_m)
if attrib.basecase :
    file_l += str(attrib.insee)+"_bs"
    file_m += str(attrib.insee)+"_bs"
else :
    file_l += attrib.scenario_name
    file_m += attrib.scenario_name
file_l += ".json"
file_m += ".json"
with open(file_l, "w") as outfile: 
    json.dump(att, outfile)
with open(file_m, "w") as outfile: 
    json.dump(ms, outfile)


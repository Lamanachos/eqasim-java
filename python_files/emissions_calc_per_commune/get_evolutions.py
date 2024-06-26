import attributes as attrib
import json

att_basecase_file = attrib.att_file + str(attrib.insee_base) + "_bs.json"
emissions_basecase_file = "emissions_results\\bs_" + str(attrib.insee) + "\\c_co2.json"
with open(att_basecase_file) as json_file:
    att_basecase = json.load(json_file)
with open(emissions_basecase_file) as json_file:
    emissions_basecase = json.load(json_file)

att_files = []
emissions_files = []
names = []
for i in range(len(attrib.scenario_names)) :
    att_files.append(attrib.att_file + attrib.scenario_names[i] + ".json")
    emissions_files.append("emissions_results\\" + attrib.scenario_names[i] + "\\c_co2.json")
    names.append(attrib.scenario_names[i])

atts = []
emissions = []
for i in range(len(att_files)):
    with open(att_files[i]) as json_file:
        att = json.load(json_file)
        atts.append(att)
    with open(emissions_files[i]) as json_file:
        emission = json.load(json_file)
        emissions.append(emission)
f = open(attrib.evolutions_file,"w")
f.write("Emissions :\n")
for zone in emissions_basecase.keys():
    f.write("Zone : "+ zone + "\n")
    f.write("basecase :" + str(round(emissions_basecase[zone],ndigits=1)) + "\n")
    for i in range(len(emissions)):
        percent = round(((emissions[i][zone]/emissions_basecase[zone])-1)*100,ndigits=2)
        if percent >= 0 :
            percent = "+"+str(percent)
        else :
            percent = str(percent)
        f.write(names[i] + ":" + str(round(emissions[i][zone],ndigits=1)) +"("+percent+"%)\n")

f.write("Average travel time :\n")
for zone in att_basecase.keys():
    f.write("Zone : " + zone + "\n")
    f.write("basecase : " + str(round(att_basecase[zone],ndigits=1))+ "\n")
    for i in range(len(atts)):
        percent = round(((atts[i][zone]/att_basecase[zone])-1)*100,ndigits=2)
        if percent >= 0 :
            percent = "+"+str(percent)
        else :
            percent = str(percent)
        f.write(names[i] + ":" + str(round(atts[i][zone],ndigits=1)) + "("+percent+"%)\n")

f.close()


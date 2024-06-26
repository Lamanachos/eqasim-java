import json
import os.path
attributes_file = "attributes.txt"

def build_attributes(basecase,sc_name=None,insee_par=None):
    if sc_name == None :
        scenario_name = "drz_75105_nores"
    else :
        scenario_name = sc_name
    if insee_par == None :
        insee = 7510593048
    else :
        insee = insee_par
    basecase = False
    basecase_scenario = "PTCar_BaseCase_rer_train_again13_0.75"
    #split_network
    network_file = "..\\..\\simulation_output\\"+scenario_name+"\\output_network"
    #split_emissions
    events_to_keep = ["warmEmissionEvent","coldEmissionEvent"]
    emissions_file = "..\\..\\simulation_output\\"+scenario_name+"\\output_emissions_events"
    emissions_split_folder_output = "emissions\\"+scenario_name+"_split"
    nb_break = 300000
    #get_links
    paris_shapefile = "Paris_shape\\Paris.shp"
    if basecase :
        results_dir = "..\\..\\emissions_results\\bs_" + str(insee)
    else:
        results_dir = "..\\..\\emissions_results\\"+scenario_name
    results_file = results_dir +"\\results.txt"
    if basecase :
        emissions_folder = "emissions\\"+basecase_scenario+"_split"
    else :
        emissions_folder = emissions_split_folder_output
    clean = True
    links_file = network_file + "_links"
    nodes_file = network_file + "_nodes"
    nb_bins_heure = 30
    nb_bins_dist = 10
    size_heure = (30*3600)//nb_bins_heure
    size_dist = 1000//nb_bins_dist
    #calculate_emissions
    emissions_results_folder = "..\\..\\emissions_results"
    liste_communes_in_paris = [75101,75102,75103,75104,75105,75106,75107,75108,75109,75110,75111,75112,75113,75114,75115,75116,75117,75118,75119,75120]
    nodes_commune_file = "..\\..\\simulation_output\\"+scenario_name+"\\nodes_commune.json"
    communes_co2_file = results_dir+"\\c_co2.json"
    communes_hdist_file = results_dir+"\\c_hdist.json"
    communes_hheure_file = results_dir+"\\c_hheure.json"
    new_shapefilename = "shapefiles_co2\\"+scenario_name
    #MS_ATT
    att_file = "..\\..\\MS_&_ATT\\ATT\\"
    ms_file = "..\\..\\MS_&_ATT\\MS\\"
    shapefile_communes = "..\\communes-dile-de-france-au-01-janvier\\communes-dile-de-france-au-01-janvier-with-fusions.shp"
#get_links_per_commune
    shapefile_communes_for_links = "..\\..\\gis\\"+str(insee)+"_buffered\\"+str(insee)+"_buffered.shp"
    precise_links = True
    #links_commune_file = "links_commune\\links_communes_prec.json"
    links_commune_folder = "links_commune"
    links_commune_file = links_commune_folder + "\\links_buffered_prec_"+str(insee)+".json"
    links_len_file = links_commune_folder + "\\links_len.json"
    just_drz = True
    #shapefile to compare
    file_to_compare = "..\\..\\emissions_results\\PTCar_BaseCase_rer_train_again13_0.75\\c_co2.json"
    #graphes
    scenario_names = ["drz_"+str(insee)+"_res","drz_"+str(insee)+"_nores"]
    insees = [insee]
    types = ["idf","res","inout"]
    nom_graphe = str(insee)
    #get_evolutions
    insee_base = insee
    evolutions_file = "..\\..\\evolutions\\"+str(insee)+".txt"
    #you have to execute split_emissions and split_network first (in whatever order), then get_per_commune, and then execute calculate_emissions
    #to visualize the results you can then execute hists_emissions
    variables = [item for item in locals() if not item.startswith("__")]
    dict = {}
    for v in variables :
        dict[v] = locals()[v]
    with open(attributes_file, "w") as outfile:
        json.dump(dict, outfile)

if __name__ == "__main__" :
    print("Building attributes")
    build_attributes(False)
else :
    if not os.path.isfile(attributes_file) :
        print("Building attributes")
        build_attributes(False)
    print("Loading attributes")
    with open(attributes_file) as json_file:
        dict = json.load(json_file)
    for v in dict.keys():
        globals()[v] = dict[v]


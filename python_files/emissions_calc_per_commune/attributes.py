import json
import os.path
origin_of_the_project = "C:\\lvmt_TS\\eqasim-java-drz_ai\\"
attributes_file = origin_of_the_project +"python_files\\emissions_calc_per_commune\\attributes\\attributes.txt"

def build_attributes(basecase=False,sc_name=None,sc_folder=None,insee_par=None,every_commune = False):
    if sc_name == None :
        scenario_name = "basecase"
    else :
        scenario_name = sc_name
    if insee_par == None :
        insee = 123456789
    else :
        insee = insee_par
    if sc_folder == None :
        # sc_folder = origin_of_the_project + "python_files\\output_5pc"
        sc_folder = r"E:\lvmt_TS_sim\sim_IdF_egt5pct_DRZ0.75"
    basecase = False
    # basecase_scenario = origin_of_the_project + "simulation_output\\PTCar_BaseCase_rer_train_again13_0.75"
    basecase_name = "basecase"
    basecase_scenario = r"E:\lvmt_TS_sim\sim_IdF_egt5pct_DRZ0.75"
    #split_network
    network_file = sc_folder+"\\output_network.xml.gz"
    #split_emissions
    events_to_keep = ["warmEmissionEvent","coldEmissionEvent"]
    emissions_file = sc_folder +"\\output_emissions_events.xml.gz"
    emissions_split_folder_output = origin_of_the_project + "python_files\\emissions_calc_per_commune\\emissions\\"+scenario_name+"_split"
    nb_break = 100000
    #get_links
    paris_shapefile = "Paris_shape\\Paris.shp"
    if basecase :
        results_dir = origin_of_the_project + "emissions_results\\bs_" + str(insee)
    else:
        results_dir = origin_of_the_project + "emissions_results\\"+scenario_name
    results_file = results_dir +"\\results.txt"
    if basecase :
        emissions_folder = origin_of_the_project + "emissions\\"+ basecase_name +"_split"
    else :
        emissions_folder = emissions_split_folder_output
    clean = True
    #if you want to resplit the network
    #links_file = network_file + "_links.xml"
    #nodes_file = network_file + "_nodes.xml"
    links_file = origin_of_the_project + "python_files\\split_network\\output_network_links.xml"
    nodes_file = origin_of_the_project + "python_files\\split_network\\output_network_nodes.xml"
    nb_bins_heure = 30
    nb_bins_dist = 10
    size_heure = (30*3600)//nb_bins_heure
    size_dist = 1000//nb_bins_dist
    #calculate_emissions
    emissions_results_folder = origin_of_the_project + "emissions_results"
    liste_communes_in_paris = [75101,75102,75103,75104,75105,75106,75107,75108,75109,75110,75111,75112,75113,75114,75115,75116,75117,75118,75119,75120]
    communes_co2_file = results_dir+"\\c_co2.json"
    communes_hdist_file = results_dir+"\\c_hdist.json"
    communes_hheure_file = results_dir+"\\c_hheure.json"
    new_shapefilename = origin_of_the_project + "shapefiles_co2\\"+scenario_name
    #Emissions from links
    links_emissions_basecase_file = origin_of_the_project + "python_files\\emissions_calc_per_commune\\emissions\\bc_emissions_per_link\\bc_emissions_per_link.json"
    #MS_ATT
    att_file = "MS_&_ATT\\ATT\\"
    ms_file = "MS_&_ATT\\MS\\"
    # shapefile_communes = origin_of_the_project + "python_files\\communes-dile-de-france-au-01-janvier\\communes-dile-de-france-au-01-janvier-with-fusions.shp"
    shapefile_commune_for_ms_and_att = r"E:\data__IdF\gis\scenarios_DRZ" + "\\" +str(insee)+"\\"+str(insee)+".shp"
#get_links_per_commune
    # shapefile_communes_for_links = origin_of_the_project + "gis\\"+str(insee)+"_buffered\\"+str(insee)+"_buffered.shp"
    shapefile_communes_for_links = r"E:\data__IdF\gis\scenarios_DRZ" + "\\" +str(insee)+"_buffered\\"+str(insee)+"_buffered.shp"
    precise_links = True
    #links_commune_file = "links_commune\\links_communes_prec.json"
    links_commune_folder = origin_of_the_project + "python_files\\emissions_calc_per_commune\\links_commune"
    just_drz = not every_commune
    if just_drz :
        links_commune_file = links_commune_folder + "\\links_all_communes.json"
        nodes_commune_file = links_commune_folder + "\\nodes_all_communes.json"
    else :
        links_commune_file = links_commune_folder + "\\links_buffered_prec_"+str(insee)+".json"
        nodes_commune_file = links_commune_folder + "\\nodes_" + str(insee) + ".json"
    links_len_file = links_commune_folder + "\\links_len.json"
    
    #shapefile to compare
    file_to_compare = origin_of_the_project + "emissions_results\\PTCar_BaseCase_rer_train_again13_0.75\\c_co2.json"
    #graphes
    scenario_names = ["drz_"+str(insee)+"_res","drz_"+str(insee)+"_nores"]
    insees = [insee]
    types = ["idf","res","inout"]
    nom_graphe = str(insee)
    #get_evolutions
    insee_base = insee
    evolutions_file = origin_of_the_project + "evolutions\\"+str(insee)+".txt"
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
    build_attributes()
else :
    if not os.path.isfile(attributes_file) :
        print("Building attributes")
        build_attributes()
    print("Loading attributes")
    with open(attributes_file) as json_file:
        dict = json.load(json_file)
    for v in dict.keys():
        globals()[v] = dict[v]


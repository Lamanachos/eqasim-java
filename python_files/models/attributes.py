data_file = "python_files\\get_data\\data_drz.csv" #adresse des caractéristiques des DRZ
results_file = "python_files\\get_data\\res_drz.csv" #adresse des résultats des DRZ
gis_clean_folder = "gis_clean" #adresse des tracés des DRZ
existing_insees = "python_files\\get_data\\existing_insees.txt" #adresse de la liste des drz existantes
ann_dep_split = [["92","75","9293","9394"],["93","7594"],["94","7592"]] #split des départements pour les anns
ml_dep_split = [["92","75","9293","9394"],["93","7594","94","7592"],[]] #split des départements pour les autres modèles

corpus_folder = "python_files\\models\\corpus" #adresse ou sauver le corpus
info_insees_folder = "python_files\\models\\info_insees" #adresse ou sauver les infos sur les insees
output_folder = "python_files\\models\\outputs" #adresse ou sauver les sorties des anns
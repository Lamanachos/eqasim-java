gis_folder = "gis_clean" #dossier où sont rangés les shapefiles des DRZ
shapefile_paris = gis_folder+"\\paris.shp" #adresse de la shapefile de paris (utilisé seulement comme référence de crs)
drz_composition_path = "python_files\\get_data\\existing_insees.txt" #pas besoin de modifier
ms_folder = "MS_&_ATT_clean\\MS" #dossier ou sont rangés les modal shares
att_folder = "MS_&_ATT_clean\\ATT" #dossier où sont rangés les average travel time
er_folder = "ER_clean" #dossier où sont rnagés les émissions
skip_insees = [100092,100083,100074,100065,100014,100028,100042,100056] #insees pour lesquelles on ne veut pas calculer les datas (par exemple les départements entiers car c'est des outliers)
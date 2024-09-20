import geopandas as gpd
import os
import attributes as attrib

#obtenir la shapefile de communes appartenant à certains départements
shapefile_communes = attrib.communes_idf_file
dest_folder = attrib.dest_folder_pc

def get_in_zone(zone,dest):
    # zone : liste de départements ex : ["92","93","94","75"]
    # dest : nom du fichier ou sauver la shapefile, celui ci sera mis dans le dossier dest_folder
    dest = dest_folder + dest
    if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)
    shape_communes = gpd.read_file(shapefile_communes)
    liste_communes = []
    for i in shape_communes["insee"] :
        if str(i)[:2] not in zone:
            liste_communes.append(i)
    liste_shapes = []
    for i in liste_communes:
        ind = shape_communes[(shape_communes["insee"] == i)].index
        shape_communes.drop(ind, inplace = True)
    shape_communes.to_file(dest)

get_in_zone(["92","93","94","75"],"petite_couronne.shp")
get_in_zone(["92"],"92.shp")
get_in_zone(["93"],"93.shp")
get_in_zone(["94"],"94.shp")
get_in_zone(["75"],"75.shp")

    
# Obtenir les DRZ et leurs caractéristiques

Avant toutes choses, dans python_files/get_data/attributes.py modifier les valeurs des paramètres pour qu’elles pointent vers les différents endroits où sont stockés les sorties (plus de précisions dans le fichier attributes.py).

## Générer des DRZ

### Obtenir les matrices d'adjacences

Lancer get_petite_couronne.py.

Lancer generate_neighbors_mat.py (peut prendre plus de 20 minutes).

Lancer generates_extended_neighbors_mat.py (peut prendre plus de 7 minutes).

### Générer un groupe de DRZ

Dans le fichier generate_drz_list.py il faut éxécuter les fonctions create_shapefiles et create_shapefiles_again.
create_shapefile crée des drz sur un département et create_shapefiles_again sur deux départements.

#### create_shapefiles

Explication des paramètres :

departements : liste des départements ou créer des drz
number_per_number : liste d'entier, pour chque indice il sera crée le nombre de drz inscrit à cet indice de taille l'indice plus un
force_disjoint : si false quand on essaie de générer des drz disjointes, si elles ne le sont pas on ne réessaie pas
disjoint_random : si false on construit les drz disjointes commune par commune (toujours mettre true)
full_dep : si true on génére pour chaque département une drz contenant toutes ses communes 

Exemple :
```python
create_shapefiles(["92","93"],[2,0,0,1],force_disjoint = True, disjoint_random = True, full_dep = False):
```
Va créer 2 DRZ de taille 1 jointes, 2 DRZ de taille 1 disjointes, 1 DRZ de taille 4 jointes, 1 DRZ de taille 4 disjointes dans le département 92, et faire de même pour le 93.

#### create_shapefiles_again

Explication des paramètres :

Les paramètres sont les mêmes sauf departments.

departements : les deux départments dans lequels vont se trouver les drz générées

Exemple :
```python
create_shapefiles(["92","93"],[0,2,0,1],force_disjoint = True, disjoint_random = True, full_dep = False):
```
Va créer 2 DRZ de taille 2 jointes, 2 DRZ de taille 2 disjointes, 1 DRZ de taille 4 jointes, 1 DRZ de taille 4 disjointes qui ont toutes au moins une commune dans le 92 et au moins une commune dans le 93.

## Obtenir les caractéristiques des DRZ 

### Obtention des données nécessaires 
Lancer get_existing_insees.py.

Lancer get_joint_coeff_for_each_drz.py.

S'assurer que les fichiers nécessaire pour le lancement de get_data_for_each_communes.py sont présents, si besoin modifier les chemins au début de get_data_for_each_communes.py (plus de précisions dans le fichier).

Lancer get_data_for_each_communes.py.

### Obtenir les caractéristiques des DRZ 

Lancer get data_for_each_drz.py

Les données seront disponibles à l'adresse python_files\\get_data\\data_drz.csv.

## Obtenir les sorties (en %)

Lancer get_results.py.

Les données seront disponibles à l'adresse python_files\\get_data\\res_drz.csv.

# Utiliser les modèles de machine learning


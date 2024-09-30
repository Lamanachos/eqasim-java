# Obtenir les DRZ et leurs caractéristiques

Tous les fichiers utilisés dans cette partie sont dans le dossier python_files/get_data.

Avant toutes choses, dans python_files/get_data/attributes.py modifier les valeurs des paramètres pour qu’elles pointent vers les différents endroits où sont stockés les sorties (plus de précisions dans le fichier attributes.py).

## Générer des DRZ

### Obtenir les matrices d'adjacences des communes de la petite_couronne

Éxécuter get_petite_couronne.py.

Éxécuter generate_neighbors_mat.py (peut prendre plus de 20 minutes).

Éxécuter generates_extended_neighbors_mat.py (peut prendre plus de 7 minutes).

### Générer un groupe de DRZ

Dans le fichier generate_drz_list.py il faut éxécuter les fonctions create_shapefiles et create_shapefiles_again.

create_shapefile crée des drz sur un seul département et create_shapefiles_again sur deux départements.

#### create_shapefiles

Explication des paramètres :

departements : liste des départements où créer des drz

number_per_number : liste d'entiers, pour chaque indice il sera crée le nombre de drz inscrit à cet indice de taille l'indice plus un

force_disjoint : si false quand on essaie de générer des drz disjointes, si elles ne le sont pas on ne réessaie pas

disjoint_random : si false on construit les drz disjointes commune par commune (toujours mettre true)

full_dep : si true on génére pour chaque département une drz contenant toutes ses communes 

Exemple :
```python
create_shapefiles(["92","93"],[2,0,0,1],force_disjoint = True, disjoint_random = True, full_dep = False)
```
Va créer 2 DRZ de taille 1 jointes, 2 DRZ de taille 1 disjointes, 1 DRZ de taille 4 jointes, 1 DRZ de taille 4 disjointes dans le département 92, et faire de même pour le 93.

#### create_shapefiles_again

Explication des paramètres :

Les paramètres sont les mêmes sauf departments.

departements : les deux départments dans lequels vont se trouver les drz générées

Exemple :
```python
create_shapefiles(["92","93"],[0,2,0,1],force_disjoint = True, disjoint_random = True, full_dep = False)
```
Va créer 2 DRZ de taille 2 jointes, 2 DRZ de taille 2 disjointes, 1 DRZ de taille 4 jointes, 1 DRZ de taille 4 disjointes qui ont toutes au moins une commune dans le 92 et au moins une commune dans le 93.

## Obtenir les caractéristiques des DRZ 

### Obtention des données nécessaires 
Éxécuter get_existing_insees.py.

Éxécuter get_joint_coeff_for_each_drz.py.

S'assurer que les fichiers nécessaire pour le lancement de get_data_for_each_communes.py sont présents, si besoin modifier les chemins au début de get_data_for_each_communes.py (plus de précisions dans le fichier).

Éxécuter get_data_for_each_communes.py.

### Obtenir les caractéristiques des DRZ 

Éxécuter get data_for_each_drz.py

Les données seront disponibles à l'adresse python_files\\get_data\\data_drz.csv.

## Obtenir les sorties (comparaison des sorties de la simulation avec le cas de base)

Éxécuter get_results.py.

Les données seront disponibles à l'adresse python_files\\get_data\\res_drz.csv.

# Utiliser les modèles de machine learning

Tous les fichiers utilisés dans cette partie siont dans le dossier python_files/models.

Avant toutes choses, dans python_files/models/attributes.py modifier les valeurs des paramètres pour qu’elles pointent vers les différents endroits où sont stockés les sorties (plus de précisions dans le fichier attributes.py).

## Utiliser le préparateur de corpus

get_train_test_val.py contient du code permettant de préparer et mettre en forme les données.

#### build_test_train

build_test_train prend en entrée de multiples paramètres et retourne des données (presque) prêtes à l'emploi.

Cette fonction permet aussi de normaliser les données.

Explication des paramètres :

df_data : dataframe des features

df_results : dataframe des résultats

split_type : random -> aléatoire, dep -> par département, classic -> une drz de chaque type dans train et le reste est séparé équitablement entre test et validation, old_school -> obsolete

split_arg : varies with split_type  random -> [test ratio, validation ratio] dep -> [departments for training, departements for testing, ddepartements for validation], classic -> no_block si true ça va classer toutes les DRZ même celles dont on a pas calculé les résultats, old_school -> no_block même chose qu'avant

normX : if true, the inputs will be normalized

normY : if true, the outputs will be normalized

list_res : list of the outputs you want to keep

list_feats : list of the feats you want to keep

## KNNs, linear regression et Gradient Boosted Trees

Dans linear_gbt_knn.py choisir le mode de découpage du corpus, ses arguments, la liste des résultats et features à prendre en compte. Pour plus de précisions voir ci-dessus.

Choisir si on veut normaliser les entrées et les sorties.

Choisir le modèle (knn, linear, gbt).

Exécuter linear_gbt_knn.py.

Les sorties se font dans le terminal.

## Spectral Vector Machines

Dans svr.py faire les mêmes choix que ci-dessus.

Exécuter linear_gbt_knn.py.

Les sorties se font dans le terminal.

## Artificial Neural Networks

Dans anns_run.py faire les même choix que ci-dessus.


Dans un terminal se rendre dans le dossier eqasim-java-pr puis éxécuter par exemple :
```shell
python python_files\\models\\anns_run.py -t dense_mix -m 1 -n bonjour
```

L'argument -t permet de choisir le type de modèle : dense_mix ou dense_alone, si il n'est pas précisé dense_mix sera choisi.

L'argument -m permet de choisir le nombre de modèles que l'on veut entraîner, si il n'est pas précisé 1 sera choisi.

L'argument -n permet de donner un nom au modèle pour le reconnaître dans les outputs, si il n'est pas précisé la date et l'heure seront utilisés comme noms.

Les résultats seront disponibles dans un rapport situé à l'adresse précisée dans attributes.py.

Les résultats contiennent un rapport qui contient diverses infos sur le modèle dont leur évaluation, une courbe de l'évaluation de la RMSE et de la perte en fonction des itérations, la même mais centrée sur les itérations supérieures à 100, et le modèle.

### Réévaluer un ann

load_and_test_model.py permet de réévaluer un modèle. 

En changeant model_path pour l'adresse du modèle que l'on veut évaluer et en configurant le bon split de corpus, on a ensuite juste à éxécuter le fichier.

Les sorties se font dans le terminal.


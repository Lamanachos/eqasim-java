# Générer des DRZ




# Obtenir les caractéristiques des DRZ 

Dans attributes.py modifier les valeurs des paramètres pour qu’elles pointent vers les différents endroits où sont stockés les sorties (plus de précisions dans le fichier)

Lancer get_joint_coeff_for_each_drz.py.

S'assurer que les fichiers nécessaire pour le lancement de get_data_for_each_communes.py sont présents, si besoin modifier les chemins au début de get_data_for_each_communes.py (plus de précisions dans le fichier).

Lancer get_data_for_each_communes.py.

Lancer get data_for_each_drz.py

Les données seront disponibles à l'adresse python_files\\get_data\\data_drz.csv.

# Obtenir les sorties (en %)



# Utiliser les modèles

# Segmentation de séries temporelles multivariées

## Setup

Pour lancer une expérience anns :

```shell
python3 ./scripts/anns_run.py -t mo
```
```python
batch_size = 64
epochs = 30 
validation_split = 0.2 #si il n'y à pas de de chemin_val renseigné la validation 
#se fera sur cette fraction du corpus d'entraînement
num_unit_lstm = 128 #un paramètre lié aux architectures de corpus
nb_obs_per_window = 20
nb_feats = 4 #4 si on utilise pas la vitesse, 5 sinon
drop_speed = True #si True on utilise pas la vitesse
size_after_conv = 8 #un paramètre lié à la taille des fenêtres,
# pour l'utilisation de mo c'est nb_obs_per_windows - 12 
#(c'est la taille de la sortie des couches de convolution)

chemin_train = "../data/ml_data_FDBA_normalized_fenetres_train" #mettre de préférence un corpus normalisés (indispensable pour avoir des résultats satisfaisants)
chemin_test = "../data/ml_data_FDBA_normalized_fenetres_test"#idem
chemin_val = None#si pas renseigné, coir validation_split
```


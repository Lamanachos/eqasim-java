# Quelques analyses statistiques sur les entrées et sorties

## Graphes disponibles

Dans all_graphes on trouve les graphes de toutes les combinaisons d'entrées et sorties possibles.

Chaque image regroupe un ensemble de graphes. 

Chaque image représente les relations des entrées ou des sorties avec une entréee ou sortie en particulier.

### Nom des graphes

Le nom des images est toujours construit de la même manière : a_with_b.png.

a représentes les ordonnées et b les abcisses.

Par exemple results_with_pop.png va contenir les graphes de chaque sortie en fonction de la population.

### Légendes

Certains graphes n'ont pas de légende par manque de place.

Tout les graphes partagent la même légende et elle peut donc être trouvée sur d'autres graphes.

### div_area_graphes

Le dossier div_area_graphes contient les même graphes que all_graphes sauf que la plupart des entrées ont été remplacées par leur densité.

## Analyses sur les graphes

### Matrice de corrélation

![Matrice de corrélation](.\mat_corr.png)

On peut voir que la plupart des sorties sont fortement corrélées à l'aire, sauf le gain de temps de trajet pour les résidents et les utilisateurs, ainsi que le gain d'émissions de CO2 dans la drz.
 
Les temps de trajets semblent être plutôt corrélés avec le nombre de voiture par personne.

La seule des entrées qui est corrélée de manière non négligeable avec le gain d'émissions de CO2 dans la DRZ est le nombre de kilomètres d'autoroutes, ce qui était attendu.

La plupart des entrées sont trés fortement corrélées à l'aire et donc ensemble.

La matrice de corrélation avec les densité des entrées peut être aussi intéressante.

### Matrice de corrélation des densités

Les entrées ont été remplacées par leur densité sauf pour le nombre de voiture par personnes, la part modale de la marche dans le cas de base et le coefficient de jointure.

![Matrice de corrélation des densités](.\mat_corr_div_area.png)

Les entrées qui étaient très fortement corrélées à l'aire ne le sont plus et donc ne sont plus corrélées aux même sorties.

Elles sont maintenant corrélées au gain du temps de trajet moyen. 

Les autres relations semblent rester les mêmes même si elles sont parfois accentuées.

## Graphes de relations entre les entrées et sorties




# État de l'art sur la mise en place de modèle de machine learning dans le but de remplacer une simulation complexe

Tous les articles, sauf un auquel je n'avais pas accès, peuvent être trouvés dans le dossier contenant ce fichier.

Le fichier excel articles.xlsx recense les articles ainsi que leurs caractéristiques (objectif, domaine d'études, méthodes utilisées...) et les commentaires que j'ai pu faire sur la pertinence de leur inclusion dans la litterature review.

Je n'ai pas eu le temps de faire une biblio propre, je référence les articles avec le numéro que je leur ai donné dans le fichier excel.

## Définitions

Pour bien comprendre de quoi on parle il est nécéssaire de définir par avance ce que veut dire "surrogate modeling" (modèles de substitution) et "metamodeling" (mettre en place des métamodèles).

Le "surrogate modeling" c'est créer des modèles simplifiés pour remplacer des simulations plus complexes, souvent dans un but d'efficacité. Le metamodeling se concentre sur la mise en place de modèles de différents niveaux de complexité et de fiabilité [14].

Le surrogate modeling est donc une partie du metamodeling.

Ce qui a été effectué pendant le stage était du surrogate modeling.

## État de l'art

Dans certains cas d'optimisation, l'objectif peut être difficilement atteignable car l'évaluation prend un temp trop élevé.

C'est le cas par exemple lorsque notre évaluation se fait à l'aide d'une simulation complexe.

On peut alors recourir au surrogate modeling qui permet de mettre en place un modèle qui approxime la simulation et nous permet alors de procéder à notre optimisation.

Le surrogate modeling est utilisé dans de nombreux domaines que ce soit dans la simulation moléculaire [4,7], dans la gestion de chaînes logistiques [3], dans la simulation de processus chimiques [2] ou dans la simulation des transports dans une ville [8,9,10,11,13].

Dans le domaine qui nous intéresse, les transports, le surrogate modeling est souvent utilisé pour optimiser une politique, cela peut être les horaires des bus [15], le prix des péages [10], les DRZ [13].

Il peut être aussi utilisé pour obtenir des résultats plus rapidement sans nécessairement qu'il y ait l'optimisation d'une politique, dans [11], le surrogate modeling est utilisé pour obtenir en temps réel des prédictions sur le trafic d'une route. 

Dans [15], il est développé un framework pour permettre d'optimiser les horaires de bus en temps réel.

Le surrogate modeling, en diminuant le temps nécessaire pour obtenir les résultats d'une simulation permet de mettre en place des systèmes en temps réel qu'il ne serait pas possible de mettre en place avec seulement des simulations classiques.

Il y a de nombreuses manières de mettre en place un surrogate model [2,6]. 

Certaines sont très reliées à leur domaine, dans [4] est présenté des architectures de neural networks dédiées à la simulation moléculaire et qui permettent de régler des problèmes uniques à ce domaine. 

Dans la plupart des cas [6,9,10,11,12], lorsqu'on se trouve dans une situation précise, on met en place un grand nombre des méthodes de machine learning classiques, comme les random forest, les gradient boosted trees, différentes régressions... (plus de détails dans le fichier excel) et/ou des réseaux de neurones, puis ont les évalue afin de choisir la plus pertinente pour notre situation.

Dans les cas avec un grand nombre de données, les anns sont généralement plus performants, mais au vu de la situation, comme on veut souvent remplacer des simulations très complexes, et donc pour lesquelles on va pouvoir faire peu de calculs, on est souvent obligés de se rabattre vers des méthodes nécéssitant moins de données.

Comme dit plus haut de nombreux articles montrent que le surrogate modeling peut être utilisé pour la simulation de transports.
L'article [12] montre que faire du surrogate modeling pour des modèles multi-agents est possible.
L'article [11] utilise le surrogate modeling sur MATSIM pour pouvoir trouver la DRZ optimale à mettre en place à Bilbao ce qui est similaire à notre projet.

Dans [13] est mis en place un Partially Observable Discrete Event Decision Process (PODEDP) pour remplacer MATSIM, ce qui à l'air très différent des autres méthodes mais j'ai du mal à comprendre si c'est vraiment le même type de processus. Se pencher plus de temps sur l'article pourrait être intéressant.




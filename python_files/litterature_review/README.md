# Litterature review sur la mise en place de modèle de machine learning dans le but de remplacer une simulation complexe

Tous les articles, sauf un auquel je n'avais pas accès, peuvent être trouvés dans le dossier contenant ce fichier.

Le fichier excel articles.xlsx recense les articles ainsi que leurs caractéristiques (objectif, domaine d'études, méthodes utilisées...) et les commentaires que j'ai pu faire sur la pertinence de leur inclusion dans la litterature review.

La bibliographie se trouve à la fin du document.

## Définitions

Pour bien comprendre de quoi on parle il est nécéssaire de définir par avance ce que veut dire "surrogate modeling" (modèles de substitution) et "metamodeling" (mettre en place des métamodèles).

Le "surrogate modeling" c'est créer des modèles simplifiés pour remplacer des simulations plus complexes, souvent dans un but d'efficacité. Le metamodeling se concentre sur la mise en place de modèles de différents niveaux de complexité et de fiabilité [[14]](#14).

Le surrogate modeling est donc une partie du metamodeling.

Ce qui a été effectué pendant le stage était du surrogate modeling.

## Litterature review

Dans certains cas d'optimisation, l'objectif peut être difficilement atteignable car l'évaluation prend un temp trop élevé.

C'est le cas par exemple lorsque notre évaluation se fait à l'aide d'une simulation complexe.

On peut alors recourir au surrogate modeling qui permet de mettre en place un modèle qui approxime la simulation et nous permet alors de procéder à notre optimisation.

Le surrogate modeling est utilisé dans de nombreux domaines que ce soit dans la simulation moléculaire [[4,7]](#4), dans la gestion de chaînes logistiques [[3]](#3), dans la simulation de processus chimiques [[2]](#2) ou dans la simulation des transports dans une ville [[8,9,10,11,13]](#8).

Dans le domaine qui nous intéresse, les transports, le surrogate modeling est souvent utilisé pour optimiser une politique, cela peut être les horaires des bus [[15]](#15), le prix des péages [[10]](#10), les DRZ [[13]](#13).

Il peut être aussi utilisé pour obtenir des résultats plus rapidement sans nécessairement qu'il y ait l'optimisation d'une politique, dans [[11]](#11), le surrogate modeling est utilisé pour obtenir en temps réel des prédictions sur le trafic d'une route. 

Dans [[15]](#15), il est développé un framework pour permettre d'optimiser les horaires de bus en temps réel.

Le surrogate modeling, en diminuant le temps nécessaire pour obtenir les résultats d'une simulation permet de mettre en place des systèmes en temps réel qu'il ne serait pas possible de mettre en place avec seulement des simulations classiques.

Il y a de nombreuses manières de mettre en place un surrogate model [[2,6]](#2). 

Certaines sont très reliées à leur domaine, dans [[4]](#4) est présenté des architectures de neural networks dédiées à la simulation moléculaire et qui permettent de régler des problèmes uniques à ce domaine. 

Dans la plupart des cas [[6,9,10,11,12]](#6), lorsqu'on se trouve dans une situation précise, on met en place un grand nombre des méthodes de machine learning classiques, comme les random forest, les gradient boosted trees, différentes régressions... (plus de détails dans le fichier excel) et/ou des réseaux de neurones, puis ont les évalue afin de choisir la plus pertinente pour notre situation.

Dans les cas avec un grand nombre de données, les anns sont généralement plus performants, mais au vu de la situation, comme on veut souvent remplacer des simulations très complexes, et donc pour lesquelles on va pouvoir faire peu de calculs, on est souvent obligés de se rabattre vers des méthodes nécéssitant moins de données.

Comme dit plus haut de nombreux articles montrent que le surrogate modeling peut être utilisé pour la simulation de transports.
L'article [[12]](#12) montre que faire du surrogate modeling pour des modèles multi-agents est possible.
L'article [[11]](#11) utilise le surrogate modeling sur MATSIM pour pouvoir trouver la DRZ optimale à mettre en place à Bilbao ce qui est similaire à notre projet.

Dans [[13]](#13) est mis en place un Partially Observable Discrete Event Decision Process (PODEDP) pour remplacer MATSIM (ce qui a l'air très différent des autres méthodes mais j'ai du mal à comprendre si c'est vraiment le même type de processus, se pencher plus de temps sur l'article pourrait être intéressant).

## Bibliographie

<a name="1"></a>
[1] HONG, L. Jeff et ZHANG, Xiaowei. Surrogate-based simulation optimization. In : Tutorials in Operations Research: Emerging Optimization Methods and Modeling Techniques with Applications. INFORMS, 2021. p. 287-311.

<a name="2"></a>
[2] COZAD, Alison, SAHINIDIS, Nikolaos V., et MILLER, David C. Learning surrogate models for simulation‐based optimization. AIChE Journal, 2014, vol. 60, no 6, p. 2211-2227.

<a name="3"></a>
[3] WAN, Xiaotao, PEKNY, Joseph F., et REKLAITIS, Gintaras V. Simulation-based optimization with surrogate models—application to supply chain management. Computers & chemical engineering, 2005, vol. 29, no 6, p. 1317-1328.

<a name="4"></a>
[4] NOÉ, Frank, TKATCHENKO, Alexandre, MÜLLER, Klaus-Robert, et al. Machine learning for molecular simulation. Annual review of physical chemistry, 2020, vol. 71, no 1, p. 361-390.

<a name="5"></a>
[5]L’article n’a pas été utilisé finalement

<a name="6"></a>
[6] BARTON, Russell R. Tutorial: Metamodeling for simulation. In : 2020 Winter Simulation Conference (WSC). IEEE, 2020. p. 1102-1116.

<a name="7"></a>
[7] POROPUDAS, Jirka et VIRTANEN, Kai. Simulation metamodeling with dynamic Bayesian networks. European Journal of Operational Research, 2011, vol. 214, no 3, p. 644-655.

<a name="8"></a>
[8] ZHANG, Jun, CHEN, Dechin, XIA, Yijie, et al. Artificial intelligence enhanced molecular simulations. Journal of Chemical Theory and Computation, 2023, vol. 19, no 14, p. 4338-4350.

<a name="9"></a>
[9] VLAHOGIANNI, Eleni I. Optimization of traffic forecasting: Intelligent surrogate modeling. Transportation Research Part C: Emerging Technologies, 2015, vol. 55, p. 14-23.

<a name="10"></a>
[10] CHEN, Xiqun, ZHANG, Lei, HE, Xiang, et al. Surrogate‐based optimization of expensive‐to‐evaluate objective for optimal highway toll charges in transportation network. Computer‐Aided Civil and Infrastructure Engineering, 2014, vol. 29, no 5, p. 359-381.

<a name="11"></a>
[11] SHULAJKOVSKA, Miljana, SMERKOL, Maj, DOVGAN, Erik, et al. A machine-learning approach to a mobility policy proposal. Heliyon, 2023, vol. 9, no 10.

<a name="12"></a>
[12] ANGIONE, Claudio, SILVERMAN, Eric, et YANESKE, Elisabeth. Using machine learning as a surrogate model for agent-based simulations. Plos one, 2022, vol. 17, no 2, p. e0263150.

<a name="13"></a>
[13] KHAIDEM, Luckyson, LUCA, Massimiliano, YANG, Fan, et al. Optimizing transportation dynamics at a city-scale using a reinforcement learning framework. IEEE Access, 2020, vol. 8, p. 171528-171541.

<a name="14"></a>
[14] KHATOURI, Hanane, BENAMARA, Tariq, BREITKOPF, Piotr, et al. Metamodeling techniques for CPU-intensive simulation-based design optimization: a survey. Advanced Modeling and Simulation in Engineering Sciences, 2022, vol. 9, no 1, p. 1.

<a name="15"></a>
[15] OTHMAN, Muhammad Shalihin Bin et TAN, Gary. Machine learning aided simulation of public transport utilization. In : 2018 IEEE/ACM 22nd International Symposium on Distributed Simulation and Real Time Applications (DS-RT). IEEE, 2018. p. 1-2.



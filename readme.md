
# Application de visualisation de simulation épidémiologique


## Contexte

Dans le cadre de mon projet de fin de Baccalauréat en physique, et dans l'optique de la poursuite de mes études dans une maitrise en informatique, ce projet de visualisation de simulation épidémiologique (et en particulier sur des réseau small-world) fut développé sous la supervision de Paul Charbonneau, professeur de physique à l'université de Montréal.

Cette application se veut la fondation du projet, qui pourra, selon la demande, être repris et améliorer par de futures élèves afin de constituer une étude comparative des différents algorithmes de génération de graphes de type "small-world" et des impacts de l'utilisation de ceux-ci sur les résultats de simulation.

## Démarrage rapide

Le coeur de la visualisation est contenu dans app.py, alors que la simulation en tant que soit est contenu dans "plague.py". Le but est de maintenir ce fichier comme indépendant du restant de la simulation , permettant de rapidement pouvoir comparer les résultats et "débugger" tout problème éventuel. Prerequisite contient des définitions de fonctions et de classe nécessaire à l'exécution de "plague.py".


### App.py

Ce code utilise les modules Dash, plotly et flask pour générer un serveur local et permettre ainsi de créer une page html qui prends en entrée les choix de l'utilisateur et retourne les résultats de la simulation épidémiologique

### Le module babel

Le module babel peut être lié avec l'application Flask pour traduire les messages contenus dans l'application. Toutefois, dù à certaines limitations, cette fonctionnalité n'est pas encore complètement fonctionnel (il suffirait d'utiliser l'application Alouette comme modèle pour créer un appel à la traduction). Par manque de temps, cette fonctionnalité ne fut pas encore implémenté.

### prerequisite.py

Le fichier prerequisite contients les définitions de classes et de fonctions permettant à la boucle de la simulation épidémiologique de fonctionner. Cela permet d'alléger le fichier plague.py

#### Classe Personne

La classe personne est l'élément clé de la simulation. Chaque marcheur sera un objet de type personne, cette classe permettant de stocker toutes les propriétés sur celui-ci et de facilement en ajouter.

#### Watts-strogatz

Cette fonction est une tentative d'implémentation maison de l'algorithme de génération de graphe de Watts-Strogatz. Toutefois, des résultats préliminaires décevant après plusieurs tentatives forca l'utilisation de la fonction Watts-strogatz et connected-watts-strogatz à partir du module networkx

[connected watts_strogatz_graph](https://networkx.org/documentation/networkx-1.9.1/reference/generated/networkx.generators.random_graphs.connected_watts_strogatz_graph.html)

[watts_strogatz_graph](https://networkx.org/documentation/networkx-1.9/reference/generated/networkx.generators.random_graphs.watts_strogatz_graph.html)
#### Small-world-power-law

La fonction Small-world-power-law est un autre algorithme de génération de graphe de type small-World. Son implémentation, bien que techniquement fonctionnel, donna des résultats qui levait des doutes sur la qualité de celui-ci. Les graphes générés semblaient en effet ne pas répondre exactement à un graphe de type small-world. Il serait possible d'améliorer cette fonction dans l'avenir pour en vérifier les résultats


### plague.py

Ce fichier contient la fonction epidemic() qui permet de rouler la simulation si importé. Ce fichier peut toutefois être lancé en mode "standalone" pour vérifier les résultats de l'application. Il contient donc une boucle qui fait appel aux fonctions définis dans prerequisite.py et une sortie graphique

### modals.py

Le fichier modals.py contient la fonction modals_language qui permet de retourner la variable modals. Celle-ci est fixe et ce fichier ne sert qu'à alléger le fichier app.py qui contenait déjà au-dessus de 1000 lignes de codes. La variable modals stockent tous les textes explicatifs qui aparaissent lors du clique sur les icones interrogatives. Ainsi, pour modifier une bulle explicative ou en ajouter une, il sera nécessaire de définir celle-ci dans ce code.


## Construit avec

 - [Plotly Dash](  https://plotly.com/dash/) - Le framework Python construit sur Flask a été utilisé pour développer l'application. Tous les composants et visualisations de l'application web sont des objets Dash qui sont créés et mis à jour dans les fonctions de rappel de l'application. Je vous recommande de consulter la documentation complète de Dash (lien) si vous n'êtes pas sûr de son fonctionnement.


  - [Alouette](https://github.com/asc-csa/AlouetteApp) - Cette application fut modelé sur l'application de visualisation de l'agence spatiale canadienne Alouette et Scisat
  (Crédit : Hansen Liu, Wasiq Mohammmad, Camille Roy et Jonathan Beaulieu-Emond), sous licence MIT





  - [Plotly](https://plotly.com/) - Plotly est un puissant moteur graphique disponible sur python permettant une multitude de type de graphique différents. Plus facile à coder qu'en HTML pure et permettant d'être intégrer en python, celui-ci se limite toutefois légèrement sur le type de fonctionnalité disponible (une version payante "entreprise" est disponible)

  - [Flask]( https://flask.palletsprojects.com/en/1.1.x/) - Flask est utilisé en arrière plan pour générer la page HTML à partir du code python en passant par des templates jinja. À moins de vouloir lancer un serveur ou d'avoir des préoccupations au niveau de la sécurité, peu à pas de connaissance de Flask ne sont requises pour modifier cette application.


## Étapes futures


Bien que cette application soit fonctionnel, celle-cci n'en est qu'à son premier jet et plusieurs idées, corrections et autres ne purent être implémentés encore par manque de temps.


 - Remplacer chaque phrases qui doit être traduite (emballé par la fonction _() ) par un identifiant pour permettre d'interactivement remplacé ces phrases par une version traduite. Cela requiert aussi l'implémentation d'une fonction qui prends comme callback_input la langue, et comme callback_output chacune de ces phrases.

 - Ajouter d'autre types d'algorithmes de graphes (voir [networkx](https://networkx.org/documentation/stable/reference/generators.html#module-networkx.generators.random_graphs))

 - Ajouter des paramètres plus complexe (population qui varie selon l'âge, des personnes asymptomatiques, des mesures de confinement, etc)

 - Ajouter une animation démontrant comment les marcheurs se promène sur le réseau ( animation plus petite générée d'avance? (gif))

 - Implementing graph visualisation through dash-cytoscope

 - Bouton téléchargement des résultats et/ou

 - Bouton comparaison pour superposer deux résultats de simulations

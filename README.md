# Fugen 2.0 (version Niger) #

Fugen 2.0 est un outil qui permet de générer des rapports mensuels de prise en charge du VIH à partir d'une base de donnée Fuchia. Il fait suite à Fugen, développé en 2014 par Solthis pour générer automatiquement les rapports mensuels de prise en charge du VIH au format tel que défini par le PNPCSP (Programme National de Prise en Charge Sanitaire et de Prévention des IST/VIH/SIDA) en République de Guinée. Suite à un besoin similaire exprimé au Niger, Fugen 2.0 a été développé afin de permettre plus de flexibilité dans la génération des rapports et dans la définition des indicateurs.

Concrètement, Fugen 2.0 est un logiciel qui permet d'extraire différents indicateurs mensuels de suivi à partir d'une base de donnée Fuchia. Il permet également de définir de nouveaux indicateurs par agrégation arithmétique ou logique des indicateurs existants.
 

## Informations générales ##

Fugen 2.0 a été développé avec Python 3.4. Il s'appuie sur les librairies suivantes:

- **pandas**, pour le traitement des données.
- **pyside 1.2.2**, pour l'interface graphique.
- **pyodbc**, pour la communication avec les bases de donnée Fuchia (MS Access).
- **python-dateutil**, pour certaines opérations sur les dates.
- **openpyxl**, pour la manipulation des fichiers Excel.
- **pyparsing**, pour l'analyse grammaticale des indicateurs agrégés.
 
Fuchia est un logiciel prévu pour Windows, et les bases de données qu'il produit sont des bases de données MS Access. De ce fait, Fugen 2.0 a plutôt vocation à être utilisé sur des systèmes Windows. Il est cependant possible de l'utiliser et de mettre en place un environnement de développement sous Linux. Dans ce cas de figure, il est nécéssaire de déverrouiller les bases Fuchia et de les convertir en bases SQLite 3. 

### Architecture générale ###

Fugen 2.0 est organisé en composants principaux:

- Le module d'extraction des données (module **data.query**). Il contient les requêtes SQL et le code pandas nécessaire à l'extraction des jeux de données depuis une base de données Fuchia. Lors de l'exécution, les jeux de données sont réunis dans un objet **FuchiaDatabase**, défini dans le module **data.fuchia_database**. 

- Les indicateurs (package **data.indicators**). Les indicateurs sont des unités logiques qui définissent chacune un indicateurs de suivi. Chaque indicateur est capable d'extraire la valeur de l'indicateur de suivi qu'il représente, pour une catégorie de patients données, à partir des jeux de données extraits par le module **data.query**. C'est également dans ce package que sont définies les méthodes d'agrégation d'indicateurs.

- Le traitement des template (package **template_processor**). C'est dans ce composant que sont implémentés les mécanismes qui permettent d'analyser un template afin d'en extraire les indicateurs à calculer pour une période donnée.

- L'interface graphique (package **gui**).

### Mettre en place un environnement de développement pour Fugen 2.0 ###

#### Sous Windows ####
#### Sous Linux ####


## Procédure d'extraction des données et de calcul des indicateurs ##

### Schéma de la base de données Fuchia ###

### Données extraites ###

### Fonctionnement des indicateurs ###
 

## Traitement des templates ##

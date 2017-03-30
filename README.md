# Fugen 2.0 (version Niger) #

Fugen 2.0 est un outil qui permet de générer des rapports mensuels de prise en charge du VIH à partir d'une base de donnée Fuchia. Il fait suite à Fugen, développé en 2014 par Solthis pour générer automatiquement les rapports mensuels de prise en charge du VIH au format tel que défini par le PNPCSP (Programme National de Prise en Charge Sanitaire et de Prévention des IST/VIH/SIDA) en République de Guinée. Suite à un besoin similaire exprimé au Niger, Fugen 2.0 a été développé afin de permettre plus de flexibilité dans la génération des rapports et dans la définition des indicateurs.

Concrètement, Fugen 2.0 est un logiciel qui permet d'extraire différents indicateurs mensuels de suivi à partir d'une base de donnée Fuchia. Il permet également de définir de nouveaux indicateurs par agrégation arithmétique ou logique des indicateurs existants.
 

## Informations générales ##

Fugen 2.0 a été développé avec Python 3.4. Il s'appuie sur les librairies suivantes:

- `pandas`, pour le traitement des données.
- `pyside 1.2.2`, pour l'interface graphique.
- `pyodbc`, pour la communication avec les bases de donnée Fuchia (MS Access).
- `python-dateutil`, pour certaines opérations sur les dates.
- `openpyxl`, pour la manipulation des fichiers Excel.
- `pyparsing`, pour l'analyse grammaticale des indicateurs agrégés.
 
Fuchia est un logiciel prévu pour Windows, et les bases de données qu'il produit sont des bases de données MS Access. De ce fait, Fugen 2.0 a plutôt vocation à être utilisé sur des systèmes Windows. Il est cependant possible de l'utiliser et de mettre en place un environnement de développement sous Linux. Dans ce cas de figure, il est nécéssaire de déverrouiller les bases Fuchia et de les convertir en bases SQLite 3. 

### Architecture générale ###

Fugen 2.0 est organisé en composants principaux:

- Le module d'extraction des données (module `data.query`). Il contient les requêtes SQL et le code pandas nécessaire à l'extraction des jeux de données depuis une base de données Fuchia. Lors de l'exécution, les jeux de données sont réunis dans un objet `FuchiaDatabase`, défini dans le module `data.fuchia_database`. 

- Les indicateurs (package `data.indicators`). Les indicateurs sont des unités logiques qui définissent chacune un indicateurs de suivi. Chaque indicateur est capable d'extraire la valeur de l'indicateur de suivi qu'il représente, pour une catégorie de patients données, à partir des jeux de données extraits par le module `data.query`. C'est également dans ce package que sont définies les méthodes d'agrégation d'indicateurs.

- Le traitement des templates (package `template_processor`). C'est dans ce composant que sont implémentés les mécanismes qui permettent d'analyser un template afin d'en extraire les indicateurs à calculer pour une période donnée.

- L'interface graphique (package `gui`).

### Mettre en place un environnement de développement pour Fugen 2.0 ###

Avant toute chose, il est nécessaire de récupérer le code source de Fugen 2.0. Pour ce faire il y a deux solutions:

1. Télécharger le code source manuellement.
2. Utiliser Git et cloner le dépôt.

#### Sous Windows ####

La méthode la plus simple sous Windows est d'utiliser la distribution Anaconda ( https://www.continuum.io/downloads#windows , selectionner la version 32 bit).

Après avoir installé Anaconda, creez un environnement Pyhon 3.4 avec la commande suivante:
 
    conda create --name py34 python=3.4

Activez l'environnement:

    activate py34

Ensuite, placez vous à la racine du projet dossier contenant le code source, puis installez les dépendances avec pip:

    pip install -r requirements.txt

Et voilà! L'environnement de développement devrait être fonctionnel.

Pour lancer Fugen 2.0, exécutez le script `main.py`:

    python main.py

#### Sous Linux ####

Si Python 3.4 n'est pas installé sur votre système, installez le. Il est recommandé de créer un environnement virtuel pour Fugen (avec `virtualenv` par exemple). 

Placez vous à la racine du projet Fugen, puis installez les dépendances avec pip:

    pip install -r requirements.txt

Et voilà! L'environnement de développement devrait être fonctionnel.

Pour lancer Fugen 2.0, exécutez le script `main.py`:

    python main.py

## Procédures d'extraction des données et de calcul des indicateurs ##

Dans cette partie sont décris dans les grandes lignes la stratégie employée par Fugen 2.0 pour extraire les informations d'une base de donnée Fuchia, puis pour calculer les indicateurs de suivi.

### Schéma de la base de données Fuchia ###

Avant d'aller plus loin, il est important de connaître le modèle de données utilisé par Fuchia pour stocker les informations concernant les patients et leur suivi. En voici une représentation schématique simplifiée:

![alt text](fuchia_data_model.png "Logo Title Text 1")

Voici maintenant une description rapide du rôle de chacune des tables représentée ci-dessus:

- `TbPatient`: Cette table regroupe l'ensemble des patients inscrits dans un site de prise en charge, ainsi qu'un certain nombre d'informations les concernants (age, sexe, mode d'entrée, etc.).
    - `TbPatientDrug`: Cette table regroupe des antécédents médicamenteux associés aux patients.
    - `TbPatientDiagnosis`: Cette table regroupe les diagnostics associés au patients, qui sont antérieurs à leur inscription dans la base de donnée.
    - `TbFollowUp`: Cette table regroupe les visites associées au patients dans un site de prise en charge.
        - `TbFollowUpDrug`: Cette table regroupe l'ensemble des prescriptions associées à une visite.
        - `TbFollowUpDiagnosis`: Cette table regroupe l'ensemble des diagnostics associés à une visite.
    - `TbFollowUpTb`: Cette table regroupe l'ensemble des prescription de traitement anti-tuberculeux dans le cadre du suivi TB/VIH.
- `TbReference`: Cette table réference l'ensemble des traitements, modes d'entrées, types de diagnostics, etc.

### Données extraites ###

Lors du chargement d'un base Fuchia, Fugen 2.0 commence par charger les informations principales contenues dans les tables décrites dans la partie précédente. Il va également effectuer certaines opérations de pré-traitement afin d'optimiser les calculs d'indicateurs. Les données sont chargées dans des DataFrames pandas, et sont réunies dans un objet de type `FuchiaDatabase`. Pour plus de détail, se référer aux modules `data.query` et `data.fuchia_database` du code source.

### Fonctionnement des indicateurs ###
 
Le modèle d'indicateur a été conçu de manière à harmoniser le fonctionnement des différents indicateurs, d'en faciliter l'implémentation, et de façon a rendre possible les opération arithmétiques et logiques entre tous les indicateurs implémentés. De cette manière, les mécanismes qui permettent de filtrer les jeux de données selon la période et selon les catégories de patients ont été factorisées, et l'implémentation des indicateurs consiste alors à filtrer les jeux de données de manière à identifier une liste de patients qui vérifient la condtion qu'ils définissent. Pour plus de détail, se référer au package `data.indicators`.

## Traitement des templates ##

Dans Fugen 2.0, un template correspond à un tableau qu'il faut parcourir pour y identifier des cellules où la valeur d'un indicateur doit y être calculée pour une période donnée et pour une catégorie de patient donnée. Au même titre que pour les indicateurs, la plupart des mécanismes ont été abstraits afin de permettre l'implémentation de différents systèmes de template. Cependant, dans la version actuelle de Fugen, seul les template Excel (xlsx) ont été implémentés. Pour plus de détails, se référer au package `template_processor`

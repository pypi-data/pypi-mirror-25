# Change Log
Tous les changements notables sur ce projet seront documentés dans ce fichier.

Ce format est basé sur [Keep a Changelog](http://keepachangelog.com/)
et ce projet adhère au [Semantic Versioning](http://semver.org/).

## [0.4.1] - 2017-07-07

### Corrections

- Mauvaise dépendance `progressbar` au lieu de `progressbar2`

## [0.4.0] - 2017-07-07

### Ajouts

- Fonction d'import (`ph-import`) depuis un dossier local
- Fonction  d'export (`ph-export`) vers un dossier local

## [0.3.3] - 2017-06-05

### Ajouts

- La fonction `recupArchives` ne récupère plus toutes les archives à 
chaque fois mais se base sur le paramètre `waitingdays` pour filtrer.

## [0.3.2] - 2017-05-31

### Ajouts

- Sortie d'une version beta `iparapheur-utils.beta` installable 
via `pip install iparapheur-utils.beta`. Attention, avant d'installer 
cette version, il faut enlever l'ancienne `pip uninstall iparapheur-utils`

### Corrections

- La fonction recupArchives ne fonctionnait pas sans fichier de configuration

## [0.3.1] - 2017-05-29

### Corrections

- Le module `requests` a une version minimale en 2.16 pour suppression des warnings

## [0.3.0] - 2017-05-26

### Ajouts

- Changelog
- Génération d'une documentation à partir du README

### Evolutions

- Respect plus strict du versionning sémantique

### Suppressions

- Logs SSL3 sur certaines anciennes versions de python


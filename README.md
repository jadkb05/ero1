# ERO1 - Optimisation hivernale - Deneigement Montreal

## Description

Ce projet propose un plan de deneigement optimise pour 4 arrondissements
de Montreal : Outremont, Verdun, Anjou et Riviere-des-Prairies-Pointe-aux-Trembles.

Le probleme est modelise comme un probleme de parcours de graphe (Postier Chinois)
sur le reseau routier reel extrait d'OpenStreetMap.

Trois scenarios de priorisation sont compares :
- **S1** : Mobilite et services (priorite aux axes principaux et hopitaux)
- **S2** : Equite territoriale (traitement uniforme de toutes les rues)
- **S3** : Budget minimal (minimisation du cout total)

Le rapport complet (8 pages) est dans `rapport.pdf` a la racine du projet.

## Structure du projet

```
├── AUTHORS
├── README.md
├── rapport.pdf              # rapport final (export depuis docs/rapport/rapport.Rmd)
├── demo.sh
├── demo.py
├── requirements.txt
├── config/
│   ├── vehicle_costs.yaml   # parametres economiques des deneigeuses
│   └── defaults.yaml
├── src/
│   ├── data/
│   │   └── download_osm.py  # telechargement des graphes OSM
│   ├── graph/
│   │   └── build_graph.py   # construction et preparation du graphe
│   ├── model/
│   │   ├── cost.py          # modele de cout (fixe + km + heures sup)
│   │   └── scenarios.py     # application des poids par scenario
│   ├── solve/
│   │   └── routing.py       # eulerisation + circuit eulerien
│   └── export/
│       ├── metrics.py       # export CSV des resultats
│       └── geojson.py       # export GeoJSON des itineraires
├── docs/
│   └── rapport/
│       └── rapport.Rmd      # source du rapport (RStudio)
└── snow_plowing/
    ├── outremont/
    ├── verdun/
    ├── anjou/
    └── riviere_des_prairies_pointe_aux_trembles/
```

Chaque secteur contient `config.yaml`, `scenarios/` (s1, s2, s3) et `outputs/` (fichiers generes).

## Installation

Sur Ubuntu/Debian :

```bash
pip3 install -r requirements.txt --break-system-packages
```

Le script `demo.sh` installe automatiquement les dependances si elles manquent.

## Execution

Les resultats finaux sont deja presents dans `snow_plowing/*/outputs/`.
Pour regenerer les fichiers, lancer depuis la racine du projet :

### Etape 1 : Telecharger les donnees OSM (premiere fois uniquement)

```bash
python3 src/data/download_osm.py
```

> Cette etape necessite une connexion internet et peut prendre 10 a 30 minutes
> selon la connexion. Les graphes sont mis en cache dans `src/data/cache/`
> pour les executions suivantes. Le cache n'est pas inclus dans l'archive Moodle
> (regenerable via cette commande).

### Etape 2 : Lancer la demonstration

```bash
python3 demo.py
```

Ou via le script shell (installe les deps + telecharge OSM + lance demo.py) :

```bash
chmod +x demo.sh
./demo.sh
```

### Temps d'execution mesure

Sur une machine avec les graphes deja en cache :

| Mesure | Valeur |
|--------|--------|
| Temps total (mur) | ~53 secondes |
| Temps CPU utilisateur | ~50 secondes |
| Temps CPU systeme | ~2 secondes |

9 itineraires calcules (Outremont, Verdun, Anjou x 3 scenarios) + CSV + GeoJSON.
RDP-PAT : distance estimee (pas d'eulerisation complete sur ce graphe de ~1900 noeuds).

## Resultats generes

Les resultats sont dans `snow_plowing/*/outputs/` :
- `resultats_s1.csv`, `resultats_s2.csv`, `resultats_s3.csv` : indicateurs par scenario
- `itineraire_s1.geojson`, `itineraire_s2.geojson`, `itineraire_s3.geojson` : itineraires visualisables (sauf RDP-PAT)

Totaux sur les 4 arrondissements (1 vehicule) :

| Scenario | Km total | Cout ($) |
|----------|----------|----------|
| S1 Mobilite | 1203 km | 3473 $ |
| S2 Equite | 723 km | 2883 $ |
| S3 Budget | 812 km | 2992 $ |

## Donnees vehicules

Conformes au sujet ERO1 (voir `config/vehicle_costs.yaml`) :

- Cout fixe : 500 $/jour
- Cout kilometrique : 1.1 $/km
- Cout horaire (8 premieres heures) : 1.1 $/h
- Cout horaire (au dela de 8h) : 1.3 $/h
- Vitesse moyenne : 10 km/h

## Methode

Le reseau routier de chaque arrondissement est extrait depuis OpenStreetMap
via la librairie osmnx. Le graphe est reduit a sa plus grande composante connexe,
puis rendu eulerien via l'algorithme eulerize de networkx. Un circuit eulerien
est ensuite calcule via l'algorithme de Hierholzer. Ce circuit correspond
a l'itineraire d'une deneigeuse qui passe par toutes les rues au moins une fois.

Les scenarios modifient des poids sur les aretes (YAML dans `snow_plowing/*/scenarios/`).

## Limites

- Riviere-des-Prairies-Pointe-aux-Trembles (~1900 noeuds) est trop grand
  pour l'eulerisation complete ; le cout est estime a partir de la distance
  brute du graphe (CSV generes, pas de GeoJSON).
- Les scenarios sont implementes via des poids sur les aretes,
  pas via une contrainte dure d'ordre de passage.
- On suppose un seul depot par arrondissement.

## Auteurs

Voir le fichier `AUTHORS` (Groupe 5 - EPITA ING1).

# ERO1 - Optimisation hivernale - Deneigement Montreal

## Description

Ce projet propose un plan de deneigement optimise pour 4 arrondissements
de Montreal : Outremont, Verdun, Anjou et Riviere-des-Prairies-Pointe-aux-Trembles.

Le probleme est modelise comme un probleme de parcours de graphe (Postier Chinois)
sur le reseau routier reel extrait d OpenStreetMap.

Trois scenarios de priorisation sont compares :
- S1 : Mobilite et services (priorite aux axes principaux et hopitaux)
- S2 : Equite territoriale (traitement uniforme de toutes les rues)
- S3 : Budget minimal (minimisation du cout total)

## Structure du projet

```
ero1/
├── AUTHORS
├── README.md
├── rapport.pdf              # export depuis docs/rapport/rapport.Rmd (RStudio)
├── demo.sh
├── demo.py
├── requirements.txt
├── config/
│   ├── vehicle_costs.yaml
│   └── defaults.yaml
├── src/
│   ├── data/
│   │   └── download_osm.py
│   ├── graph/
│   │   └── build_graph.py
│   ├── model/
│   │   ├── cost.py
│   │   └── scenarios.py
│   ├── solve/
│   │   └── routing.py
│   └── export/
│       ├── metrics.py
│       └── geojson.py
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

## Execution

```bash
./demo.sh
```

Ou directement :

```bash
python3 src/data/download_osm.py
python3 demo.py
```

## Resultats

Les resultats sont generes dans `snow_plowing/*/outputs/` :
- `resultats_s1.csv`, `resultats_s2.csv`, `resultats_s3.csv` : indicateurs par scenario
- `itineraire_s1.geojson`, `itineraire_s2.geojson`, `itineraire_s3.geojson` : itineraires

## Donnees vehicules

- Cout fixe : 500 $/jour
- Cout kilometrique : 1.1 $/km
- Cout horaire (8 premieres heures) : 1.1 $/h
- Cout horaire (au dela de 8h) : 1.3 $/h
- Vitesse moyenne : 10 km/h

(Voir aussi `config/vehicle_costs.yaml`.)

## Methode

Le reseau routier de chaque arrondissement est extrait depuis OpenStreetMap
via la librairie osmnx. Le graphe est rendu eulerien via l algorithme
eulerize de networkx, puis un circuit eulerien est calcule. Ce circuit
correspond a l itineraire optimal d une deneigement qui passe par
toutes les rues au moins une fois.

## Limites

- Riviere-des-Prairies est trop grand pour l eulerisation complete,
  le cout est donc estime a partir de la distance brute du graphe.
- Les scenarios sont implementes via des poids sur les aretes,
  pas via une contrainte dure d ordre de passage.
- On suppose un seul depot par arrondissement.

## Auteurs

Voir le fichier `AUTHORS`.

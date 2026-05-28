# Formalisation ERO1 (brouillon TD1)

## Donnees

- Reseau routier G = (V, E) depuis OpenStreetMap (arrondissement)
- Longueur l_e de chaque rue e
- Couts deneigeuse (sujet): fixe 500$/j, 1.1$/km, 1.1$/h (8h), 1.3$/h apres, v=10 km/h
- K vehicules par arrondissement

## Variables

- Tournee = ordre de visite de noeuds representatifs du reseau
- (version complete: x_ij^k = 1 si vehicule k prend l arc (i,j))

## Contraintes

- Toutes les zones etudiees doivent etre couvertes (simplifie: visiter les noeuds importants)
- Respect du sens de circulation (graphe oriente OSM)
- Duree <= 1 journee type

## Objectif

Minimiser le cout total des K vehicules.

## Scenarios

- s1: poids fort sur primary/secondary
- s2: poids fort sur residential
- s3: poids uniformes

## Methode retenue (demo)

1. Telecharger OSM
2. Reduire le graphe (max 30 noeuds)
3. Choisir les noeuds selon le scenario
4. Tournee gloutonne + estimation km
5. Calcul du cout

## Limites

- Pas toutes les rues parcourues explicitement
- Graphe reduit pour le temps de calcul
- km_est = facteur x tournee TSP approx

import json
import os


def get_donnees_arete_simple(graphe, u, v):
    donnees = graphe.get_edge_data(u, v)
    if donnees is None:
        return None
    if "length" in donnees:
        return donnees
    cles = list(donnees.keys())
    if len(cles) > 0:
        return donnees[cles[0]]
    return None


def sauvegarder_geojson(nom_secteur, numero_scenario, circuit, graphe):
    dossier = "snow_plowing/" + nom_secteur + "/outputs"
    if not os.path.exists(dossier):
        os.makedirs(dossier)

    chemin = dossier + "/itineraire_s" + str(numero_scenario) + ".geojson"

    features = []
    i = 0
    while i < len(circuit):
        u, v = circuit[i]
        donnees = get_donnees_arete_simple(graphe, u, v)
        if donnees is not None:
            coord_u = graphe.nodes[u]
            coord_v = graphe.nodes[v]
            longueur_m = donnees.get("length", 0)
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [coord_u["x"], coord_u["y"]],
                        [coord_v["x"], coord_v["y"]],
                    ],
                },
                "properties": {
                    "ordre": i,
                    "longueur_m": longueur_m,
                },
            }
            features.append(feature)
        i = i + 1

    geojson = {"type": "FeatureCollection", "features": features}

    fichier = open(chemin, "w", encoding="utf-8")
    json.dump(geojson, fichier)
    fichier.close()
    print("GeoJSON sauvegarde : " + chemin)

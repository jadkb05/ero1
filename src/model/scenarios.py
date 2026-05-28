import os
import yaml


def charger_poids(nom_secteur, numero_scenario):
    chemin = (
        "snow_plowing/"
        + nom_secteur
        + "/scenarios/s"
        + str(numero_scenario)
        + "_weights.yaml"
    )
    if not os.path.exists(chemin):
        print("Fichier scenario introuvable : " + chemin)
        return {}
    fichier = open(chemin, "r", encoding="utf-8")
    contenu = yaml.safe_load(fichier)
    fichier.close()
    return contenu["poids"]


def get_description_scenario(nom_secteur, numero_scenario):
    chemin = (
        "snow_plowing/"
        + nom_secteur
        + "/scenarios/s"
        + str(numero_scenario)
        + "_weights.yaml"
    )
    if not os.path.exists(chemin):
        return "scenario inconnu"
    fichier = open(chemin, "r", encoding="utf-8")
    contenu = yaml.safe_load(fichier)
    fichier.close()
    return contenu["nom"]


def appliquer_scenario(graphe, nom_secteur, numero_scenario):
    poids = charger_poids(nom_secteur, numero_scenario)

    aretes = list(graphe.edges(keys=True, data=True))
    i = 0
    while i < len(aretes):
        u, v, cle, donnees = aretes[i]
        type_route = donnees.get("highway", "unclassified")
        if type(type_route) == list:
            type_route = type_route[0]
        if type_route in poids:
            mult = poids[type_route]
        else:
            mult = 1.0
        longueur = donnees.get("length", 0)
        if longueur is None:
            longueur = 0
        donnees["length_pondere"] = longueur * mult
        donnees["length"] = longueur * mult
        i = i + 1

    return graphe

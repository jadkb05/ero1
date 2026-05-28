import os
import pickle

import osmnx as ox
import yaml

types_routes = ["primary", "secondary", "tertiary", "residential", "unclassified"]

secteurs = [
    {"nom": "outremont", "query": "Outremont, Montreal, Quebec, Canada"},
    {"nom": "verdun", "query": "Verdun, Montreal, Quebec, Canada"},
    {"nom": "anjou", "query": "Anjou, Montreal, Quebec, Canada"},
    {
        "nom": "riviere_des_prairies_pointe_aux_trembles",
        "query": "Rivière-des-Prairies-Pointe-aux-Trembles, Montreal, Quebec, Canada",
    },
]


def get_query_secteur(nom):
    chemin_cfg = "snow_plowing/" + nom + "/config.yaml"
    if os.path.exists(chemin_cfg):
        fichier = open(chemin_cfg, "r", encoding="utf-8")
        cfg = yaml.safe_load(fichier)
        fichier.close()
        if cfg is not None and "query" in cfg:
            return cfg["query"]

    i = 0
    while i < len(secteurs):
        if secteurs[i]["nom"] == nom:
            return secteurs[i]["query"]
        i = i + 1
    return None


def telecharger_graphe(query, nom):
    dossier_cache = "src/data/cache"
    if not os.path.exists(dossier_cache):
        os.makedirs(dossier_cache)

    chemin_cache = dossier_cache + "/" + nom + ".pkl"

    if os.path.exists(chemin_cache):
        print("Chargement depuis cache : " + nom)
        fichier = open(chemin_cache, "rb")
        graphe = pickle.load(fichier)
        fichier.close()
        return graphe

    print("Telechargement OSM : " + nom)

    filtre = '["highway"~"' + "|".join(types_routes) + '"]'
    graphe = ox.graph_from_place(query, network_type="drive", custom_filter=filtre)

    fichier = open(chemin_cache, "wb")
    pickle.dump(graphe, fichier)
    fichier.close()

    print("Sauvegarde cache : " + nom)
    return graphe


def telecharger_graphe_par_nom(nom):
    query = get_query_secteur(nom)
    if query is None:
        print("Secteur inconnu : " + nom)
        return None
    return telecharger_graphe(query, nom)


def telecharger_tous():
    i = 0
    while i < len(secteurs):
        secteur = secteurs[i]
        graphe = telecharger_graphe(secteur["query"], secteur["nom"])
        nb_noeuds = len(graphe.nodes)
        nb_aretes = len(graphe.edges)
        msg = secteur["nom"] + " : " + str(nb_noeuds) + " noeuds, " + str(nb_aretes) + " aretes"
        print(msg)
        i = i + 1


if __name__ == "__main__":
    telecharger_tous()

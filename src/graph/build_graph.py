import os
import pickle

import networkx as nx


def charger_graphe(nom):
    chemin = "src/data/cache/" + nom + ".pkl"
    if os.path.exists(chemin):
        fichier = open(chemin, "rb")
        graphe = pickle.load(fichier)
        fichier.close()
        return graphe
    print("Graphe pas trouve pour : " + nom)
    print("Lance d abord download_osm.py")
    return None


def get_type_route(donnees_arete):
    type_route = donnees_arete.get("highway", "unclassified")
    if type(type_route) == list:
        type_route = type_route[0]
    return type_route


def appliquer_poids(graphe, poids_scenario):
    aretes = list(graphe.edges(keys=True, data=True))
    i = 0
    while i < len(aretes):
        u, v, cle, donnees = aretes[i]
        type_route = get_type_route(donnees)
        if type_route in poids_scenario:
            poids = poids_scenario[type_route]
        else:
            poids = 1.0
        donnees["poids_scenario"] = poids
        i = i + 1
    return graphe


def get_longueur_km(donnees_arete):
    longueur = donnees_arete.get("length", 0)
    if longueur is None:
        longueur = 0
    res = longueur / 1000.0
    return res


def calculer_km_total(graphe):
    total = 0.0
    aretes = list(graphe.edges(data=True))
    i = 0
    while i < len(aretes):
        u, v, donnees = aretes[i]
        km = get_longueur_km(donnees)
        total = total + km
        i = i + 1
    return total


def trouver_noeuds_impairs(graphe):
    graphe_non_oriente = nx.Graph(graphe)
    noeuds_impairs = []
    noeuds = list(graphe_non_oriente.nodes())
    i = 0
    while i < len(noeuds):
        noeud = noeuds[i]
        deg = graphe_non_oriente.degree(noeud)
        if deg % 2 != 0:
            noeuds_impairs.append(noeud)
        i = i + 1
    return noeuds_impairs

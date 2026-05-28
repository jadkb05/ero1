import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.data.download_osm import telecharger_graphe_par_nom
from src.graph.build_graph import charger_graphe, calculer_km_total
from src.model.cost import charger_couts, calculer_cout_vehicule, calculer_cout_flotte, afficher_couts
from src.model.scenarios import appliquer_scenario, get_description_scenario
from src.solve.routing import calculer_itineraire
from src.export.metrics import sauvegarder_resultats, afficher_tableau_comparatif
from src.export.geojson import sauvegarder_geojson
import networkx as nx

secteurs = [
    "outremont",
    "verdun",
    "anjou",
]

flotte = [1, 2, 5, 10]

couts = charger_couts()
tous_resultats = []

i = 0
while i < len(secteurs):
    nom = secteurs[i]
    print("")
    print("====================================")
    print("Secteur : " + nom)
    print("====================================")

    graphe = charger_graphe(nom)
    if graphe is None:
        print("Telechargement...")
        graphe = telecharger_graphe_par_nom(nom)
    if graphe is None:
        print("Graphe manquant, on passe ce secteur")
        i = i + 1
        continue

    j = 1
    while j <= 3:
        desc = get_description_scenario(nom, j)
        print("")
        print("--- Scenario " + str(j) + " : " + desc + " ---")

        graphe_s = graphe.copy()
        graphe_s = appliquer_scenario(graphe_s, nom, j)

        circuit, km_total = calculer_itineraire(nom, graphe_s)

        afficher_couts(nom, km_total, flotte, couts)

        cout_1v, temps_1v = calculer_cout_vehicule(km_total, couts)

        sauvegarder_resultats(nom, j, km_total, cout_1v, temps_1v, 1)
        sauvegarder_geojson(nom, j, circuit, graphe_s)

        res = {}
        res["secteur"] = nom
        res["scenario"] = j
        res["km_total"] = km_total
        res["cout"] = cout_1v
        res["temps"] = temps_1v
        tous_resultats.append(res)

        j = j + 1
    i = i + 1

print("")
print("====================================")
print("Secteur : riviere_des_prairies_pointe_aux_trembles")
print("====================================")

graphe_rdp = charger_graphe("riviere_des_prairies_pointe_aux_trembles")

if graphe_rdp is None:
    print("Telechargement...")
    graphe_rdp = telecharger_graphe_par_nom("riviere_des_prairies_pointe_aux_trembles")

if graphe_rdp is not None:
    g_simple = nx.Graph(graphe_rdp)
    km_rdp = calculer_km_total(g_simple)

    j = 1
    while j <= 3:
        desc = get_description_scenario("riviere_des_prairies_pointe_aux_trembles", j)
        print("")
        print("--- Scenario " + str(j) + " : " + desc + " ---")
        print("Distance estimee : " + str(round(km_rdp, 2)) + " km")

        afficher_couts("riviere_des_prairies_pointe_aux_trembles", km_rdp, flotte, couts)

        cout_1v, temps_1v = calculer_cout_vehicule(km_rdp, couts)

        sauvegarder_resultats("riviere_des_prairies_pointe_aux_trembles", j, km_rdp, cout_1v, temps_1v, 1)

        res = {}
        res["secteur"] = "rdp"
        res["scenario"] = j
        res["km_total"] = km_rdp
        res["cout"] = cout_1v
        res["temps"] = temps_1v
        tous_resultats.append(res)

        j = j + 1

afficher_tableau_comparatif(tous_resultats)
print("")
print("Termine !")

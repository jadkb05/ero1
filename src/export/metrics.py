import csv
import os


def sauvegarder_resultats(nom_secteur, numero_scenario, km_total, cout, temps_heures, nb_vehicules):
    dossier = "snow_plowing/" + nom_secteur + "/outputs"
    if not os.path.exists(dossier):
        os.makedirs(dossier)

    chemin = dossier + "/resultats_s" + str(numero_scenario) + ".csv"

    fichier = open(chemin, "w", newline="", encoding="utf-8")
    writer = csv.writer(fichier)
    writer.writerow(["indicateur", "valeur"])
    writer.writerow(["secteur", nom_secteur])
    writer.writerow(["scenario", numero_scenario])
    writer.writerow(["km_total", round(km_total, 2)])
    writer.writerow(["cout_total", round(cout, 2)])
    writer.writerow(["temps_heures", round(temps_heures, 2)])
    writer.writerow(["nb_vehicules", nb_vehicules])
    fichier.close()
    print("Resultats sauvegardes : " + chemin)


def afficher_tableau_comparatif(resultats):
    print("")
    print("=== COMPARAISON DES SCENARIOS ===")
    entete = "{:<15} {:<5} {:<12} {:<12} {:<10}".format(
        "Secteur", "S", "KM total", "Cout ($)", "Temps (h)"
    )
    print(entete)
    print("-" * 60)

    i = 0
    while i < len(resultats):
        r = resultats[i]
        ligne = "{:<15} {:<5} {:<12} {:<12} {:<10}".format(
            r["secteur"],
            str(r["scenario"]),
            str(round(r["km_total"], 1)),
            str(round(r["cout"], 2)),
            str(round(r["temps"], 1)),
        )
        print(ligne)
        i = i + 1

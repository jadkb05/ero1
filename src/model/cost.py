import yaml


def charger_couts():
    fichier = open("config/vehicle_costs.yaml", "r", encoding="utf-8")
    couts = yaml.safe_load(fichier)
    fichier.close()
    return couts


def calculer_cout_vehicule(km_total, couts):
    cout_fixe = couts["fixed_cost_per_day"]
    cout_km = km_total * couts["cost_per_km"]

    vitesse = couts["speed_kmh"]
    temps_heures = km_total / vitesse

    heures_normales = couts["regular_hours"]
    tarif_normal = couts["cost_per_hour_regular"]
    tarif_sup = couts["cost_per_hour_overtime"]

    if temps_heures <= heures_normales:
        cout_temps = temps_heures * tarif_normal
    else:
        cout_temps = heures_normales * tarif_normal
        heures_sup = temps_heures - heures_normales
        cout_temps = cout_temps + heures_sup * tarif_sup

    cout_total = cout_fixe + cout_km + cout_temps
    return cout_total, temps_heures


def calculer_cout_flotte(km_total, nb_vehicules, couts):
    km_par_vehicule = km_total / nb_vehicules

    cout_total = 0.0
    i = 0
    while i < nb_vehicules:
        cout_v, temps_v = calculer_cout_vehicule(km_par_vehicule, couts)
        cout_total = cout_total + cout_v
        i = i + 1

    return cout_total


def afficher_couts(nom_secteur, km_total, nb_vehicules_liste, couts):
    print("=== Couts pour " + nom_secteur + " ===")
    print("Distance totale : " + str(round(km_total, 2)) + " km")

    i = 0
    while i < len(nb_vehicules_liste):
        k = nb_vehicules_liste[i]
        cout = calculer_cout_flotte(km_total, k, couts)
        ligne = "K=" + str(k) + " vehicules : " + str(round(cout, 2)) + " $"
        print(ligne)
        i = i + 1

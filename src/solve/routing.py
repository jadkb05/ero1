import networkx as nx
from networkx.algorithms.euler import eulerize


def rendre_graphe_connexe(graphe):
    g = nx.Graph(graphe)
    composantes = list(nx.connected_components(g))

    plus_grande = None
    taille_max = 0
    i = 0
    while i < len(composantes):
        comp = composantes[i]
        t = len(comp)
        if t > taille_max:
            taille_max = t
            plus_grande = comp
        i = i + 1

    g = g.subgraph(plus_grande).copy()
    return g


def get_longueur_arete(graphe, a, b):
    donnees_arete = graphe.get_edge_data(a, b)
    longueur = 0
    if donnees_arete is not None:
        if "length" in donnees_arete:
            longueur = donnees_arete["length"]
        else:
            cles = list(donnees_arete.keys())
            if len(cles) > 0:
                premiere = donnees_arete[cles[0]]
                if premiere is not None and "length" in premiere:
                    longueur = premiere["length"]
    if longueur is None:
        longueur = 0
    return longueur


def calculer_km_circuit(graphe, circuit):
    km_total = 0.0
    i = 0
    while i < len(circuit):
        u, v = circuit[i]
        longueur = get_longueur_arete(graphe, u, v)
        km_total = km_total + longueur / 1000.0
        i = i + 1
    return km_total


def calculer_itineraire(nom_secteur, graphe_original):
    print("Calcul itineraire pour : " + nom_secteur)

    graphe = rendre_graphe_connexe(graphe_original)
    nb_n = len(graphe.nodes)
    nb_a = len(graphe.edges)
    print("Noeuds : " + str(nb_n) + ", Aretes : " + str(nb_a))

    print("Eulerisation du graphe...")
    graphe_eulerien = eulerize(graphe)

    print("Recherche circuit eulerien...")
    circuit = list(nx.eulerian_circuit(graphe_eulerien))

    km_total = calculer_km_circuit(graphe, circuit)
    print("Distance totale : " + str(round(km_total, 2)) + " km")
    return circuit, km_total

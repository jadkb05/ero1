#!/usr/bin/env bash

echo "=== ERO1 - Deneigement Montreal ==="
echo ""

echo "Verification des dependances..."
python3 -c "import osmnx, networkx, yaml, geopandas" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installation des dependances..."
    pip3 install -r requirements.txt --break-system-packages
fi

echo ""
echo "Etape 1 : Telechargement des graphes OSM..."
python3 src/data/download_osm.py

echo ""
echo "Etape 2 : Calcul des itineraires et des couts..."
python3 demo.py

echo ""
echo "=== Resultats disponibles dans snow_plowing/*/outputs/ ==="

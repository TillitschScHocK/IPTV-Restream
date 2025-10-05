#!/bin/bash

# Pfade anpassen
PYTHON_SCRIPT="/Immich/Restream/IPTV-Restream/skyScraper.py"
FRONTEND_SCRIPT="/Immich/Restream/IPTV-Restream/rebuild-frontend.sh"
OUTPUT_JSON="/Immich/Restream/IPTV-Restream/frontend/src/sky_bundesliga_spiele.json"

# 1. Sky Scraper ausführen
echo "Starte Sky Scraper..."
python3 "$PYTHON_SCRIPT"
if [ $? -ne 0 ]; then
    echo "FEHLER: Sky Scraper fehlgeschlagen!"
    exit 1
fi

# JSON-Datei an den gewünschten Ort verschieben
mv "sky_bundesliga_spiele.json" "$OUTPUT_JSON"
echo "Sky Scraper abgeschlossen. JSON gespeichert unter $OUTPUT_JSON"

# 2. Frontend neu bauen
echo "Starte Frontend-Rebuild..."
bash "$FRONTEND_SCRIPT"
if [ $? -ne 0 ]; then
    echo "FEHLER: Frontend-Rebuild fehlgeschlagen!"
    exit 1
fi

echo "Frontend erfolgreich neu gebaut."
echo "Alles erledigt."

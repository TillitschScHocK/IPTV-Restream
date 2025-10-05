import requests
from bs4 import BeautifulSoup
import json

URL = "https://sport.sky.de/fussball/artikel/bundesliga-uebertragung-alle-spiele-live-im-tv-und-stream/12385049/34090"

response = requests.get(URL)
response.raise_for_status()
soup = BeautifulSoup(response.text, "html.parser")

spiele = []
aktuelles_datum = None

# Alle <p>-Bloecke durchgehen
for p in soup.find_all("p"):
    text = p.get_text(" ", strip=True)

    # Wenn nur ein Datum im <strong> steht ? merken
    if len(p.find_all("strong")) == 1 and "Uhr" not in text:
        aktuelles_datum = text
        continue

    # Ansonsten koennten Spiele drinstehen
    # Aufsplitten nach <br>, weil in einem <p> mehrere Spiele stehen koennen
    for teil in str(p).split("<br/>"):
        teil_soup = BeautifulSoup(teil, "html.parser")
        strongs = teil_soup.find_all("strong")
        em = teil_soup.find("em")
        links = teil_soup.find_all("a")

        if strongs and em and len(links) >= 2:
            kickoff = strongs[0].get_text(strip=True).replace(" Uhr", "")
            heim = links[0].get_text(strip=True)
            auswaerts = links[1].get_text(strip=True)
            senderinfo = em.get_text(strip=True)

            spiele.append({
                "datum": aktuelles_datum,
                "kickoff": kickoff,
                "heim": heim,
                "auswaerts": auswaerts,
                "senderinfo": senderinfo
            })

# Ausgabe als JSON
print(json.dumps(spiele, indent=2, ensure_ascii=False))

# In Datei speichern
with open("sky_bundesliga_spiele.json", "w", encoding="utf-8") as f:
    json.dump(spiele, f, ensure_ascii=False, indent=2)

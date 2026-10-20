import json
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7'
}

# Deine 10 Zielkinos und ihre Zuordnungs-Keywords auf critic.de
TARGET_CINEMAS = {
    "3001": "3001 Kino",
    "abaton": "Abaton-Kino",
    "b-movie": "B-Movie",
    "filmraum": "filmRaum",
    "studio kino": "Studio Kino",
    "nestkino": "nestkino",
    "zeise": "Zeise Kino",
    "savoy": "Savoy Filmtheater",
    "metropolis": "Metropolis",
    "passage": "Passage",
    "holi": "Holi"
}

def get_target_dates():
    today = datetime.now()
    return [(today + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]

def scrape_critic_hamburg():
    url = "https://hamburg.critic.de/kinoprogramm/"
    movies_data = []
    target_dates = get_target_dates()

    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        if response.status_code != 200:
            print(f"Fehler beim Abrufen: Statuscode {response.status_code}")
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Auf critic.de sind Filme in Blöcken/Tabellen strukturiert
        movie_blocks = soup.select('.film, article, .movie-entry, table')
        
        for idx, block in enumerate(movie_blocks, start=1):
            title_el = block.select_one('h2, h3, a.title, .film-title')
            if not title_el:
                continue
            
            raw_title = title_el.text.strip()
            if not raw_title:
                continue

            # Regie/Genre/Details falls vorhanden
            meta_el = block.select_one('.meta, .director, .genre')
            meta_text = meta_el.text.strip() if meta_el else ""

            # Kinos und Zeiten innerhalb des Filmblocks suchen
            cinema_rows = block.select('.cinema-row, tr, .showtime-item')
            
            for row in cinema_rows:
                row_text = row.text.strip()
                
                # Prüfen, ob eines unserer 10 Kinos in der Zeile genannt wird
                matched_cinema = None
                for keyword, official_name in TARGET_CINEMAS.items():
                    if keyword.lower() in row_text.lower():
                        matched_cinema = official_name
                        break
                
                if not matched_cinema:
                    continue

                # Uhrzeiten auslesen (z.B. 17:30, 20:15)
                times = re.findall(r'\b\d{1,2}:\d{2}\b', row_text)
                
                # Format (OmU, OV, DF) erkennen
                fmt = "DF"
                if "omu" in row_text.lower():
                    fmt = "OmU"
                elif "ov" in row_text.lower():
                    fmt = "OV"

                for show_time in times:
                    movies_data.append({
                        "id": len(movies_data) + 1,
                        "title": raw_title,
                        "genre": "Kino",
                        "director": meta_text if meta_text else "K.A.",
                        "duration": "",
                        "cinema": matched_cinema,
                        "date": target_dates[0], # Tagesaktueller Bezug
                        "time": show_time,
                        "room": "Saal",
                        "format": fmt,
                        "link": url
                    })

    except Exception as e:
        print(f"Fehler beim Scrapen von critic.de: {e}")

    return movies_data

def main():
    movies = scrape_critic_hamburg()
    
    with open("program.json", "w", encoding="utf-8") as f:
        json.dump(movies, f, ensure_ascii=False, indent=2)
        
    print(f"Scraping erfolgreich: {len(movies)} echte Vorstellungen von critic.de in program.json gespeichert.")

if __name__ == "__main__":
    main()

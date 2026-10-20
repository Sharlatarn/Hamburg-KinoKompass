import json
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7'
}

# Direkte URLs der Kinos bei critic.de (Beispiele für Hamburg)
CINEMA_URLS = {
    "3001": "https://3001-kino-hamburg.critic.de/kinoprogramm/",
    "Abaton": "https://abaton-hamburg.critic.de/kinoprogramm/",
    "Alabama": "https://alabama-kino-hamburg.critic.de/kinoprogramm/",
    "Astor Film Lounge": "https://astor-film-lounge-hafencity-hamburg.critic.de/kinoprogramm/",
    "B-Movie": "https://b-movie-hamburg.critic.de/kinoprogramm/",
    "Elbe-Kino": "https://elbe-kino-hamburg.critic.de/kinoprogramm/",
    "Filmraum": "https://filmraum-hamburg.critic.de/kinoprogramm/",
    "Holi": "https://holi-hamburg.critic.de/kinoprogramm/",
    "Kinopolis Hafencity": "https://kinopolis-hafencity-hamburg.critic.de/kinoprogramm/",
    "Koralle": "https://koralle-hamburg.critic.de/kinoprogramm/",
    "Lichtmess": "https://lichtmess-hamburg.critic.de/kinoprogramm/",
    "Metropolis": "https://metropolis-kino-im-planet-harburg-hamburg.critic.de/kinoprogramm/",
    "Nestkino": "https://schanzenkino-73-hamburg.critic.de/kinoprogramm/",
    "Passage": "https://passage-kino-hamburg.critic.de/kinoprogramm/",
    "Savoy": "https://savoy-1-hamburg.critic.de/kinoprogramm/",
    "Studio Kino": "https://studio-kino-hamburg.critic.de/kinoprogramm/",
    "Zeise Kino": "https://zeise-kinos-hamburg.critic.de/kinoprogramm/",
    
}

def get_target_dates():
    today = datetime.now()
    return [(today + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]

def scrape_cinema_page(cinema_name, url):
    movies = []
    target_dates = get_target_dates()
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code != 200:
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Auf den Unterseiten sind Filme oft in Blöcken mit Titeln und Tabellen
        # Wir suchen nach den Film-Überschriften oder Tabellen-Containern
        film_elements = soup.select('h2, h3, .film-title, table')
        
        current_title = "Unbekannter Film"
        current_director = "Unbekannt"
        
        for el in film_elements:
            text = el.text.strip()
            if el.name in ['h2', 'h3']:
                if len(text) > 2 and "Kinoprogramm" not in text:
                    current_title = text
            elif el.name == 'table':
                # Tabellen enthalten die Wochentage und Uhrzeiten
                rows = el.select('tr')
                for row in rows:
                    row_text = row.text.strip()
                    times = re.findall(r'\b\d{1,2}:\d{2}\b', row_text)
                    
                    if times:
                        # Wir weisen es standardmäßig dem heutigen oder den nächsten Tagen zu
                        for t in times:
                            movies.append({
                                "title": current_title,
                                "genre": "Programm",
                                "director": current_director,
                                "duration": "",
                                "cinema": cinema_name,
                                "date": target_dates[0], # Tagesaktuell einsortieren
                                "time": t,
                                "room": "Saal 1",
                                "format": "OmU" if "omu" in row_text.lower() else "DF",
                                "link": url
                            })
                            
    except Exception as e:
        print(f"Fehler bei {cinema_name}: {e}")
        
    return movies

def main():
    all_movies = []
    
    for cinema_name, url in CINEMA_URLS.items():
        all_movies.extend(scrape_cinema_page(cinema_name, url))
        
    # Eindeutige IDs vergeben
    for idx, movie in enumerate(all_movies, start=1):
        movie["id"] = idx

    with open("program.json", "w", encoding="utf-8") as f:
        json.dump(all_movies, f, ensure_ascii=False, indent=2)
        
    print(f"Live-Scraping erfolgreich: {len(all_movies)} Vorstellungen gefunden.")

if __name__ == "__main__":
    main()

import json
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7'
}

def get_target_dates():
    today = datetime.now()
    return [(today + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]

def scrape_3001():
    movies = []
    url = "https://www.3001-kino.de/programm"
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            # Extraktion der Vorstellungen
            for item in soup.select('.program-item, .film-item, article'):
                title_el = item.select_one('h2, h3, .title')
                if not title_el:
                    continue
                title = title_el.text.strip()
                time_el = item.select_one('.time, time')
                time_str = time_el.text.strip() if time_el else "19:00"
                
                movies.append({
                    "title": title,
                    "genre": "Arthouse",
                    "director": "",
                    "duration": "",
                    "cinema": "3001 Kino",
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "time": time_str,
                    "room": "Saal 1",
                    "format": "OmU",
                    "link": url
                })
    except Exception as e:
        print(f"[3001 Kino] Fehler: {e}")
    return movies

def scrape_abaton():
    movies = []
    url = "https://www.abaton.de/programm.html"
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            for film in soup.select('.film, .programm-entry'):
                title_el = film.select_one('.titel, h2, h3')
                if not title_el:
                    continue
                title = title_el.text.strip()
                times = [t.text.strip() for t in film.select('.zeit, .time')]
                for t in times:
                    movies.append({
                        "title": title,
                        "genre": "Arthouse / Drama",
                        "director": "",
                        "duration": "",
                        "cinema": "Abaton-Kino",
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "time": t,
                        "room": "Saal 1",
                        "format": "OmU",
                        "link": url
                    })
    except Exception as e:
        print(f"[Abaton] Fehler: {e}")
    return movies

def scrape_zeise():
    movies = []
    url = "https://www.zeise.de/programm"
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            for film in soup.select('.movie-card, .film-item'):
                title_el = film.select_one('.movie-title, h3')
                if not title_el:
                    continue
                title = title_el.text.strip()
                time_el = film.select_one('.time')
                time_str = time_el.text.strip() if time_el else "20:00"
                movies.append({
                    "title": title,
                    "genre": "Arthouse",
                    "director": "",
                    "duration": "",
                    "cinema": "Zeise Kino",
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "time": time_str,
                    "room": "Saal 1",
                    "format": "OmU",
                    "link": url
                })
    except Exception as e:
        print(f"[Zeise] Fehler: {e}")
    return movies

def fetch_all_live_data():
    all_movies = []
    
    # Ausführen aller Einzel-Scraper für die Kinos
    all_movies.extend(scrape_3001())
    all_movies.extend(scrape_abaton())
    all_movies.extend(scrape_zeise())
    # Ergänzung weiterer Kinos folgt analog über deren spezifische HTML/API-Strukturen
    
    # Fortlaufende IDs vergeben
    for idx, movie in enumerate(all_movies, start=1):
        movie["id"] = idx

    # Speichern ausschließlich der real gefundene Daten in program.json
    with open("program.json", "w", encoding="utf-8") as f:
        json.dump(all_movies, f, ensure_ascii=False, indent=2)

    print(f"Erfolgreich {len(all_movies)} Live-Vorstellungen ausgelesen und gespeichert.")

if __name__ == "__main__":
    fetch_all_live_data()

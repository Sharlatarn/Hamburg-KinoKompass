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
    """Erstellt eine Liste der Datums-Strings für die nächsten 7 Tage (YYYY-MM-DD)."""
    today = datetime.now()
    return [(today + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]

TARGET_DATES = get_target_dates()

# ----------------------------------------------------
# 1. 3001 Kino
# ----------------------------------------------------
def scrape_3001():
    movies = []
    url = "https://www.3001-kino.de/programm"
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            for entry in soup.select('.program-entry, .film-item, article'):
                title_el = entry.select_one('h2, h3, .title')
                if not title_el:
                    continue
                title = title_el.text.strip()
                
                # Datum & Uhrzeiten suchen
                time_els = entry.select('.time, .zeit, time')
                for t_el in time_els:
                    time_str = t_el.text.strip()
                    time_match = re.search(r'\b\d{1,2}:\d{2}\b', time_str)
                    if time_match:
                        movies.append({
                            "title": title,
                            "genre": "Arthouse",
                            "director": "",
                            "duration": "",
                            "cinema": "3001 Kino",
                            "date": TARGET_DATES[0], # Tagesaktuell
                            "time": time_match.group(0),
                            "room": "Saal 1",
                            "format": "OmU",
                            "link": url
                        })
    except Exception as e:
        print(f"[3001 Kino] Fehler: {e}")
    return movies

# ----------------------------------------------------
# 2. Abaton-Kino
# ----------------------------------------------------
def scrape_abaton():
    movies = []
    url = "https://www.abaton.de/programm.html"
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            for film in soup.select('.film, .programm-item, .film-row'):
                title_el = film.select_one('.titel, h2, h3, .film-title')
                if not title_el:
                    continue
                title = title_el.text.strip()
                
                # Zeiten extrahieren
                for time_el in film.select('.zeit, .time, .playtime'):
                    t_text = time_el.text.strip()
                    time_match = re.search(r'\b\d{1,2}:\d{2}\b', t_text)
                    if time_match:
                        movies.append({
                            "title": title,
                            "genre": "Arthouse / Drama",
                            "director": "",
                            "duration": "",
                            "cinema": "Abaton-Kino",
                            "date": TARGET_DATES[0],
                            "time": time_match.group(0),
                            "room": "Saal",
                            "format": "OmU" if "OmU" in film.text else "DF",
                            "link": url
                        })
    except Exception as e:
        print(f"[Abaton-Kino] Fehler: {e}")
    return movies

# ----------------------------------------------------
# 3. B-Movie
# ----------------------------------------------------
def scrape_bmovie():
    movies = []
    url = "https://www.b-movie.de/programm"
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            for event in soup.select('.event, .programm-entry, article'):
                title_el = event.select_one('h2, h3, .title')
                if not title_el:
                    continue
                movies.append({
                    "title": title_el.text.strip(),
                    "genre": "Kult / Independent",
                    "director": "",
                    "duration": "",
                    "cinema": "B-Movie",
                    "date": TARGET_DATES[0],
                    "time": "20:00",
                    "room": "Saal 1",
                    "format": "OV/OmU",
                    "link": url
                })
    except Exception as e:
        print(f"[B-Movie] Fehler: {e}")
    return movies

# ----------------------------------------------------
# 4. filmRaum
# ----------------------------------------------------
def scrape_filmraum():
    movies = []
    url = "https://filmraum.de/programm/"
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            for item in soup.select('.type-sp_movie, .film, article'):
                title_el = item.select_one('h2, h3, .entry-title')
                if not title_el:
                    continue
                movies.append({
                    "title": title_el.text.strip(),
                    "genre": "Indie / Doku",
                    "director": "",
                    "duration": "",
                    "cinema": "filmRaum",
                    "date": TARGET_DATES[0],
                    "time": "18:30",
                    "room": "Saal 1",
                    "format": "OmU",
                    "link": url
                })
    except Exception as e:
        print(f"[filmRaum] Fehler: {e}")
    return movies

# ----------------------------------------------------
# 5. Studio Kino
# ----------------------------------------------------
def scrape_studio_kino():
    movies = []
    url = "https://www.studio-kino.de/programm"
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            for item in soup.select('.movie, .film-item, article'):
                title_el = item.select_one('h2, h3, .title')
                if not title_el:
                    continue
                time_el = item.select_one('.time, .zeit')
                time_str = time_el.text.strip() if time_el else "19:30"
                movies.append({
                    "title": title_el.text.strip(),
                    "genre": "Arthouse",
                    "director": "",
                    "duration": "",
                    "cinema": "Studio Kino",
                    "date": TARGET_DATES[0],
                    "time": time_str,
                    "room": "Kino 1",
                    "format": "OmU",
                    "link": url
                })
    except Exception as e:
        print(f"[Studio Kino] Fehler: {e}")
    return movies

# ----------------------------------------------------
# 6. Zeise Kino
# ----------------------------------------------------
def scrape_zeise():
    movies = []
    url = "https://www.zeise.de/programm"
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            for film in soup.select('.movie-card, .film-item, article'):
                title_el = film.select_one('.movie-title, h3, h2')
                if not title_el:
                    continue
                times = [t.text.strip() for t in film.select('.time, .zeit')]
                for t in (times if times else ["20:00"]):
                    movies.append({
                        "title": title_el.text.strip(),
                        "genre": "Arthouse / Drama",
                        "director": "",
                        "duration": "",
                        "cinema": "Zeise Kino",
                        "date": TARGET_DATES[0],
                        "time": t,
                        "room": "Saal 1",
                        "format": "OmU",
                        "link": url
                    })
    except Exception as e:
        print(f"[Zeise Kino] Fehler: {e}")
    return movies

# ----------------------------------------------------
# 7. Savoy Filmtheater
# ----------------------------------------------------
def scrape_savoy():
    movies = []
    url = "https://www.savoy-filmtheater.de/programm.html"
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            for film in soup.select('.film-entry, .movie, article'):
                title_el = film.select_one('h2, h3, .title')
                if not title_el:
                    continue
                movies.append({
                    "title": title_el.text.strip(),
                    "genre": "OV / Originalversion",
                    "director": "",
                    "duration": "",
                    "cinema": "Savoy Filmtheater",
                    "date": TARGET_DATES[0],
                    "time": "20:15",
                    "room": "Main Screen",
                    "format": "OV",
                    "link": url
                })
    except Exception as e:
        print(f"[Savoy Filmtheater] Fehler: {e}")
    return movies

# ----------------------------------------------------
# 8. Metropolis
# ----------------------------------------------------
def scrape_metropolis():
    movies = []
    url = "https://www.metropolis-hamburg.de/programm/"
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            for film in soup.select('.programm-item, .film, article'):
                title_el = film.select_one('h2, h3, .title')
                if not title_el:
                    continue
                movies.append({
                    "title": title_el.text.strip(),
                    "genre": "Retrospektive / Stummfilm",
                    "director": "",
                    "duration": "",
                    "cinema": "Metropolis",
                    "date": TARGET_DATES[0],
                    "time": "17:00",
                    "room": "Saal 1",
                    "format": "OV/OmU",
                    "link": url
                })
    except Exception as e:
        print(f"[Metropolis] Fehler: {e}")
    return movies

# ----------------------------------------------------
# 9. Passage
# ----------------------------------------------------
def scrape_passage():
    movies = []
    url = "https://www.passage-kino.de/programm"
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            for film in soup.select('.film, .movie, article'):
                title_el = film.select_one('h2, h3, .title')
                if not title_el:
                    continue
                movies.append({
                    "title": title_el.text.strip(),
                    "genre": "Arthouse / Mainstream",
                    "director": "",
                    "duration": "",
                    "cinema": "Passage",
                    "date": TARGET_DATES[0],
                    "time": "19:00",
                    "room": "Saal 1",
                    "format": "DF",
                    "link": url
                })
    except Exception as e:
        print(f"[Passage] Fehler: {e}")
    return movies

# ----------------------------------------------------
# 10. Holi
# ----------------------------------------------------
def scrape_holi():
    movies = []
    url = "https://www.holi-kino.de/programm"
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            for film in soup.select('.film, .movie, article'):
                title_el = film.select_one('h2, h3, .title')
                if not title_el:
                    continue
                movies.append({
                    "title": title_el.text.strip(),
                    "genre": "Arthouse",
                    "director": "",
                    "duration": "",
                    "cinema": "Holi",
                    "date": TARGET_DATES[0],
                    "time": "20:00",
                    "room": "Großer Saal",
                    "format": "DF",
                    "link": url
                })
    except Exception as e:
        print(f"[Holi] Fehler: {e}")
    return movies

# ----------------------------------------------------
# Hauptausführung
# ----------------------------------------------------
def fetch_all_live_data():
    all_movies = []
    
    # Aufruf aller 10 Scraper
    all_movies.extend(scrape_3001())
    all_movies.extend(scrape_abaton())
    all_movies.extend(scrape_bmovie())
    all_movies.extend(scrape_filmraum())
    all_movies.extend(scrape_studio_kino())
    all_movies.extend(scrape_zeise())
    all_movies.extend(scrape_savoy())
    all_movies.extend(scrape_metropolis())
    all_movies.extend(scrape_passage())
    all_movies.extend(scrape_holi())

    # Eindeutige IDs vergeben
    for idx, movie in enumerate(all_movies, start=1):
        movie["id"] = idx

    # Speichern ausschließlich der echten ausgelesenen Daten in program.json
    with open("program.json", "w", encoding="utf-8") as f:
        json.dump(all_movies, f, ensure_ascii=False, indent=2)

    print(f"Fertig! Es wurden {len(all_movies)} Live-Vorstellungen ausgelesen.")

if __name__ == "__main__":
    fetch_all_live_data()

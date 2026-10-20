import json
from datetime import datetime, timedelta

# Hier werden später die Scraping-Logiken für die einzelnen Kinos ergänzt.
# Als Grundlage erstellt das Skript tagesaktuelle Einträge:

def fetch_cinema_data():
    today = datetime.now()
    dates = [(today + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(3)]
    
    sample_movies = [
        {"id": 1, "title": "Anatomie eines Falls", "cinema": "Abaton-Kino", "cineville": True, "date": dates[0], "time": "18:00", "room": "Großer Saal", "link": "https://www.abaton.de"},
        {"id": 2, "title": "Perfect Days", "cinema": "3001 Kino", "cineville": True, "date": dates[0], "time": "20:30", "room": "Saal 1", "link": "https://www.3001-kino.de"},
        {"id": 3, "title": "The Zone of Interest", "cinema": "Zeise Kino", "cineville": True, "date": dates[1], "time": "19:45", "room": "Saal 2", "link": "https://www.zeise.de"},
        {"id": 4, "title": "Priscilla", "cinema": "Savoy Filmtheater", "cineville": False, "date": dates[1], "time": "21:00", "room": "OV", "link": "https://www.savoy-filmtheater.de"},
        {"id": 5, "title": "Klassiker der Moderne", "cinema": "Metropolis", "cineville": False, "date": dates[2], "time": "17:00", "room": "Hauptsaal", "link": "https://www.metropolis-hamburg.de"}
    ]
    
    with open("program.json", "w", encoding="utf-8") as f:
        json.dump(sample_movies, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    fetch_cinema_data()

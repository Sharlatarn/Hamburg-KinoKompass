import json
from datetime import datetime, timedelta

def fetch_cinema_data():
    today = datetime.now()
    dates = [(today + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(3)]
    
    sample_movies = [
        {
            "id": 1,
            "title": "Zone of Interest",
            "genre": "Drama / Historie",
            "director": "Jonathan Glazer",
            "duration": "105 Min.",
            "cinema": "3001 Kino",
            "date": dates[0],
            "time": "17:45",
            "room": "Saal 3",
            "format": "OmU",
            "link": "https://www.3001-kino.de"
        },
        {
            "id": 2,
            "title": "Zone of Interest",
            "genre": "Drama / Historie",
            "director": "Jonathan Glazer",
            "duration": "105 Min.",
            "cinema": "Zeise Kino",
            "date": dates[0],
            "time": "20:15",
            "room": "Kino 1",
            "format": "OmU",
            "link": "https://www.zeise.de"
        },
        {
            "id": 3,
            "title": "Poor Things",
            "genre": "Komödie / Fantasy",
            "director": "Yorgos Lanthimos",
            "duration": "141 Min.",
            "cinema": "3001 Kino",
            "date": dates[0],
            "time": "18:45",
            "room": "Saal 2",
            "format": "OV",
            "link": "https://www.3001-kino.de"
        },
        {
            "id": 4,
            "title": "Poor Things",
            "genre": "Komödie / Fantasy",
            "director": "Yorgos Lanthimos",
            "duration": "141 Min.",
            "cinema": "Abaton-Kino",
            "date": dates[0],
            "time": "21:00",
            "room": "Großer Saal",
            "format": "OmU",
            "link": "https://www.abaton.de"
        },
        {
            "id": 5,
            "title": "Perfect Days",
            "genre": "Drama",
            "director": "Wim Wenders",
            "duration": "124 Min.",
            "cinema": "Abaton-Kino",
            "date": dates[0],
            "time": "17:15",
            "room": "Saal 1",
            "format": "OmU",
            "link": "https://www.abaton.de"
        },
        {
            "id": 6,
            "title": "Anatomie eines Falls",
            "genre": "Thriller / Drama",
            "director": "Justine Triet",
            "duration": "151 Min.",
            "cinema": "Zeise Kino",
            "date": dates[1],
            "time": "19:30",
            "room": "Kino 2",
            "format": "DF",
            "link": "https://www.zeise.de"
        },
        {
            "id": 7,
            "title": "Klassiker der Moderne",
            "genre": "Retrospektive",
            "director": "Diverse",
            "duration": "90 Min.",
            "cinema": "Metropolis",
            "date": dates[2],
            "time": "17:00",
            "room": "Hauptsaal",
            "format": "OV",
            "link": "https://www.metropolis-hamburg.de"
        }
    ]
    
    with open("program.json", "w", encoding="utf-8") as f:
        json.dump(sample_movies, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    fetch_cinema_data()

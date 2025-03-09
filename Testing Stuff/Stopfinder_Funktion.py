import requests


def query_stopfinder():
    # API-Endpunkt und Abfrageparameter
    url = "https://www.efa-bw.de/mobidata-bw/XML_STOPFINDER_REQUEST"
    params = {
        'outputFormat': 'rapidJSON',
        'type_sf': 'any',
        'name_sf': 'Esslingen (Neckar) Bahnhof'  # Name der Haltestelle
    }
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    # Abfrage an die API senden
    response = requests.get(url, params=params, headers=headers)

    # Antwort verarbeiten
    if response.status_code == 200:
        data = response.json()
        print(data)
    else:
        print(f"Fehler: {response.status_code}")


# Funktion aufrufen
query_stopfinder()

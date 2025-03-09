# DM_Monitor_API.py

import requests
from datetime import datetime

def get_departures(name_dm):
    # Aktuelle Uhrzeit im Format HHMM
    current_time = datetime.now().strftime("%H%M")

    # API-Endpunkt und Abfrageparameter
    url = "https://www.efa-bw.de/mobidata-bw/XML_DM_REQUEST?"
    params = {
        'commonMacro': 'dm',
        'type_dm': 'any',
        'name_dm': name_dm,  # Übergabe der Haltestelle
        'itdTime': current_time,  # Aktuelle Uhrzeit statt fester Zeit
        'outputFormat': 'rapidJSON',
        'coordOutputFormat': 'WGS84[dd.ddddd]',
        'locationServerActive': '1',
        'mode': 'direct',  # sollte enthalten sein
        'useAllStops': '1',  # sollte enthalten sein
        'useRealtime': '1',  # aktiviert Echtzeit
        'useProxFootSearch': '0',  # sollte enthalten sein - keine alternativen Haltestellen
        'limit': '10'
    }
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    # Abfrage an die API senden
    response = requests.get(url, headers=headers, params=params)

    # Antwort verarbeiten
    if response.status_code == 200:
        data = response.json()
        departures = []
        for event in data.get("stopEvents", []):
            time = event.get("departureTimePlanned", "Unbekannt")[11:16]
            line = event["transportation"]["name"]
            destination = event["transportation"]["destination"]["name"]
            departures.append((time, line, destination))
        return departures
    else:
        return []

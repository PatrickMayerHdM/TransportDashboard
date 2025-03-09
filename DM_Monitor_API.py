import requests
from datetime import datetime


def get_departures():
    # Aktuelle Uhrzeit im Format HHMM
    current_time = datetime.now().strftime("%H%M")

    # API-Endpunkt und Abfrageparameter
    url = "https://www.efa-bw.de/mobidata-bw/XML_DM_REQUEST?"
    params = {
        'commonMacro': 'dm',
        'type_dm': 'any',
        'name_dm': 'de:08116:4118',  # Sulzgries Bergstraße
        'itdTime': current_time,  # Aktuelle Uhrzeit statt fester Zeit
        'outputFormat': 'rapidJSON',
        'coordOutputFormat': 'WGS84[dd.ddddd]',
        'locationServerActive': '1',
        'mode': 'direct', # should be included
        'useAllStops': '1', # should be included
        'useRealtime': '1', # activates real time
        'useProxFootSearch': '0', # should be included - no alternative stops
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


if __name__ == "__main__":
    print(get_departures())  # Teste den Abruf, wenn die Datei direkt ausgeführt wird

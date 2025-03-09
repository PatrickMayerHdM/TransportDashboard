import requests
from datetime import datetime

def get_departures(name_dm, limit=10):
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
        'limit': limit  # Limit für die API-Anfrage
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
            # Zeit und Transportdetails abrufen
            planned_time = event.get("departureTimePlanned", "Unbekannt")
            actual_time = event.get("departureTimeActual") or event.get("departureTimeEstimated", "Unbekannt")  # Echtzeit oder geschätzte Zeit
            time = planned_time[11:16] if planned_time != "Unbekannt" else "Unbekannt"  # HH:MM Format
            line = event["transportation"]["name"]
            destination = event["transportation"]["destination"]["name"]

            # Überprüfen, ob die Abfahrt in der Zukunft liegt
            if planned_time >= current_time:  # Vergleiche mit der aktuellen Zeit
                departures.append((time, line, destination, actual_time[11:16] if actual_time else "Unbekannt"))  # Echtzeit oder geschätzte Zeit hinzufügen

        return departures[:limit]  # Gibt nur die gewünschte Anzahl an Abfahrten zurück
    else:
        return []

import requests
from datetime import datetime
import pytz


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
        print(data)
        departures = []
        utc_tz = pytz.utc
        local_tz = pytz.timezone("Europe/Berlin")

        for event in data.get("stopEvents", []):
            # Zeit und Transportdetails abrufen
            planned_time = event.get("departureTimePlanned", "Unbekannt")
            actual_time = event.get("departureTimeActual") or event.get("departureTimeEstimated", "Unbekannt")
            line = event["transportation"]["name"]
            destination = event["transportation"]["destination"]["name"]
            operator_name = event["transportation"]["operator"]["name"]  # Betreiberinformationen

            # Zeitumrechnung von UTC zu lokaler Zeit
            if planned_time != "Unbekannt":
                dt_utc = datetime.strptime(planned_time, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=utc_tz)
                planned_time_local = dt_utc.astimezone(local_tz).strftime("%H:%M")
            else:
                planned_time_local = "Unbekannt"

            if actual_time and actual_time != "Unbekannt":
                dt_utc = datetime.strptime(actual_time, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=utc_tz)
                actual_time_local = dt_utc.astimezone(local_tz).strftime("%H:%M")
            else:
                actual_time_local = "Unbekannt"

            # Hinweise sammeln
            hints = [hint["content"] for hint in event.get("hints", [])]

            departures.append((planned_time_local, actual_time_local, line, destination, operator_name, hints))

        return departures[:limit]  # Gibt nur die gewünschte Anzahl an Abfahrten zurück
    else:
        return []

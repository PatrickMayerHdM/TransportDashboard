from flask import Flask, render_template
from DM_Monitor_API import get_departures

app = Flask(__name__)

# Liste von Haltestellen mit Limits
stations = {
    "Sulzgries Bergstraße (Richtung Esslingen)": ("de:08116:4118:0:4", 3),
    "Esslingen (N)": ("de:08116:7800", 10),
    "Sulzgries Maienwalterstraße (Richtung Esslingen)": ("de:08116:4112:0:4", 1),

}

@app.route('/')
def index():
    all_departures = {}  # Dictionary, um Abfahrten für jede Haltestelle zu speichern

    # Abfahrten für jede Haltestelle abrufen
    for station_name, (station_code, limit) in stations.items():
        all_departures[station_name] = get_departures(station_code, limit)  # Limit übergeben

    return render_template('index.html', all_departures=all_departures, stations=stations)

if __name__ == "__main__":
    app.run(debug=True)

import tkinter as tk
from tkinter import ttk
from DM_Monitor_API import get_departures

# Liste von Haltestellen mit Limits
stations = {
    "Sulzgries Bergstraße (Richtung Esslingen)": ("de:08116:4118:0:4", 3),
    "Esslingen (N)": ("de:08116:7800", 10),
    "Sulzgries Maienwalterstraße (Richtung Esslingen)": ("de:08116:4112:0:4", 1),
}

def fetch_departures():
    all_departures = {}
    for station_name, (station_code, limit) in stations.items():
        all_departures[station_name] = get_departures(station_code, limit)
    return all_departures

def update_table():
    all_departures = fetch_departures()
    for station in all_departures:
        tree.insert("", "end", text=station)
        for departure in all_departures[station]:
            tree.insert("", "end", values=(departure[0], departure[1], departure[2]))

# Hauptfenster erstellen
root = tk.Tk()
root.title("Abfahrten")
root.geometry("600x400")
root.configure(bg="#f2efe9")

# Überschrift
header = tk.Label(root, text="Abfahrten", font=("Arial", 24), bg="#f2efe9", fg="#252627")
header.pack(pady=10)

# Baumansicht (Treeview) für die Abfahrten
tree = ttk.Treeview(root, columns=("Zeit", "Linie", "Ziel"), show="headings", height=15)
tree.heading("Zeit", text="Zeit")
tree.heading("Linie", text="Linie")
tree.heading("Ziel", text="Ziel")
tree.column("Zeit", anchor="w")
tree.column("Linie", anchor="w")
tree.column("Ziel", anchor="w")
tree.pack(pady=20, padx=10, fill="x")

# Abfahrten abrufen und Tabelle aktualisieren
update_table()

# Hauptschleife starten
root.mainloop()

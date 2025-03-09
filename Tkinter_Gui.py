import tkinter as tk
from tkinter import ttk
from DM_Monitor_API import get_departures  # Importiert die Funktion aus api.py

def update_table():
    """Löscht die alte Tabelle und fügt neue Abfahrtsdaten hinzu."""
    for row in tree.get_children():
        tree.delete(row)
    for dep in get_departures():
        tree.insert("", "end", values=dep)

# GUI erstellen
root = tk.Tk()
root.title("Abfahrtsmonitor")
root.geometry("400x300")

# Spalten definieren
columns = ("Uhrzeit", "Linie", "Ziel")
tree = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100)

tree.pack(expand=True, fill="both")

# Aktualisieren-Button
btn = tk.Button(root, text="Aktualisieren", command=update_table)
btn.pack()

update_table()  # Starte mit den aktuellen Daten
root.mainloop()

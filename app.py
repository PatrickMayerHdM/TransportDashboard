
from flask import Flask, render_template
from DM_Monitor_API import get_departures

app = Flask(__name__)

@app.route('/')
def index():
    departures = get_departures()
    return render_template('index.html', departures=departures)

if __name__ == "__main__":
    app.run(debug=True)

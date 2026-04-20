from flask import Flask, render_template

app = Flask(__name__, template_folder="templates", static_folder="static")

cities = [
    {
        "name": "New York",
        "status": "Clear",
        "current": 22,
        "temperature_day": 25,
        "temperature_night": 16,
        "details": "Clear skies throughout the day. Low humidity and light winds from the southwest."
    },
    {
        "name": "London",
        "status": "Rain",
        "current": 13,
        "temperature_day": 15,
        "temperature_night": 9,
        "details": "Persistent light rain expected. Bring an umbrella. Visibility may be reduced in the evening."
    },
    {
        "name": "Tokyo",
        "status": "Fog",
        "current": 18,
        "temperature_day": 21,
        "temperature_night": 14,
        "details": "Morning fog clearing by midday. Afternoon will be partly cloudy with mild temperatures."
    },
    {
        "name": "Reykjavik",
        "status": "Snow",
        "current": -3,
        "temperature_day": 0,
        "temperature_night": -7,
        "details": "Heavy snowfall overnight continuing into the morning. Roads may be icy. Travel with caution."
    },
]

@app.route("/")
def index():
    return render_template("index.html", cities=cities)

@app.route("/city/<city_name>")
def city_detail(city_name):
    city = next((c for c in cities if c["name"] == city_name), None)
    if city is None:
        return "City not found", 404
    return render_template("city.html", city=city)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)

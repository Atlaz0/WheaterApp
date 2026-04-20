from flask import Flask, render_template
import requests

app = Flask(__name__, template_folder="templates", static_folder="static")

CITIES = [
    {"name": "New York",   "lat": 40.71,  "lon": -74.01},
    {"name": "London",     "lat": 51.51,  "lon": -0.13},
    {"name": "Tokyo",      "lat": 35.68,  "lon": 139.69},
    {"name": "Reykjavik",  "lat": 64.13,  "lon": -21.82},
    {"name": "Tallinn",    "lat": 59.44,  "lon": 24.75},
]

WMO_CODES = {
    0:  "Clear",
    1:  "Clear",  2: "Cloudy",  3: "Cloudy",
    45: "Fog",   48: "Fog",
    51: "Rain",  53: "Rain",   55: "Rain",
    61: "Rain",  63: "Rain",   65: "Rain",
    71: "Snow",  73: "Snow",   75: "Snow", 77: "Snow",
    80: "Rain",  81: "Rain",   82: "Rain",
    95: "Storm", 96: "Storm",  99: "Storm",
}

def fetch_weather(city):
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={city['lat']}&longitude={city['lon']}"
        "&current=temperature_2m,weathercode"
        "&daily=temperature_2m_max,temperature_2m_min"
        "&timezone=auto"
    )
    try:
        data = requests.get(url, timeout=5).json()
        code = data["current"]["weathercode"]
        return {
            "name":             city["name"],
            "status":           WMO_CODES.get(code, "Cloudy"),
            "current":          round(data["current"]["temperature_2m"]),
            "temperature_day":  round(data["daily"]["temperature_2m_max"][0]),
            "temperature_night":round(data["daily"]["temperature_2m_min"][0]),
            "details": (
                f"Weather code {code}. "
                f"High {round(data['daily']['temperature_2m_max'][0])}°C, "
                f"low {round(data['daily']['temperature_2m_min'][0])}°C."
            ),
        }
    except Exception as e:
        return {
            "name":             city["name"],
            "status":           "N/A",
            "current":          "?",
            "temperature_day":  "?",
            "temperature_night":"?",
            "details":          f"Could not fetch weather data: {e}",
        }

@app.route("/")
def index():
    cities = [fetch_weather(c) for c in CITIES]
    return render_template("index.html", cities=cities)

@app.route("/city/<city_name>")
def city_detail(city_name):
    match = next((c for c in CITIES if c["name"] == city_name), None)
    if match is None:
        return "City not found", 404
    city = fetch_weather(match)
    return render_template("city.html", city=city)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)

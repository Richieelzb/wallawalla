import os
import requests
from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    redirect,
    session
)

app = Flask(__name__)

API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

@app.route("/")
def home():
 return render_template("frontend.html")

@app.route("/location")
def location():
    lat = request.args.get("lat")
    lng = request.args.get("lng")

    url = (
        "https://maps.googleapis.com/maps/api/geocode/json"
        f"?latlng={lat},{lng}"
        f"&key={API_KEY}"
    )

    response = requests.get(url)
    data = response.json()

    if data["results"]:
        address = data["results"][0]["formatted_address"]
    else:
        address = "Location not found"

    return {"address": address}

@app.route("/health")
def health():
   return {"status": "healthy"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

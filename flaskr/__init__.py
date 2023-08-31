from flask import Flask, render_template, redirect, request, url_for, Markup
import requests
import urllib.request
import json

app = Flask(__name__)

API_KEY = "Y0UR_4P1_K3Y"


@app.route('/', methods=["POST", "GET"])
def index():
    if request.method == "POST":
        city = request.form.get("city")

        return redirect(url_for("weather", city=city))
    return render_template("index.html")


@app.route("/weather/<city>")
def weather(city: str):
    url = f"https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}&aqi=Yes"
    response = requests.get(url)
    data = response.json()
    city = data["location"]["name"]
    country = data["location"]["country"]
    localtime = data["location"]["localtime"][11::]
    temperature_C = data["current"]["temp_c"]
    condition = data["current"]["condition"]["text"]
    wind = data["current"]["wind_kph"]
    humidity = data["current"]["humidity"]
    print(temperature_C, condition, wind, humidity)
    # TODO RENDER
    """
    1. city & icon
    2. country & icon
    4. localtime & icon
    5. temp_C & temp_F & icon
    6. condition (e.g Partyl cloudy) & icon
    7. wind_mph & wind_kph & icon
    8. humidity & icon
    9. IN OTHER WINDOW MAYBE? Air Quality & icons
    """
    if condition == "Sunny":
        condition = "<i class='fa-solid fa-sun'>&nbsp;Sunny</i>"
    elif condition == "Partly cloudy":
        condition = "<i class='fa-solid fa-cloud-sun part' style='font-size:30px; white-space: nowrap;'>&nbsp;Partly cloudy</i>"
    elif condition == "Light rain":
        condition = "<i class='fa-solid fa-cloud-sun-rain' style='white-space: nowrap;'>&nbsp;Light Rain</i>"
    elif condition == "Clear":
        condition = "<i class='fa-solid fa-sun'>&nbsp;Clear</i>"
    elif condition == "Overcast":
        condition = "<i class='fa-solid fa-cloud'>&nbsp;Overcast</i>"
    elif condition == "Heavy snow" or condition == "Snow" or condition == "Light snow":
        condition = "<i class='fa-solid fa-snowflake'>&nbsp;Snow</i>"
    return render_template("weather.html", condition=condition,
                           city=city,
                           country=country,
                           time=localtime,
                           temperature=temperature_C,
                           wind=wind,
                           humidity=humidity)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8000", debug=True)

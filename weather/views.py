import os
import requests
from django.shortcuts import render


def weather_view(request):
    api_key = os.getenv("OPENWEATHER_API_KEY")
    city = request.GET.get("city", "Puerto Princesa")
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key, "units": "metric"}

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        weather_data = {
            "city": data["name"],
            "country": data["sys"]["country"],
            "temp": data["main"]["temp"],
            "description": data["weather"][0]["description"].title(),
            "icon": data["weather"][0]["icon"],
        }
    except requests.exceptions.HTTPError as e:
        # HTTPError must come before RequestException (it is a subclass)
        if e.response is not None and e.response.status_code == 404:
            weather_data = {"error": f"City '{city}' not found. Try mo another name."}
        elif e.response is not None and e.response.status_code == 401:
            weather_data = {"error": "Invalid or inactive API key. Check your .env file."}
        else:
            weather_data = {"error": "Weather service returned an error. Please try again."}
    except requests.exceptions.RequestException:
        weather_data = {"error": "Could not connect to the weather service. Check your internet."}
    except KeyError:
        weather_data = {"error": f"Could not find weather information for '{city}'."}

    return render(request, "weather.html", {"weather": weather_data, "city": city})
import datetime as dt
import requests
import os

BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"

API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_weather_city(location: str) -> str:
    """
    Fetches current weather data for a given location using the OpenWeatherMap API
    and formats it into a human-readable string.

    Args:
        location (str): The name of the city (e.g., "London", "New York").

    Returns:
        str: A formatted string containing weather information, or an error message.
    """
    if not API_KEY:
        return "Weather API key not found. Please set OPENWEATHER_API_KEY environment variable."

    url = f"{BASE_URL}appid={API_KEY}&q={location}&units=metric" 

    try:
        response = requests.get(url)
        response.raise_for_status() 
        data = response.json()

        if data.get("cod") == "404":
            return f"Could not find weather for '{location}'. Please check the city name."

        weather_description = data["weather"][0]["description"].capitalize()
        temperature = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        pressure = data["main"]["pressure"]
        city_name = data["name"]
        country = data["sys"]["country"]

        weather_report = (
            f"The current weather in {city_name}, {country} is {weather_description}. "
            f"The temperature is {temperature:.1f}°C, but it feels like {feels_like:.1f}°C. "
            f"Humidity is {humidity}%, wind speed is {wind_speed} m/s, and atmospheric pressure is {pressure} hPa."
        )
        return weather_report

    except requests.exceptions.RequestException as e:
        return f"Error fetching weather data: {e}"
    except KeyError:
        return "Unexpected data format from weather API. Could not parse weather information."
    except Exception as e:
        return f"An unexpected error occurred: {e}"


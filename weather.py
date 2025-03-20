import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_weather_data(city):
    API_KEY = os.getenv("WEATHER_API_KEY")
    if not API_KEY:
        print("Error: API key is missing. Set it in the .env file.")
        return None

    URL = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={city}&days=1&aqi=no&alerts=no"

    try:
        response = requests.get(URL)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return None

def compare_temperatures(city1, city2):
    data1 = get_weather_data(city1)
    data2 = get_weather_data(city2)

    if data1 and data2:
        temp1 = data1['current']['temp_f']
        temp2 = data2['current']['temp_f']
        
        if temp1 > temp2:
            temp_comparison = f"{city1} is warmer ({temp1}°F) than {city2} ({temp2}°F)."
        elif temp1 < temp2:
            temp_comparison = f"{city1} is colder ({temp1}°F) than {city2} ({temp2}°F)."
        else:
            temp_comparison = f"{city1} and {city2} have the same temperature: {temp1}°F."
        
        return temp_comparison
    return "Could not retrieve data for both cities."

def compare_rain_chance(city1, city2):
    data1 = get_weather_data(city1)
    data2 = get_weather_data(city2)

    if data1 and data2:
        try:
            rain_chance1 = data1['forecast']['forecastday'][0]['day'].get('daily_chance_of_rain', 0)
            rain_chance2 = data2['forecast']['forecastday'][0]['day'].get('daily_chance_of_rain', 0)

            if rain_chance1 > rain_chance2:
                return f"{city1} has a higher chance of rain ({rain_chance1}%) than {city2} ({rain_chance2}%)."
            elif rain_chance1 < rain_chance2:
                return f"{city1} has a lower chance of rain ({rain_chance1}%) than {city2} ({rain_chance2}%)."
            else:
                return f"Both {city1} and {city2} have the same chance of rain ({rain_chance1}%)."

        except KeyError:
            return "Could not retrieve chance of rain data from the API."
    
    return "Could not retrieve weather data for both cities."

city1 = input("Enter the first city: ")
city2 = input("Enter the second city: ")

print("\nTemperature Comparison:")
print(compare_temperatures(city1, city2))

print("\nRain Probability Comparison:")
print(compare_rain_chance(city1, city2))

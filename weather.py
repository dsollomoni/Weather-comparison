import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_weather_data(city):
    
    # Retrieve API key from environment variables
    API_KEY = os.getenv("WEATHER_API_KEY")
    if not API_KEY:
        print("Error: API key is missing. Set it in the .env file.")
        return None

    # API request URL for the given city (forecast for 1 day)
    URL = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={city}&days=1&aqi=no&alerts=no"

    try:
        response = requests.get(URL)  # Send request to the API
        response.raise_for_status()  # Raise an error for unsuccessful responses
        return response.json()  # Return the API response as JSON
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")  # Handle API errors
        return None

def compare_temperatures(city1, city2):
    # Fetches weather data for two cities and compares temperatures.

    data1 = get_weather_data(city1) 
    data2 = get_weather_data(city2) 

    if data1 and data2:
        temp1 = data1['current']['temp_f']  
        temp2 = data2['current']['temp_f'] 
        
        # Compare the temperatures and return the result
        if temp1 > temp2:
            temp_comparison = f"{city1} is warmer ({temp1}°F) than {city2} ({temp2}°F)."
        elif temp1 < temp2:
            temp_comparison = f"{city1} is colder ({temp1}°F) than {city2} ({temp2}°F)."
        else:
            temp_comparison = f"{city1} and {city2} have the same temperature: {temp1}°F."
        
        return temp_comparison
    return "Could not retrieve data for both cities."

def compare_rain_chance(city1, city2):
    # Compares the chance of rain between two cities.

    data1 = get_weather_data(city1)  
    data2 = get_weather_data(city2)  

    if data1 and data2:
        try:
            # Extract chance of rain from forecast data
            rain_chance1 = data1['forecast']['forecastday'][0]['day'].get('daily_chance_of_rain', 0)
            rain_chance2 = data2['forecast']['forecastday'][0]['day'].get('daily_chance_of_rain', 0)

            # Compare rain chances and return the result
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

# Display temperature comparison
print("\nTemperature Comparison:")
print(compare_temperatures(city1, city2))

# Display rain probability comparison
print("\nRain Probability Comparison:")
print(compare_rain_chance(city1, city2))

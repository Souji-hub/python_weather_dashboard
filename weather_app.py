import tkinter as tk
from tkinter import ttk
import requests
from PIL import Image, ImageTk
from datetime import datetime

# Function to fetch real-time weather data from WeatherAPI.com
def get_realtime_weather(api_key, city):
    base_url = "http://api.weatherapi.com/v1/current.json"
    params = {
        'key': api_key,
        'q': city,
        'aqi': 'yes'  
    }

    response = requests.get(base_url, params=params)
    realtime_weather_data = response.json()

    return realtime_weather_data

# Function to update the real-time weather information on the GUI
def update_realtime_weather():
    city = city_entry.get()
    if not city:
        result_label.config(text="Please enter a city.")
        return

    try:
        realtime_weather_data = get_realtime_weather(api_key, city)
        temperature = realtime_weather_data['current']['temp_c']
        description = realtime_weather_data['current']['condition']['text']
        aqi = realtime_weather_data['current']['air_quality']['us-epa-index']
        wind_speed = realtime_weather_data['current']['wind_kph']
        pressure = realtime_weather_data['current']['pressure_mb']
        humidity = realtime_weather_data['current']['humidity']

        # Update the result label with real-time weather details
        result_label.config(text=f'Real-Time Weather Information:\n'
                                  f'Temperature: {temperature}°C, {description.capitalize()}\n'
                                  f'AQI: {aqi}\nWind Speed: {wind_speed} kph\n'
                                  f'Pressure: {pressure} mb\nHumidity: {humidity}%')

        # Display real-time weather icon
        icon_url = f"http:{realtime_weather_data['current']['condition']['icon']}"
        icon_image = Image.open(requests.get(icon_url, stream=True).raw)
        icon_image = ImageTk.PhotoImage(icon_image)
        icon_label.config(image=icon_image)
        icon_label.image = icon_image

    except Exception as e:
        result_label.config(text=f'Error fetching real-time weather data: {str(e)}')

# Function to fetch weather forecast data from WeatherAPI.com
def get_forecast(api_key, city):
    base_url = "http://api.weatherapi.com/v1/forecast.json"
    params = {
        'key': api_key,
        'q': city,
        'days': 3  # You can adjust the number of days for the forecast
    }

    response = requests.get(base_url, params=params)
    forecast_data = response.json()

    return forecast_data

# Function to update the weather forecast information on the GUI
def update_forecast():
    city = city_entry.get()
    if not city:
        result_label.config(text="Please enter a city.")
        return

    try:
        forecast_data = get_forecast(api_key, city)
        forecast_days = forecast_data['forecast']['forecastday']

        # Clear previous results
        result_label.config(text="")

        # Display forecast for the next few days
        for day in forecast_days:
            date = datetime.strptime(day['date'], '%Y-%m-%d').strftime('%A, %B %d')
            max_temp = day['day']['maxtemp_c']
            min_temp = day['day']['mintemp_c']
            condition = day['day']['condition']['text']

            # Append forecast information to the result label
            result_label.config(text=result_label.cget("text") +
                               f'{date}: Max Temp: {max_temp}°C, Min Temp: {min_temp}°C, Condition: {condition}\n')

    except Exception as e:
        result_label.config(text=f'Error fetching weather forecast: {str(e)}')

# Function to fetch historical weather data from WeatherAPI.com
def get_historical_weather(api_key, city, date):
    base_url = "http://api.weatherapi.com/v1/history.json"
    params = {
        'key': api_key,
        'q': city,
        'dt': date  # Date in the format 'yyyy-mm-dd'
    }

    response = requests.get(base_url, params=params)
    historical_weather_data = response.json()

    return historical_weather_data

# Function to update the historical weather information on the GUI
def update_historical_weather():
    city = city_entry.get()
    date = historical_date_entry.get()

    if not city or not date:
        result_label.config(text="Please enter a city and a historical date.")
        return

    try:
        historical_weather_data = get_historical_weather(api_key, city, date)
        temperature = historical_weather_data['forecast']['forecastday'][0]['day']['avgtemp_c']
        description = historical_weather_data['forecast']['forecastday'][0]['day']['condition']['text']

        # Update the result label with historical weather details
        result_label.config(text=f'Historical Weather Information for {date}:\n'
                                  f'Average Temperature: {temperature}°C, {description.capitalize()}')

    except Exception as e:
        result_label.config(text=f'Error fetching historical weather data: {str(e)}')

# Function to fetch timezone information from WeatherAPI.com
def get_timezone(api_key, city):
    base_url = "http://api.weatherapi.com/v1/current.json"
    params = {
        'key': api_key,
        'q': city
    }

    response = requests.get(base_url, params=params)
    timezone_data = response.json()

    return timezone_data

# Function to update the timezone information on the GUI
def update_timezone():
    city = city_entry.get()
    if not city:
        result_label.config(text="Please enter a city.")
        return

    try:
        timezone_data = get_timezone(api_key, city)
        timezone = timezone_data['location']['tz_id']

        # Update the result label with timezone information
        result_label.config(text=f'Timezone Information:\nTimezone: {timezone}')

    except Exception as e:
        result_label.config(text=f'Error fetching timezone information: {str(e)}')

# Function to perform IP lookup using ipinfo.io
def ip_lookup():
    try:
        response = requests.get("https://ipinfo.io/json")
        ip_info = response.json()
        ip_address = ip_info.get('ip', 'N/A')
        city = ip_info.get('city', 'N/A')
        region = ip_info.get('region', 'N/A')
        country = ip_info.get('country', 'N/A')

        # Update the result label with IP lookup information
        result_label.config(text=f'IP Lookup Information:\n'
                                  f'IP Address: {ip_address}\nCity: {city}\nRegion: {region}\nCountry: {country}')

    except Exception as e:
        result_label.config(text=f'Error performing IP lookup: {str(e)}')

# Main GUI window
root = tk.Tk()
root.title("Weather Data Dashboard")

# API Key
with open('api_key.txt', 'r') as file:
    api_key = file.read().strip()

# City Entry
city_label = tk.Label(root, text="Enter City:")
city_label.grid(row=0, column=0, pady=10, padx=10, sticky='w')

city_entry = tk.Entry(root, width=30)
city_entry.grid(row=0, column=1, pady=10, padx=10)

# Real-Time Weather Button
get_realtime_weather_button = tk.Button(root, text="Get Real-Time Weather", command=update_realtime_weather)
get_realtime_weather_button.grid(row=0, column=2, pady=10, padx=10)

# Weather Forecast Button
get_forecast_button = tk.Button(root, text="Get Weather Forecast", command=update_forecast)
get_forecast_button.grid(row=0, column=3, pady=10, padx=10)

# Historical Weather Section
historical_date_label = tk.Label(root, text="Enter Historical Date (yyyy-mm-dd):")
historical_date_label.grid(row=1, column=0, pady=10, padx=10, sticky='w')

historical_date_entry = tk.Entry(root, width=20)
historical_date_entry.grid(row=1, column=1, pady=10, padx=10)

get_historical_weather_button = tk.Button(root, text="Get Historical Weather", command=update_historical_weather)
get_historical_weather_button.grid(row=1, column=2, pady=10, padx=10)

# Timezone Section
get_timezone_button = tk.Button(root, text="Get Timezone Information", command=update_timezone)
get_timezone_button.grid(row=1, column=3, pady=10, padx=10)

# IP Lookup Section
ip_lookup_button = tk.Button(root, text="Perform IP Lookup", command=ip_lookup)
ip_lookup_button.grid(row=2, column=0, pady=10, padx=10)

# Result Label
result_label = tk.Label(root, text="", justify='left')
result_label.grid(row=3, column=0, columnspan=4, pady=10, padx=10, sticky='w')

# Weather Icon Label
icon_label = tk.Label(root)
icon_label.grid(row=0, column=4, rowspan=4, pady=10, padx=10)

# Run the GUI
root.mainloop()

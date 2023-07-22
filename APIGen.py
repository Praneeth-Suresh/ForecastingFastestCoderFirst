import requests
import sys
import json
from datetime import date

# Code to get the current weather; used during experimentation with the API and Github Copilot
"""""""""
def GetRawWeather():
    try:
        city = "+".join(sys.argv[1:])
    except IndexError:
        sys.exit("Please enter a city name as an argument")

    api_key = '6164e853cf114c97b92102633232306'

    try:
        response = requests.get(f"https://api.worldweatheronline.com/premium/v1/weather.ashx?q={city}&num_of_days=0&date=today&fx=no&mca=no&format=json&key={api_key}")
        response = response.json()
        return response
    except (requests.exceptions.ConnectionError, requests.exceptions.InvalidURL):
        sys.exit("Please enter a valid city name")

def ParseRawWeather(response): # we need city name, date, time, tempC, weatherDesc[value], windspeedKmph, rainfall, humidity, visibility, pressure, cloudcover, FeelsLikeC, icon
    raw_data = response["data"]
    city = raw_data["request"][0]["query"]
    today = date.today().strftime(r'%Y-%m-%d')
    time = raw_data["current_condition"][0]["observation_time"]
    tempC = raw_data["current_condition"][0]["temp_C"]
    weatherIconUrl = raw_data["current_condition"][0]["weatherIconUrl"][0]["value"]
    weatherDesc = raw_data["current_condition"][0]["weatherDesc"][0]["value"]
    windspeedKmph = raw_data["current_condition"][0]["windspeedKmph"]
    rainfall = raw_data["current_condition"][0]["precipMM"]
    humidity = raw_data["current_condition"][0]["humidity"]
    visibility = raw_data["current_condition"][0]["visibility"]
    pressure = raw_data["current_condition"][0]["pressure"]
    cloudcover = raw_data["current_condition"][0]["cloudcover"]
    FeelsLikeC = raw_data["current_condition"][0]["FeelsLikeC"]
    
    return [city, today, time, tempC, weatherIconUrl, weatherDesc, windspeedKmph, rainfall, humidity, visibility, pressure, cloudcover, FeelsLikeC]

def DisplayWeather(data):
    print(f"City: {data[0]}")
    print(f"Date: {data[1]}")
    print(f"Time: {data[2]}")
    print(f"Temperature: {data[3]}°C")
    print(f"Weather Icon: {data[4]}")
    print(f"Weather Description: {data[5]}")
    print(f"Wind Speed: {data[6]}km/h")
    print(f"Rainfall: {data[7]}mm")
    print(f"Humidity: {data[8]}%")
    print(f"Visibility: {data[9]}km")
    print(f"Pressure: {data[10]}mb")
    print(f"Cloud Cover: {data[11]}%")
    print(f"Feels Like: {data[12]}°C")
    
    
raw_weather_data = GetRawWeather()
DisplayWeather(ParseRawWeather(raw_weather_data))
"""

def GetRawWeatherFC(city):
    api_key = '6164e853cf114c97b92102633232306'

    try:
        url = "https://api.worldweatheronline.com/premium/v1/weather.ashx"
        params = {
            "key": api_key,
            "q": city,
            "format": "json",
            "num_of_days": 1,
            "cc": "no",
            "mca": "no",
            "tp": 1
        }
        response = requests.get(url, params=params)
        data = json.loads(response.text)
        return data
    except (requests.exceptions.ConnectionError, requests.exceptions.InvalidURL):
        print("Please enter a valid city name")
        sys.exit("Please enter a valid city name")

def ParseRawWeatherFC(data): # we need city name, date, time, tempC, weatherDesc[value], windspeedKmph, rainfall, humidity, visibility, pressure, cloudcover, FeelsLikeC, icon
    weather_data = data['data']['weather'][0]['hourly']
    city = data['data']['request'][0]['query']
    Date = data['data']['weather'][0]['date']
    # print(f"City: {city}")
    # print(f"Date: {Date}")
    all_data = [city, Date]
    for hourly_data in weather_data:
        time = hourly_data['time']
        tempC = hourly_data['tempC']
        weatherDesc = hourly_data['weatherDesc'][0]['value']
        windspeedKmph = hourly_data['windspeedKmph']
        rainfall = hourly_data['precipMM']
        humidity = hourly_data['humidity']
        visibility = hourly_data['visibility']
        pressure = hourly_data['pressure']
        cloudcover = hourly_data['cloudcover']
        FeelsLikeC = hourly_data['FeelsLikeC']
        icon = hourly_data['weatherIconUrl'][0]['value']

        this_hour = {
            "time": f"{(int(time)//100):02d}:00",
            "weatherDesc": weatherDesc,
            "tempC": tempC,
            "FeelsLikeC": FeelsLikeC,
            "windspeedKmph": windspeedKmph,
            "rainfall": rainfall,
            "humidity": humidity,
            "visibility": visibility,
            "pressure": pressure,
            "cloudcover": cloudcover,
            "weatherIconUrl": icon
        }
        all_data.append(this_hour)

        # print(f"Time: {(int(time)//100):02d}:00")
        # print(f"Weather Description: {weatherDesc}")
        # print(f"Temperature: {tempC}°C")
        # print(f"Feels Like: {FeelsLikeC}°C")
        # print(f"Wind Speed: {windspeedKmph}km/h")
        # print(f"Rainfall: {rainfall}mm")
        # print(f"Humidity: {humidity}%")
        # print(f"Visibility: {visibility}km")
        # print(f"Pressure: {pressure}mb")
        # print(f"Cloud Cover: {cloudcover}%")
        # print("\n")

    return all_data

# print(GetRawWeatherFC("Auckland"))
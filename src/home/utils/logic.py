import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
import requests


class WeatherApiClient:
    def __init__(self, session):
        self.session = session

    def get_weather_data(self, latitude, longitude, location_name):
        raise NotImplementedError


class OpenMeteoApiClient(WeatherApiClient):
    def get_weather_data(self, latitude, longitude, location_name):
        # Setup the Open-Meteo API client with cache and retry on error
        cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
        retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
        openmeteo = openmeteo_requests.Client(session=retry_session)

        # Make sure all required weather variables are listed here
        # The order of variables in hourly or daily is important to assign them correctly below
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "hourly": "temperature_2m"
        }
        responses = openmeteo.weather_api(url, params=params)

        # Process first location. Add a for-loop for multiple locations or weather models
        response = responses[0]
        print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
        print(f"Elevation {response.Elevation()} m asl")
        print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
        print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

        # Process hourly data. The order of variables needs to be the same as requested.
        hourly = response.Hourly()
        hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()

        hourly_data = {
            "latitude": latitude,
            "longitude": longitude,
            "location_name": location_name,
            "date": pd.date_range(
                start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
                end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
                freq=pd.Timedelta(seconds=hourly.Interval()),
                inclusive="left"
            ).strftime("%Y-%m-%d %H:%M:%S"),
            "temperature_2m": hourly_temperature_2m.tolist(),
        }

        return hourly_data


class WeatherDataFactory:
    def __init__(self, api_client):
        self.api_client = api_client

    def get_weather_data(self, latitude, longitude, location_name):
        return self.api_client.get_weather_data(latitude, longitude, location_name)
    
    @staticmethod
    def get_districts_temperature():
        # Fetching data of all districts in Bangladesh
        districts_url = "https://raw.githubusercontent.com/strativ-dev/technical-screening-test/main/bd-districts.json"
        response = requests.get(districts_url)
        districts_data = response.json()["districts"]

        # Fetching temperature forecast for each district
        coolest_districts = []
        for district in districts_data:
            lat = district["lat"]
            long = district["long"]
            forecast_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&hourly=temperature_2m"
            response = requests.get(forecast_url)
            forecast_data = response.json().get("hourly", {}).get("temperature_2m", {})

            # Extracting temperatures at 2 PM for the next 7 days
            temperatures_at_2pm = forecast_data[13:20]

            # Calculating average temperature at 2 PM for the next 7 days
            average_temperature = sum(temperatures_at_2pm) / len(temperatures_at_2pm)

            # Storing district name and its average temperature
            coolest_districts.append({"name": district["name"], "average_temperature": average_temperature})

        # Sorting districts based on average temperature and selecting the coolest 10
        coolest_districts = sorted(coolest_districts, key=lambda x: x["average_temperature"])[:10]
        return coolest_districts


class WeatherAnalyzer:
    @staticmethod
    def compare_temperatures(location1, location2, date, csv_file):
        # Read the CSV file
        weather_data = pd.read_csv(csv_file)
        # Filter data for location1
        location1_data = weather_data[(weather_data['latitude'] == location1[0]) & (
                    weather_data['longitude'] == location1[1])]
        location1_date_data = location1_data[location1_data['date'] == date]
        if location1_date_data.empty:
            return f"No data available for location1 on {date}"
        temperature1 = location1_date_data.iloc[0]['temperature_2m']
        # Filter data for location2
        location2_data = weather_data[(weather_data['latitude'] == location2[0]) & (
                    weather_data['longitude'] == location2[1])]
        location2_date_data = location2_data[location2_data['date'] == date]
        if location2_date_data.empty:
            return f"No data available for location2 on {date}"
        temperature2 = location2_date_data.iloc[0]['temperature_2m']
        # Comparing temperatures and deciding if it's suitable for travel
        if temperature1 < temperature2:
            return f"Location 1 has a cooler temperature ({temperature1}°C) compared to Location 2 " \
                   f"({temperature2}°C). It's suitable for travel."
        elif temperature1 > temperature2:
            return f"Location 2 has a cooler temperature ({temperature2}°C) compared to Location 1 " \
                   f"({temperature1}°C). It's suitable for travel."
        else:
            return f"The temperatures at Location 1 ({temperature1}°C) and Location 2 " \
                   f"({temperature2}°C) are the same. Choose according to your preference."
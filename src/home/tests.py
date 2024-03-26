from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import ForecastMetaData, ForecastData


class ForecastTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.create_forecast_data()

    def create_forecast_data(self):
        locations = [
            {"name": "Dhaka", "latitude": "23.7115253", "longitude": "90.4111451", "temperature": 28.5},
            {"name": "Satkhira", "latitude": "22.7185", "longitude": "89.0705", "temperature": 25.5},
            {"name": "Gopalganj", "latitude": "23.0050857", "longitude": "89.8266059", "temperature": 24.5},
            {"name": "Chattogram", "latitude": "22.335109", "longitude": "91.834073", "temperature": 26.8},
            {"name": "Rajshahi", "latitude": "24.3745", "longitude": "88.6042", "temperature": 27.2},
            {"name": "Barisal", "latitude": "22.702921", "longitude": "90.346597", "temperature": 25.0},
            {"name": "Khulna", "latitude": "22.815774", "longitude": "89.551148", "temperature": 25.3},
            {"name": "Mymensingh", "latitude": "24.7460", "longitude": "90.4028", "temperature": 26.1},
            {"name": "Sylhet", "latitude": "24.8898", "longitude": "91.8710", "temperature": 24.9},
            {"name": "Comilla", "latitude": "23.4682", "longitude": "91.1782", "temperature": 25.7}
        ]

        for location_data in locations:
            location_obj = ForecastMetaData.objects.create(
                latitude=location_data["latitude"],
                longitude=location_data["longitude"],
                location_name=location_data["name"],
                average_temperature=location_data["temperature"]
            )
            ForecastData.objects.create(
                forecast_meta_data=location_obj,
                date="2024-04-01 14:00:00",
                temperature_2m=location_data["temperature"]
            )

    def test_get_average_temperature(self):
        url = '/api/get_average_temperature/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('source', response.data)
        self.assertIn('data', response.data)
        self.assertIn(response.data['source'], ['database', 'cache'])

    def test_compare_temperature(self):
        request_data_list = [
            {"present_location": "Dhaka", "destination_location": "Satkhira", "travel_date": "2024-04-01"},
        ]

        for request_data in request_data_list:
            response = self.client.post('/api/compare_temperature/', request_data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIn(response.data['source'], ['database', 'cache'])

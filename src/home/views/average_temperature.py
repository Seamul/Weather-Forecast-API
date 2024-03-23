"""
Module: get_lowest_average_temperatures.py

This module contains an APIView class, GetLowestAverageTemperatures, for retrieving the lowest average temperatures from forecast metadata.

Classes:
- GetLowestAverageTemperatures: APIView class for retrieving the lowest average temperatures.

Dependencies:
- Django Rest Framework
- ..models: ForecastMetaData
- ..serializer: ForecastMetaDataSerializer

Usage:
- Import GetLowestAverageTemperatures class and call its get method to retrieve the lowest average temperatures.

API Endpoint:
- URL: GET http://0.0.0.0:8700/api/get_average_temperature/
- Method: GET
- Response:
    {
        "lowest_10_average_temperatures": [
            {
                "id": 507,
                "latitude": "26.3411",
                "longitude": "88.5541606",
                "location_name": "Panchagarh",
                "average_temperature": 21.356285895620072,
                "created_at": "2024-03-21T17:55:33.537888Z",
                "updated_at": "2024-03-21T17:55:33.549997Z"
            },
            {
                "id": 509,
                "latitude": "26.0336945",
                "longitude": "88.4616834",
                "location_name": "Thakurgaon",
                "average_temperature": 21.984570787066506,
                "created_at": "2024-03-21T17:55:34.165233Z",
                "updated_at": "2024-03-21T17:55:34.173923Z"
            },
            ...
        ]
    }
"""

from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import ForecastMetaData
from ..serializer import ForecastMetaDataSerializer


class GetLowestAverageTemperatures(APIView):
    """
    APIView class for retrieving the lowest average temperatures from forecast metadata.

    Methods:
    - get: Handles GET requests to retrieve the lowest average temperatures.
    """

    def get(self, request):
        """
        Handles GET requests to retrieve the lowest average temperatures.

        Returns:
        - Response: JSON response containing the lowest 10 average temperatures.
        """
        cache_key = 'lowest_average_temperatures'
        cached_data = cache.get(cache_key)
        
        if cached_data:
            source = "cache"
            return Response({"source": source, "data": cached_data})
        else:
            lowest_temperatures = ForecastMetaData.objects.exclude(
                average_temperature=None).order_by('average_temperature')[:10]

            serializer = ForecastMetaDataSerializer(lowest_temperatures, many=True)
            data = serializer.data

            # Cache the data
            cache.set(cache_key, data, 60 * 15)  # Cache for 15 minutes

            source = "database"
            return Response({"source": source, "data": data})




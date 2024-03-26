from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from ..models import ForecastData, ForecastMetaData
from ..serializer import ForecastMetaDataSerializer
import json

class GetLowestAverageTemperatures(APIView):
    """
    APIView class for retrieving the lowest average temperatures from forecast metadata.
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
            # Deserialize cached data
            cached_data = json.loads(cached_data)
            source = "cache"
            return Response({"source": source, "data": cached_data})
        else:
            lowest_temperatures = ForecastMetaData.objects.exclude(
                average_temperature=None).order_by('average_temperature')[:10]

            serializer = ForecastMetaDataSerializer(lowest_temperatures, many=True)
            data = serializer.data

            # Serialize data before caching
            cache.set(cache_key, json.dumps(data), 60 * 15)  # Cache for 15 minutes

            source = "database"
            return Response({"source": source, "data": data})

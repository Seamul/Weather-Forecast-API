from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import ForecastData



class GetLowestAverageTemperatures(APIView):
    def get(self, request):
        return Response({"lowest_10_average_temperatures": "lowest_10_average_temperatures"})

from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import ForecastMetaData
from ..serializer import ForecastMetaDataSerializer


class GetLowestAverageTemperatures(APIView):
    def get(self, request):

        lowest_temperatures = ForecastMetaData.objects.exclude(
            average_temperature=None).order_by('average_temperature')[:10]

        serializer = ForecastMetaDataSerializer(lowest_temperatures, many=True)

        return Response({"lowest_10_average_temperatures": serializer.data})

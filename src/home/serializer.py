from rest_framework import serializers
from .models import District,ForecastData


class DistrictSerializer(serializers.ModelSerializer):

    class Meta:
        model = District
        fields = '__all__'

class ForecastDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = ForecastData
        fields = '__all__'
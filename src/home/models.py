from django.db import models
from django.db.models import Avg, FloatField
# Create your models here.
from django.db.models.functions import Cast
from django.db import models
from django.db.models import Avg
from django.db.models.signals import post_save
from django.dispatch import receiver


class TestModel(models.Model):
    test_field = models.CharField(max_length=255)


class District(models.Model):
    division_id = models.CharField(max_length=10, null=True)
    name = models.CharField(max_length=20, null=True)
    bn_name = models.CharField(max_length=20, null=True)
    lat = models.CharField(max_length=20, null=True)
    long = models.CharField(max_length=40, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)


class ForecastDataManager(models.Manager):
    pass


class ForecastMetaData(models.Model):
    latitude = models.CharField(max_length=20, null=True)
    longitude = models.CharField(max_length=20, null=True)
    location_name = models.CharField(max_length=40, null=True)
    average_temperature = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    # TODO: singleton pattern

    class Meta:
        verbose_name_plural = 'ForecastMetaData'
        unique_together = [['latitude', 'longitude', 'location_name']]


class ForecastData(models.Model):
    forecast_meta_data = models.ForeignKey(
        ForecastMetaData, on_delete=models.CASCADE, related_name="forecast_meta_data", null=True)
    date = models.CharField(max_length=20, null=True)
    temperature_2m = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    objects = ForecastDataManager()

    class Meta:
        verbose_name_plural = 'ForecastData'

    def __str__(self):
        return f'{self.date}'


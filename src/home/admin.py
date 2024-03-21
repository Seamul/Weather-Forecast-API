from django.contrib import admin

# # Register your models here.
from .models import TestModel, District, ForecastData, ForecastMetaData

# @admin.register(TestModel)
# class TestModelAdmin(admin.ModelAdmin):
#     list_display=['test_field']


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ['id', 'division_id', 'name', 'bn_name', 'lat', 'long']


@admin.register(ForecastData)
class ForecastDataAdmin(admin.ModelAdmin):
    list_display = ['id','forecast_meta_data', 'date', 'temperature_2m']


# @admin.register(AverageTemperatureByLocation)
# class AverageTemperatureByLocationAdmin(admin.ModelAdmin):
#     list_display = ['id', 'location_name']


@admin.register(ForecastMetaData)
class ForecastMetaDataAdmin(admin.ModelAdmin):
    list_display = ['id', 'average_temperature',
                    'latitude', 'longitude', 'location_name']

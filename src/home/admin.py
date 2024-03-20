from django.contrib import admin

# # Register your models here.
from .models import TestModel, District, ForecastData

# @admin.register(TestModel)
# class TestModelAdmin(admin.ModelAdmin):
#     list_display=['test_field']


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ['id', 'division_id', 'name', 'bn_name', 'lat', 'long']


@admin.register(ForecastData)
class ForecastDataAdmin(admin.ModelAdmin):
    list_display = ['id', 'date', 'temperature_2m',
                    'latitude', 'longitude', 'location_name']

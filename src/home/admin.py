from django.contrib import admin

# # Register your models here.
from .models import TestModel, District

# @admin.register(TestModel)
# class TestModelAdmin(admin.ModelAdmin):
#     list_display=['test_field']


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ['id', 'division_id', 'name', 'bn_name', 'lat', 'long']

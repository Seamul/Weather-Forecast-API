from django.db import models

# Create your models here.


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

class ForecastData(models.Model):
    date = models.CharField(max_length=20, null=True)
    temperature_2m = models.CharField(max_length=20, null=True)
    latitude = models.CharField(max_length=20, null=True)
    longitude = models.CharField(max_length=20, null=True)
    location_name = models.CharField(max_length=40, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    objects = ForecastDataManager()

    class Meta:
        verbose_name_plural = 'ForecastData'

    def __str__(self):
        return f'{self.date} - {self.location_name}'
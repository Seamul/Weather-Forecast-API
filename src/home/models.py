from django.db import models

# Create your models here.
class TestModel(models.Model):
    test_field=models.CharField(max_length=255)



class District(models.Model):
    division_id=models.CharField(max_length=10, null=True)
    name=models.CharField(max_length=20, null=True)
    bn_name=models.CharField(max_length=20, null=True)
    lat=models.CharField(max_length=20, null=True)
    long=models.CharField(max_length=40, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
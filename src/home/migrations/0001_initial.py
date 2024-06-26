# Generated by Django 4.2.5 on 2024-03-20 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Districts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('division_id', models.CharField(max_length=4, null=True)),
                ('name', models.CharField(max_length=20, null=True)),
                ('bn_name', models.CharField(max_length=20, null=True)),
                ('lat', models.CharField(max_length=20, null=True)),
                ('long', models.CharField(max_length=4, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TestModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_field', models.CharField(max_length=255)),
            ],
        ),
    ]

# Generated by Django 5.1.3 on 2024-12-06 13:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("forecast", "0003_remove_weatherdata_chance_of_rain_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="weatherdata",
            name="chance_of_rain",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="weatherdata",
            name="chance_of_snow",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="weatherdata",
            name="will_it_rain",
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AddField(
            model_name="weatherdata",
            name="will_it_snow",
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
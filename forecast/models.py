# forecast/models.py
from django.db import models


class Location(models.Model):
    city = models.CharField(max_length=100)


class WeatherData(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="weather_data")
    date = models.DateField()
    time = models.TimeField()

    # add from API1
    temp_max = models.FloatField(null=True, blank=True)
    temp_min = models.FloatField(null=True, blank=True)
    temp_current = models.FloatField(null=True, blank=True)
    will_it_rain = models.BooleanField(default=False, blank=True)
    chance_of_rain = models.FloatField(null=True, blank=True)
    will_it_snow = models.BooleanField(default=False, blank=True)
    chance_of_snow = models.FloatField(null=True, blank=True)

    # add from API2
    sunrise = models.TimeField(null=True, blank=True)
    sunset = models.TimeField(null=True, blank=True)
    conditions = models.CharField(max_length=255, null=True, blank=True)
    precipitation = models.FloatField(null=True, blank=True)
    precipitation_probability = models.FloatField(null=True, blank=True)

    wind_speed = models.FloatField(null=True, blank=True)
    wind_gust = models.FloatField(null=True, blank=True)

    humidity = models.FloatField(null=True, blank=True)
    pressure = models.FloatField(null=True, blank=True)
    dew_point = models.FloatField(null=True, blank=True)
    feels_like = models.FloatField(null=True, blank=True)
    cloud_cover = models.FloatField(null=True, blank=True)
    visibility = models.FloatField(null=True, blank=True)
    uv_index = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = "WeatherData"
        verbose_name_plural = "WeatherData"

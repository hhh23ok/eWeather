# Generated by Django 5.1.3 on 2024-12-06 13:00

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("forecast", "0002_alter_weatherdata_options_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="weatherdata",
            name="chance_of_rain",
        ),
        migrations.RemoveField(
            model_name="weatherdata",
            name="chance_of_snow",
        ),
        migrations.RemoveField(
            model_name="weatherdata",
            name="cloud_cover",
        ),
        migrations.RemoveField(
            model_name="weatherdata",
            name="conditions",
        ),
        migrations.RemoveField(
            model_name="weatherdata",
            name="dew_point",
        ),
        migrations.RemoveField(
            model_name="weatherdata",
            name="feels_like",
        ),
        migrations.RemoveField(
            model_name="weatherdata",
            name="humidity",
        ),
        migrations.RemoveField(
            model_name="weatherdata",
            name="precipitation",
        ),
        migrations.RemoveField(
            model_name="weatherdata",
            name="precipitation_probability",
        ),
        migrations.RemoveField(
            model_name="weatherdata",
            name="pressure",
        ),
        migrations.RemoveField(
            model_name="weatherdata",
            name="sunrise",
        ),
        migrations.RemoveField(
            model_name="weatherdata",
            name="sunset",
        ),
        migrations.RemoveField(
            model_name="weatherdata",
            name="uv_index",
        ),
        migrations.RemoveField(
            model_name="weatherdata",
            name="visibility",
        ),
        migrations.RemoveField(
            model_name="weatherdata",
            name="will_it_rain",
        ),
        migrations.RemoveField(
            model_name="weatherdata",
            name="will_it_snow",
        ),
        migrations.RemoveField(
            model_name="weatherdata",
            name="wind_direction",
        ),
        migrations.RemoveField(
            model_name="weatherdata",
            name="wind_gust",
        ),
        migrations.RemoveField(
            model_name="weatherdata",
            name="wind_speed",
        ),
    ]

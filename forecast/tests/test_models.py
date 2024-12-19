from django.test import TestCase
from forecast.models import Location, WeatherData
from datetime import date, time


class LocationModelTest(TestCase):

    def setUp(self):
        # Create a sample Location instance for testing
        self.location = Location.objects.create(city="Test City")

    def test_location_creation(self):
        """Test that a Location instance is created and saved correctly."""
        self.assertEqual(self.location.city, "Test City")

    def test_str_representation(self):
        """Test the string representation of the model (if defined later)."""
        # By default, str() will give "<Location: Location object (1)>"
        # Update this test if you define a __str__ method in the model.
        self.assertEqual(str(self.location), f"Location object ({self.location.id})")

    def test_city_field_max_length(self):
        """Test that the city field respects the max_length constraint."""
        max_length = Location._meta.get_field('city').max_length
        self.assertEqual(max_length, 100)


class WeatherDataModelTest(TestCase):

    def setUp(self):
        # Create a Location instance for ForeignKey testing
        self.location = Location.objects.create(city="Test City")
        # Create a WeatherData instance
        self.weather_data = WeatherData.objects.create(
            location=self.location,
            date=date(2024, 12, 14),
            time=time(12, 30),
            temp_max=30.5,
            temp_min=20.1,
            temp_current=25.3,
            will_it_rain=True,
            chance_of_rain=75.5,
            will_it_snow=False,
            chance_of_snow=0.0,
            sunrise=time(6, 15),
            sunset=time(18, 45),
            conditions="Clear Sky",
            precipitation=0.0,
            precipitation_probability=0.0,
            wind_speed=12.4,
            wind_gust=20.3,
            humidity=65.2,
            pressure=1015.3,
            dew_point=18.5,
            feels_like=27.0,
            cloud_cover=10.0,
            visibility=10.0,
            uv_index=5,
        )

    def test_weather_data_creation(self):
        """Test that WeatherData instance is created and saved correctly."""
        self.assertEqual(self.weather_data.location.city, "Test City")
        self.assertEqual(self.weather_data.date, date(2024, 12, 14))
        self.assertEqual(self.weather_data.temp_max, 30.5)
        self.assertTrue(self.weather_data.will_it_rain)

    def test_optional_fields(self):
        """Test that optional fields can store null values."""
        weather_data_null = WeatherData.objects.create(
            location=self.location,
            date=date(2024, 12, 15),
            time=time(15, 0),
        )
        self.assertIsNone(weather_data_null.temp_max)
        self.assertIsNone(weather_data_null.sunrise)
        self.assertFalse(weather_data_null.will_it_rain)

    def test_relationship_with_location(self):
        """Test the relationship between WeatherData and Location."""
        related_weather_data = self.location.weather_data.all()
        self.assertEqual(related_weather_data.count(), 1)
        self.assertEqual(related_weather_data.first(), self.weather_data)

    def test_field_max_length(self):
        """Test the max_length of the conditions field."""
        max_length = WeatherData._meta.get_field('conditions').max_length
        self.assertEqual(max_length, 255)

    def test_default_values(self):
        """Test that default values are set correctly."""
        weather_data_default = WeatherData.objects.create(
            location=self.location,
            date=date(2024, 12, 15),
            time=time(10, 0),
        )
        self.assertFalse(weather_data_default.will_it_rain)
        self.assertFalse(weather_data_default.will_it_snow)
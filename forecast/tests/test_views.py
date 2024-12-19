from django.test import TestCase
from forecast.views import get_icon_for_weather


class GetIconForWeatherTests(TestCase):

    def test_get_icon_for_weather_clear(self):
        self.assertEqual(get_icon_for_weather('Clear'), 'bi bi-sun')

    def test_get_icon_for_weather_rain(self):
        self.assertEqual(get_icon_for_weather('Rain'), 'bi bi-cloud-rain')

    def test_get_icon_for_weather_combined_conditions(self):
        self.assertEqual(get_icon_for_weather('Rain, Overcast'), 'bi bi-cloud-rain')
        self.assertEqual(get_icon_for_weather('Partially cloudy, Wind'), 'bi bi-cloud-sun')

    def test_get_icon_for_weather_unknown_condition(self):
        self.assertEqual(get_icon_for_weather('Hail'), 'bi bi-cloud')

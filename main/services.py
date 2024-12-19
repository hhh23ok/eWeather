# main/services.py
from forecast.services import combine_weather_forecasts
from forecast.views import get_icon_for_weather


def get_forecast_data(location):
    try:
        forecast_data = combine_weather_forecasts(location, 7)

        if not forecast_data:
            raise ValueError("Invalid or missing weather data.")

        # Apply weather icons to the forecast data
        for day in forecast_data:
            day['icon'] = get_icon_for_weather(day['conditions'])

        return forecast_data

    except ValueError as e:
        print(f"Error processing weather data: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None


# def get_forecast_data(location):
#     base_url = ("https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"
#                 + location
#                 + "?key="
#                 + VISUAL_CROSSING_API_KEY)
#
#     response = requests.get(base_url)
#
#     if response.status_code == 200:
#         data = response.json()
#
#         forecast_days = 7
#         forecast_data = []
#
#         for day in data['days'][:forecast_days]:
#             forecast_data.append({
#                 'date': day['datetime'],
#                 'tempmax': fahrenheit_to_celsius(day['tempmax']),
#                 'tempmin': fahrenheit_to_celsius(day['tempmin']),
#                 'windspeed': day['windspeed'],
#                 'windgust': day['windgust'],
#                 'precipprob': day['precipprob'],
#                 'humidity': day['humidity'],
#                 'uvindex': day['uvindex'],
#                 'sunrise': day['sunrise'],
#                 'sunset': day['sunset'],
#                 'icon': get_icon_for_weather(day['conditions'])
#             })
#
#         return forecast_data
#     else:
#         print("Unable to get data from API")
#         return None

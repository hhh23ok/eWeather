# forecast/views.py
from django.shortcuts import render
from .services import combine_weather_forecasts


def forecast_days(request):
    days = 12
    location = request.GET.get('location', 'London')
    try:
        forecast_data = combine_weather_forecasts(location, days)

        if not forecast_data:
            raise ValueError("Invalid or missing weather data.")

        for day in forecast_data:
            day['icon'] = get_icon_for_weather(day['conditions'])

        # Prepare chart data
        if forecast_data:
            dates = [day['date'] for day in forecast_data]
            temp_min = [day['tempmin'] for day in forecast_data]
            temp_max = [day['tempmax'] for day in forecast_data]
            chart_data = {'dates': dates, 'temp_min': temp_min, 'temp_max': temp_max}
        else:
            chart_data = None

        return render(request, 'forecast/forecast.html', {'forecast_data': forecast_data, 'location': location, 'chart_data': chart_data})

    except ValueError as e:
        print(f"Error processing weather data: {e}")
        error_message = "Weather data is unavailable at the moment. Please try again later."
        return render(request, 'forecast/forecast.html', {'error_message': error_message, 'location': location})
    except Exception as e:
        print(f"Unexpected error: {e}")
        error_message = "Unable to fetch weather data. Please check the location or try again later."
        return render(request, 'forecast/forecast.html', {'error_message': error_message, 'location': location})


def get_icon_for_weather(description):
    icon_map = {
        'Clear': 'bi bi-sun',
        'Partly Cloudy': 'bi bi-cloud-sun',
        'Cloudy': 'bi bi-cloud',
        'Rain': 'bi bi-cloud-rain',
        'Snow': 'bi bi-snow',
        'Wind': 'bi bi-wind',
        'Thunderstorm': 'bi bi-cloud-lightning',
        'Fog': 'bi bi-cloud-fog',
        'Overcast': 'bi bi-cloud',
        'Partially cloudy': 'bi bi-cloud-sun',
        'Rain, Overcast': 'bi bi-cloud-rain',
        'Rain, Partially cloudy': 'bi bi-cloud-rain',
    }

    normalized_description = description.strip().lower()

    # Fallback for combined descriptions (e.g., "Rain, Overcast")
    if "," in normalized_description:
        conditions = [cond.strip().capitalize() for cond in normalized_description.split(",")]
        for condition in conditions:
            if condition in icon_map:
                return icon_map[condition]
        return 'bi bi-cloud'

    return icon_map.get(description.capitalize(), 'bi bi-cloud')

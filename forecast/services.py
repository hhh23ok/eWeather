# forecast/services.py
import csv
import json
import os
from collections import defaultdict
from datetime import timedelta, datetime
from asgiref.sync import sync_to_async
from django.utils import timezone
import requests
from prophet import Prophet
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from .models import WeatherData, Location
import pandas as pd

weather_api_base_url = "http://api.weatherapi.com/v1"


def fahrenheit_to_celsius(fahrenheit):
    return (fahrenheit - 32) * 5.0 / 9.0


def get_weather_forecast_visual_crossing(location_name: str, days: int = 7):
    # Replace with the actual API endpoint and API key
    base_url = ("https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"
                + location_name
                + "?key="
                + VISUAL_CROSSING_API_KEY)

    # print(base_url)

    response = requests.get(base_url)

    if response.status_code == 200:
        data = response.json()

        forecast_days = days
        forecast_data = []

        for day in data['days'][:forecast_days]:
            # print(day['conditions'])
            forecast_data.append({
                'date': day['datetime'],
                'tempmax': round(fahrenheit_to_celsius(day['tempmax']), 2),  # Convert to Celsius
                'tempmin': round(fahrenheit_to_celsius(day['tempmin']), 2),  # Convert to Celsius
                'windspeed': round(day['windspeed'], 2),
                'windgust': round(day['windgust'], 2),
                'precipprob': round(day['precipprob'], 2),
                'humidity': round(day['humidity'], 2),
                'uvindex': round(day['uvindex'], 2),
                'sunrise': day['sunrise'],
                'sunset': day['sunset'],
                'conditions': day['conditions']
            })

        for forecast_day in forecast_data:
            print(forecast_day)

        return forecast_data


def get_coordinates(location_name: str):
    """
    Get the latitude and longitude for a given location name using a geocoding API.
    """
    geocoding_url = f"https://api.opencagedata.com/geocode/v1/json"
    params = {
        "q": location_name,
        "key": GEOCODING_API_KEY,
        "limit": 1
    }

    response = requests.get(geocoding_url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            latitude = data['results'][0]['geometry']['lat']
            longitude = data['results'][0]['geometry']['lng']
            return latitude, longitude
        else:
            print("Location not found.")
            return None, None
    else:
        print(f"Geocoding API error: {response.status_code}")
        return None, None


def fetch_weather_data_stormglass(location_name: str, days: int = 7):
    """
    Fetch daily weather data from Storm Glass API for a given location name.
    """
    latitude, longitude = get_coordinates(location_name)
    if latitude is None or longitude is None:
        return

    # Calculate timestamps for start and end dates
    now = datetime.now(timezone.utc)
    start_timestamp = int(now.timestamp())
    end_timestamp = int((now + timedelta(days=days)).timestamp())

    stormglass_url = "https://api.stormglass.io/v2/weather/point"
    params = {
        "lat": latitude,
        "lng": longitude,
        "params": ",".join([
            "airTemperature", "gust", "humidity", "precipitation",
            "cloudCover", "windSpeed"
        ]),
        "start": start_timestamp,
        "end": end_timestamp,
        "resolution": "daily"
    }

    headers = {
        "Authorization": STORMGLASS_API_KEY
    }

    response = requests.get(stormglass_url, params=params, headers=headers)
    if response.status_code == 200:
        data = response.json()

        # Initialize a dictionary to store daily aggregates
        daily_aggregates = defaultdict(lambda: defaultdict(list))

        for day in data['hours']:
            timestamp = datetime.fromisoformat(day['time'].replace("Z", "+00:00")).timestamp()
            date = datetime.fromtimestamp(timestamp, timezone.utc).strftime('%Y-%m-%d')

            # Store each data point in the corresponding list
            daily_aggregates[date]['temp'].append(day.get('airTemperature', {}).get('sg', None))
            daily_aggregates[date]['gust'].append(day.get('gust', {}).get('sg', None))
            daily_aggregates[date]['humidity'].append(day.get('humidity', {}).get('sg', None))
            daily_aggregates[date]['precip'].append(day.get('precipitation', {}).get('sg', None))
            daily_aggregates[date]['cloudCover'].append(day.get('cloudCover', {}).get('sg', None))
            daily_aggregates[date]['windSpeed'].append(day.get('windSpeed', {}).get('sg', None))

        daily_data = []
        # Calculate averages for each day
        for date, values in daily_aggregates.items():
            daily_data = {
                'date': date,
                'temp': round(sum(values['temp']) / len(values['temp']), 2),
                'gust': round(sum(values['gust']) / len(values['gust']), 2),
                'humidity': round(sum(values['humidity']) / len(values['humidity']), 2),
                'precip': round(sum(values['precip']) / len(values['precip']), 2),
                'cloudCover': round(sum(values['cloudCover']) / len(values['cloudCover']), 2),
                'windSpeed': round(sum(values['windSpeed']) / len(values['windSpeed']), 2)
            }
            # print(daily_data)

        return daily_data
    else:
        print(f"Storm Glass API error: {response.status_code}")
        print(f"Response: {response.text}")


def combine_weather_forecasts(location: str, forecast_days_count: int = 7):
    print(f"Combining weather")
    visual_crossing_forecast = {}
    stormglass_forecast = {}
    try:
        # Attempt to fetch weather data from Storm Glass API
        stormglass_forecast = fetch_weather_data_stormglass(location, forecast_days_count)
        print(f"Retrieved {stormglass_forecast}")
    except Exception as e:
        print(f"Error fetching data from Storm Glass API: {e}")
        stormglass_forecast = None

    try:
        # If Storm Glass API fails, use Visual Crossing API as a fallback
        visual_crossing_forecast = get_weather_forecast_visual_crossing(location, forecast_days_count)
        # print(f"Retrieved {visual_crossing_forecast }")
        if stormglass_forecast is None:
            return visual_crossing_forecast
    except Exception as e:
        print(f"Error fetching data from Storm Glass API: {e}")
        stormglass_forecast = None

    # Initialize a combined forecast list
    combined_forecast = []

    for stormglass_day, visual_crossing_day in zip(stormglass_forecast, visual_crossing_forecast):
        # Averaging uvindex, precip, and gust if available in both forecasts
        avg_uvindex = round((stormglass_day.get('uvindex', 0) + visual_crossing_day.get('uvindex', 0)) / 2, 2)
        avg_precip = round((stormglass_day.get('precip', 0) + visual_crossing_day.get('precipprob', 0)) / 2, 2)
        avg_gust = round((stormglass_day.get('gust', 0) + visual_crossing_day.get('windgust', 0)) / 2, 2)

        # Add the averaged data to the combined forecast
        combined_forecast.append({
            'date': stormglass_day['date'],  # Assuming the dates match up
            'tempmax': stormglass_day['temp'],  # Use stormglass_day['temp'] or visual_crossing_day['temp'] as needed
            'tempmin': stormglass_day['temp'],  # Use stormglass_day['temp'] or visual_crossing_day['temp'] as needed
            'windspeed': stormglass_day['windSpeed'],
            # Use stormglass_day['windSpeed'] or visual_crossing_day['windspeed'] as needed
            'windgust': avg_gust,
            'precipprob': avg_precip,
            'humidity': round((stormglass_day.get('humidity', 0) + visual_crossing_day.get('humidity', 0)) / 2,2),
            'uvindex': avg_uvindex,
            'sunrise': stormglass_day['sunrise'],  # Assuming similar structure
            'sunset': stormglass_day['sunset'],  # Assuming similar structure
            'conditions': stormglass_day['conditions'],  # Assuming similar structure
        })

    return combined_forecast


# -----------------------------------------------------------------------------

# ETL process for db.sqlite3
def update_stored_weather_data(location: str):
    # Get the current date and time
    today = timezone.now().date()

    # Define the cutoff date (120 days ago)
    cutoff_date = today - timedelta(days=120)

    # Delete weather data older than 120 days for the specific location
    WeatherData.objects.filter(location__city=location, date__lt=cutoff_date).delete()


def fetch_and_save_historical_data(location_name: str, start_date: str, end_date: str):
    location_instance, created = Location.objects.get_or_create(city=location_name)

    if created:
        print(f"New location created: {location_instance.city}")
    else:
        print(f"Location already exists: {location_instance.city}")

    # Visual Crossing API (API 1)
    base_url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location_instance.city}/{start_date}/{end_date}"
    api_url = f"{base_url}?key={VISUAL_CROSSING_API_KEY}"

    visual_crossing_response = requests.get(api_url)

    # WeatherAPI (API 2)
    endpoint = "/history.json"
    parameters = {
        "key": STORMGLASS_API_KEY,
        "q": location_instance.city,
        "dt": start_date,
        "end_dt": end_date
    }

    weather_api_response = requests.get(weather_api_base_url + endpoint, params=parameters)

    if visual_crossing_response.status_code == 200:
        try:
            visual_crossing_data = visual_crossing_response.json()
        except json.JSONDecodeError:
            print("Error decoding Visual Crossing JSON response. Using mock data.")
    else:
        print(f"Visual Crossing API failed with status code {visual_crossing_response.status_code}. Using mock data.")
        visual_crossing_data = fetch_mock_data(VISUAL_CROSSING_MOCK_FILE)

    if weather_api_response.status_code == 200:
        try:
            weather_api_data = weather_api_response.json()
            print("Weather API data:", weather_api_data)
        except json.JSONDecodeError:
            print("Error decoding WeatherAPI JSON response. Using mock data.")
            weather_api_data = fetch_mock_data(WEATHER_API_MOCK_FILE)
    else:
        print(f"WeatherAPI failed with status code {weather_api_response.status_code}. Using mock data.")
        weather_api_data = fetch_mock_data(WEATHER_API_MOCK_FILE)

    # weather_api_data = fetch_mock_data(WEATHER_API_MOCK_FILE)
    # visual_crossing_data = fetch_mock_data(VISUAL_CROSSING_MOCK_FILE)

    if weather_api_data:
        for forecast_data in weather_api_data['forecast']['forecastday']:
            for hour_data in forecast_data['hour']:
                # Extract relevant data
                date = datetime.strptime(hour_data['time'], '%Y-%m-%d %H:%M').date()
                time = datetime.strptime(hour_data['time'], '%Y-%m-%d %H:%M').time()

                # Check if weather data already exists for this date, time, and location
                existing_weather = WeatherData.objects.filter(
                    location=location_instance,
                    date=date,
                    time=time
                ).first()

                if not existing_weather:
                    # Extract additional fields from Visual Crossing response
                    # Add fields from Visual Crossing API response
                    sunrise = visual_crossing_data['days'][0].get('sunrise', None)
                    sunset = visual_crossing_data['days'][0].get('sunset', None)
                    conditions = visual_crossing_data['days'][0].get('conditions', None)
                    precipitation = visual_crossing_data['days'][0].get('precip', None)
                    precipitation_probability = visual_crossing_data['days'][0].get('precipprob', None)

                    wind_speed = visual_crossing_data['days'][0].get('windspeed', None)
                    wind_gust = visual_crossing_data['days'][0].get('windgust', None)

                    humidity = visual_crossing_data['days'][0].get('humidity', None)
                    pressure = visual_crossing_data['days'][0].get('pressure', None)
                    dew_point = visual_crossing_data['days'][0].get('dew', None)
                    feels_like = visual_crossing_data['days'][0].get('feelslike', None)
                    cloud_cover = visual_crossing_data['days'][0].get('cloudcover', None)
                    visibility = visual_crossing_data['days'][0].get('visibility', None)
                    uv_index = visual_crossing_data['days'][0].get('uvindex', None)

                    # Create a new weather data entry if it doesn't exist
                    weather = WeatherData(
                        location=location_instance,
                        date=date,
                        time=time,
                        temp_max=forecast_data['day']['maxtemp_c'],
                        temp_min=forecast_data['day']['mintemp_c'],
                        temp_current=hour_data['temp_c'],
                        will_it_rain=forecast_data['day'].get('daily_will_it_rain', False),
                        chance_of_rain=forecast_data['day'].get('daily_chance_of_rain', 0),
                        will_it_snow=forecast_data['day'].get('daily_will_it_snow', False),
                        chance_of_snow=forecast_data['day'].get('daily_chance_of_snow', 0),
                        sunrise=sunrise,
                        sunset=sunset,
                        conditions=conditions,
                        precipitation=precipitation,
                        precipitation_probability=precipitation_probability,
                        wind_speed=wind_speed,
                        wind_gust=wind_gust,
                        humidity=humidity,
                        pressure=pressure,
                        dew_point=dew_point,
                        feels_like=feels_like,
                        cloud_cover=cloud_cover,
                        visibility=visibility,
                        uv_index=uv_index
                    )
                    weather.save()
                    print(f"Saved weather data for {weather.date} {weather.time}")
                # else:
                #     # print(f"Weather data for {date} {time} already exists.")
    else:
        print("No historical data found from WeatherAPI.")


def load_historical_weather(location: str):
    # Get today's date and the date 15 days ago
    today = timezone.now().date()
    start_date = today - timedelta(days=15)
    fetch_and_save_historical_data(location, start_date, today)


def load_from_db(location_name: str):
    location_instance = Location.objects.get(city=location_name)
    weather_data = WeatherData.objects.filter(location=location_instance).order_by('date', 'time')
    df = pd.DataFrame(list(weather_data.values()))

    # Ensure the 'datetime' column exists and convert it to datetime format
    if 'datetime' not in df.columns:
        df['datetime'] = pd.to_datetime(df['date'].astype(str) + ' ' + df['time'].astype(str), errors='coerce')

    # Convert 'date' and 'time' separately if they are in different columns
    df['date'] = pd.to_datetime(df['date'])
    df['time'] = pd.to_datetime(df['time'], format='%H:%M:%S').dt.time

    return df


def check_missing_values(df):
    missing_values = df.isna().sum()

    for column, missing_count in missing_values.items():
        if missing_count > 0:
            print(f"Column: {column}, Missing Values: {missing_count}")


# -----------------------FORECAST-----------------------
def prophet_forecast(df, column_name):
    df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')

    if 'datetime' not in df.columns:
        raise KeyError("DataFrame does not have a 'datetime' column")

    # Convert 'datetime' to datetime format
    df['datetime'] = pd.to_datetime(df['datetime'])

    # Prepare the DataFrame for Prophet
    df_prophet = df[['datetime', column_name]].rename(columns={'datetime': 'ds', column_name: 'y'})

    # Initialize and fit the model
    model = Prophet()
    model.fit(df_prophet)

    # Forecast for the next 7 days
    future = model.make_future_dataframe(periods=7, freq='D')
    forecast = model.predict(future)

    # Print the forecasted values for the next 7 days
    forecasted_values = forecast[['ds', 'yhat']].tail(7)
    # print(f"Forecasted {column_name} for the next 7 days:")
    # print(forecasted_values)

    return forecasted_values


def prepare_data_rand_forest(df):
    df['datetime'] = pd.to_datetime(df['datetime'])
    df.set_index('datetime', inplace=True)

    # Encode categorical variables
    label_encoder = LabelEncoder()
    df['conditions'] = label_encoder.fit_transform(df['conditions'])

    # Select features and target variable
    features = df[['temp_max', 'temp_min', 'temp_current',
                   'chance_of_rain', 'chance_of_snow', 'precipitation',
                   'humidity', 'pressure', 'wind_speed', 'wind_gust',
                   'cloud_cover', 'visibility', 'uv_index']]
    target = df['conditions']

    return features, target, label_encoder


# Function to make predictions for the next 7 days
def predict_conditions_rand_forest(df):
    features, target, label_encoder = prepare_data_rand_forest(df)

    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

    # Train RandomForest model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Predict for the next 7 days
    last_known_data = features.iloc[-1].to_frame().T  # Ensure it's a DataFrame with correct feature names
    forecast_dates = pd.date_range(start=features.index[-1], periods=8, freq='D')[1:]
    predictions = []

    for date in forecast_dates:
        pred = model.predict(last_known_data)[0]
        predictions.append((date, label_encoder.inverse_transform([pred])[0]))
        # Update last_known_data with the latest prediction if needed
        # last_known_data = update_last_known_data(last_known_data, new_info)
    # print("Predictions for the next 7 days:")
    # for date, condition in predictions:
    #     print(f"Date: {date}, Condition: {condition}")

    return predictions


def generate_daily_forecast(location: str):
    print(location, "is in generate_daily_forecast;")

    # Fetch combined weather forecasts from APIs
    combined_api_forecast = combine_weather_forecasts(location)

    # Ensure the database is updated with the latest data
    yesterday = (datetime.now() - timedelta(days=1)).date()
    df = load_from_db(location)

    if df.empty or yesterday not in df['date'].values:
        print(f"No data for {location} on {yesterday}. Updating historical data.")
        print("--------------------")
        load_historical_weather(location)
        print("--------------------")

    df = load_from_db(location)

    # Predict numerical data
    temp_max_forecast = prophet_forecast(df, 'temp_max')
    temp_min_forecast = prophet_forecast(df, 'temp_min')
    uv_index_forecast = prophet_forecast(df, 'uv_index')
    wind_gust_forecast = prophet_forecast(df, 'wind_gust')

    # Extract latest forecast values
    max_temperature_pred = temp_max_forecast['yhat'].iloc[-1] if not temp_max_forecast.empty else None
    min_temperature_pred = temp_min_forecast['yhat'].iloc[-1] if not temp_min_forecast.empty else None
    uv_index_pred = uv_index_forecast['yhat'].iloc[-1] if not uv_index_forecast.empty else None
    wind_gust_pred = wind_gust_forecast['yhat'].iloc[-1] if not wind_gust_forecast.empty else None

    # Predict categorical data
    predicted_conditions = predict_conditions_rand_forest(df)
    main_condition_pred = predicted_conditions[0][1] if predicted_conditions else 'N/A'

    # Take the first day from the combined API forecast
    combined_api_day = combined_api_forecast[0] if combined_api_forecast else {}

    # Weighted average calculation with weights 0.6 for real data and 0.3 for predicted data
    def weighted_avg(real_val, pred_val):
        if real_val is not None and pred_val is not None:
            return round(0.6 * real_val + 0.3 * pred_val, 2)
        return real_val if real_val is not None else pred_val

    # Create forecast list with dictionaries
    forecast = []
    for i, combined_day in enumerate(combined_api_forecast):
        forecast.append({
            'date': combined_day['date'],  # Ensure the date is included
            'min_temperature': f"{weighted_avg(combined_day.get('tempmin'), min_temperature_pred)}°C",
            'max_temperature': f"{weighted_avg(combined_day.get('tempmax'), max_temperature_pred)}°C",
            'uv_index': f"{weighted_avg(combined_day.get('uvindex'), uv_index_pred)}",
            'wind_gust': f"{weighted_avg(combined_day.get('windgust'), wind_gust_pred)} km/h",
            'precip_prob': f"{combined_day.get('precipprob', 'N/A')}%",  # Add precipitation probability
            'condition': combined_day.get('conditions', main_condition_pred),
        })

    return forecast


@sync_to_async
def generate_daily_forecast_async(location: str):
    return generate_daily_forecast(location)


async def generate_daily_forecast_tg(location: str):
    forecast_data = await generate_daily_forecast_async(location)
    return forecast_data

def check_extremal_conditions(weather):
    # Define thresholds
    temp_min, temp_max = -20, 35  # °C
    uv_index_max = 3  # Safe UV index
    wind_gust_max = 20  # Safe wind gust speed (in km/h)

    conditions = []

    # Helper function to safely convert to integer and handle errors
    def safe_int(value, default=None):
        try:
            return int(value.replace('°C', '').strip())
        except (ValueError, AttributeError):
            return default

    # Check if weather is a dictionary or a list and extract values accordingly
    if isinstance(weather, dict):
        temperature_max = safe_int(weather.get('max_temperature', ''), None)
        temperature_min = safe_int(weather.get('min_temperature', ''), None)
        wind_gust = safe_int(weather.get('wind_gust', '').split(' ')[0], None)
        uv_index = safe_int(weather.get('uv_index', '0'), 0)
    elif isinstance(weather, list) and len(weather) > 0 and isinstance(weather[0], dict):
        # Accessing values from the first dictionary in the list
        temperature_max = safe_int(weather[0].get('max_temperature', ''), None)
        temperature_min = safe_int(weather[0].get('min_temperature', ''), None)
        wind_gust = safe_int(weather[0].get('wind_gust', '').split(' ')[0], None)
        uv_index = safe_int(weather[0].get('uv_index', '0'), 0)
    else:
        # Handle unexpected structure
        temperature_max, temperature_min, wind_gust, uv_index = None, None, None, None

    if temperature_min is not None and temperature_min < temp_min:
        conditions.append(f"⚠️ Temperature ({temperature_min}°C) is extremely cold.")
    elif temperature_max is not None and temperature_max > temp_max:
        conditions.append(f"⚠️ Temperature ({temperature_max}°C) is extremely hot.")

    if uv_index is not None and uv_index > uv_index_max:
        conditions.append(f"⚠️ UV index ({uv_index}) is unsafe. Protect your skin!")

    if wind_gust is not None and wind_gust > wind_gust_max:
        conditions.append(f"⚠️ Wind gust ({wind_gust} km/h) is strong. Be cautious!")

    return conditions if conditions else ["✅ Weather conditions are safe."]

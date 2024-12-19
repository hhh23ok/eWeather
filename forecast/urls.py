# In forecast/urls.py
from django.urls import path
from . import views

app_name = 'forecast'

urlpatterns = [
    path("forecast", views.forecast_days, name="forecast_days"),  # Fixed path
]

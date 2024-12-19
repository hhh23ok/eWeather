# In weather_app/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("main.urls")),
    path("users/", include("users.urls")),
    path("weather/", include("forecast.urls")),
    path("news/", include("news.urls")),
    path('accounts/', include('allauth.urls')),  # allauth URL
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

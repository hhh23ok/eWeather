from django.urls import path, include
from . import views

app_name = 'users'

urlpatterns = [
    path("account/", views.account, name="account"),
    path('location/<int:id>/delete/', views.location_delete, name='location_delete'),
    path('', include('allauth.urls'))
]

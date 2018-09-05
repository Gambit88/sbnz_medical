from django.urls import path

from . import views


urlpatterns = [
    path('<int:patient_id>/', views.something),
    path('alarms/', views.something),
]
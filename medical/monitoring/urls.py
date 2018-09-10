from django.urls import path

from . import views


urlpatterns = [
    path('<int:patient_id>/', views.something),
    path('alarms/', views.something,name='monitoringPage'),
    path('alarms/solve/<int:alarm_id>', views.something,name='solveAlarm'),
]
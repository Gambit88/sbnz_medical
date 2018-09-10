from django.urls import path

from . import views


urlpatterns = [
    path('<int:patient_id>/', views.info),
    path('alarms/', views.getPage,name='monitoringPage'),
    path('alarms/solve/<int:alarm_id>', views.solve,name='solveAlarm'),
]
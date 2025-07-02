from django.urls import path
from . import views

app_name = 'dashboard_app'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('api/chart-data/', views.get_chart_data, name='chart_data'),
    path('api/stats/', views.get_stats, name='stats'),
] 
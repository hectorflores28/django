from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import random
from datetime import datetime, timedelta

@login_required
def dashboard_view(request):
    """Vista principal del dashboard"""
    context = {
        'user': request.user,
        'page_title': 'Dashboard de Datos'
    }
    return render(request, 'dashboard_app/dashboard.html', context)

@login_required
def get_chart_data(request):
    """API para obtener datos de gráficos"""
    chart_type = request.GET.get('type', 'sales')
    
    if chart_type == 'sales':
        # Datos de ventas mensuales
        months = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
        data = {
            'labels': months,
            'datasets': [{
                'label': 'Ventas 2024',
                'data': [12000, 19000, 15000, 25000, 22000, 30000, 28000, 35000, 32000, 40000, 38000, 45000],
                'backgroundColor': 'rgba(54, 162, 235, 0.2)',
                'borderColor': 'rgba(54, 162, 235, 1)',
                'borderWidth': 2
            }]
        }
    elif chart_type == 'users':
        # Datos de usuarios activos
        days = [(datetime.now() - timedelta(days=i)).strftime('%d/%m') for i in range(30, 0, -1)]
        data = {
            'labels': days,
            'datasets': [{
                'label': 'Usuarios Activos',
                'data': [random.randint(800, 1200) for _ in range(30)],
                'backgroundColor': 'rgba(75, 192, 192, 0.2)',
                'borderColor': 'rgba(75, 192, 192, 1)',
                'borderWidth': 2
            }]
        }
    elif chart_type == 'revenue':
        # Datos de ingresos por categoría
        categories = ['Productos', 'Servicios', 'Consultoría', 'Soporte', 'Otros']
        data = {
            'labels': categories,
            'datasets': [{
                'label': 'Ingresos por Categoría',
                'data': [45, 25, 15, 10, 5],
                'backgroundColor': [
                    'rgba(255, 99, 132, 0.8)',
                    'rgba(54, 162, 235, 0.8)',
                    'rgba(255, 205, 86, 0.8)',
                    'rgba(75, 192, 192, 0.8)',
                    'rgba(153, 102, 255, 0.8)'
                ]
            }]
        }
    else:
        data = {'error': 'Tipo de gráfico no válido'}
    
    return JsonResponse(data)

@login_required
def get_stats(request):
    """API para obtener estadísticas generales"""
    stats = {
        'total_users': 1250,
        'active_users': 892,
        'total_revenue': 1250000,
        'monthly_growth': 12.5,
        'conversion_rate': 3.2,
        'avg_session_duration': 8.5
    }
    return JsonResponse(stats)

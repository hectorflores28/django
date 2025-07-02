from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.signing import Signer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from .models import CustomUser
import json

def login_view(request):
    """Vista de login personalizada con encriptación"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            # Intentar autenticar con el usuario personalizado
            try:
                user = CustomUser.objects.get(username=username)
                if user.check_password(password):
                    login(request, user)
                    messages.success(request, f'Bienvenido {username}!')
                    return redirect('dashboard')
                else:
                    messages.error(request, 'Usuario o contraseña incorrectos')
            except ObjectDoesNotExist:
                messages.error(request, 'Usuario no encontrado')
        else:
            messages.error(request, 'Por favor complete todos los campos')
    
    return render(request, 'auth_app/login.html')

_requ@loginired
def logout_view(request):
    """Vista de logout"""
    logout(request)
    messages.info(request, 'Has cerrado sesión exitosamente')
    return redirect('login')

def forgot_password_view(request):
    """Vista para recuperar contraseña"""
    if request.method == 'POST':
        username = request.POST.get('username')
        new_password = request.POST.get('new_password')
        
        if username and new_password:
            try:
                user = CustomUser.objects.get(username=username)
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Contraseña actualizada exitosamente')
                return redirect('login')
            except ObjectDoesNotExist:
                messages.error(request, 'Usuario no encontrado')
        else:
            messages.error(request, 'Por favor complete todos los campos')
    
    return render(request, 'auth_app/forgot_password.html')

@csrf_exempt
def create_user_api(request):
    """API para crear usuarios desde el portal de gestión"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            email = data.get('email', '')
            
            if username and password:
                # Verificar si el usuario ya existe
                if CustomUser.objects.filter(username=username).exists():
                    return JsonResponse({'error': 'El usuario ya existe'}, status=400)
                
                # Crear nuevo usuario
                user = CustomUser.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )
                user.save()
                
                return JsonResponse({
                    'success': True,
                    'message': f'Usuario {username} creado exitosamente',
                    'user_id': user.id
                })
            else:
                return JsonResponse({'error': 'Username y password son requeridos'}, status=400)
                
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.signing import Signer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .models import CustomUser, PasswordResetToken
import json

def login_view(request):
    """Vista de login personalizada con email y contraseña"""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if email and password:
            # Buscar usuario por email
            try:
                user = CustomUser.objects.get(email=email)
                if user.check_password(password):
                    login(request, user)
                    messages.success(request, f'Bienvenido {user.username}!')
                    return redirect('dashboard_app:dashboard')
                else:
                    messages.error(request, 'Email o contraseña incorrectos')
            except ObjectDoesNotExist:
                messages.error(request, 'Email no encontrado')
        else:
            messages.error(request, 'Por favor complete todos los campos')
    
    return render(request, 'auth_app/login.html')

@login_required
def logout_view(request):
    """Vista de logout"""
    logout(request)
    messages.info(request, 'Has cerrado sesión exitosamente')
    return redirect('auth_app:login')

def forgot_password_view(request):
    """Vista para solicitar reset de contraseña"""
    if request.method == 'POST':
        email = request.POST.get('email')
        
        if email:
            try:
                user = CustomUser.objects.get(email=email)
                
                # Crear token de reset
                reset_token = PasswordResetToken.create_token(user)
                
                # Construir URL de reset
                reset_url = request.build_absolute_uri(
                    f'/auth/reset-password/{reset_token.token}/'
                )
                
                # Enviar email
                subject = 'Recuperación de Contraseña'
                html_message = render_to_string('auth_app/email_reset_password.html', {
                    'user': user,
                    'reset_url': reset_url,
                })
                plain_message = strip_tags(html_message)
                
                try:
                    send_mail(
                        subject,
                        plain_message,
                        settings.DEFAULT_FROM_EMAIL,
                        [email],
                        html_message=html_message,
                        fail_silently=False,
                    )
                    messages.success(request, 'Se ha enviado un email con instrucciones para recuperar tu contraseña')
                except Exception as e:
                    messages.error(request, f'Error al enviar el email: {str(e)}')
                
            except ObjectDoesNotExist:
                # Por seguridad, no revelamos si el email existe o no
                messages.success(request, 'Si el email existe, se ha enviado un correo con instrucciones')
        else:
            messages.error(request, 'Por favor ingrese su email')
    
    return render(request, 'auth_app/forgot_password.html')

def reset_password_view(request, token):
    """Vista para resetear contraseña con token"""
    # Obtener el token
    try:
        reset_token = PasswordResetToken.objects.get(token=token)
        
        if not reset_token.is_valid():
            messages.error(request, 'El enlace de recuperación ha expirado o ya fue usado')
            return redirect('auth_app:login')
        
        if request.method == 'POST':
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            
            if password and confirm_password:
                if password == confirm_password:
                    # Actualizar contraseña
                    user = reset_token.user
                    user.set_password(password)
                    user.save()
                    
                    # Marcar token como usado
                    reset_token.mark_as_used()
                    
                    messages.success(request, 'Contraseña actualizada exitosamente. Puede iniciar sesión ahora.')
                    return redirect('auth_app:login')
                else:
                    messages.error(request, 'Las contraseñas no coinciden')
            else:
                messages.error(request, 'Por favor complete todos los campos')
        
        return render(request, 'auth_app/reset_password.html', {'token': token})
        
    except ObjectDoesNotExist:
        messages.error(request, 'Enlace de recuperación inválido')
        return redirect('auth_app:login')

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
                
                if email and CustomUser.objects.filter(email=email).exists():
                    return JsonResponse({'error': 'El email ya está registrado'}, status=400)
                
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

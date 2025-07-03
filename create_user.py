#!/usr/bin/env python
"""
Script para crear el usuario "toto" con las credenciales especificadas
Usando el sistema estándar de Django para encriptación de contraseñas
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from auth_app.models import CustomUser

def create_toto_user():
    """Crea el usuario toto con las credenciales especificadas"""
    
    # Datos del usuario
    username = 'toto'
    email = 'hflores@velasresorts.com'
    password = 'test123'
    
    try:
        # Verificar si el usuario ya existe
        if CustomUser.objects.filter(username=username).exists():
            print(f"El usuario '{username}' ya existe.")
            user = CustomUser.objects.get(username=username)
            
            # Actualizar email si es necesario
            if user.email != email:
                user.email = email
                user.save()
                print(f"Email actualizado a: {email}")
            
            # Actualizar contraseña usando el sistema estándar de Django
            # set_password() automáticamente encripta la contraseña con pbkdf2_sha256
            print(f"Actualizando contraseña para el usuario '{username}'...")
            user.set_password(password)
            user.save()
            print(f"✅ Contraseña actualizada usando encriptación estándar de Django")
            
        else:
            # Crear nuevo usuario usando el sistema estándar de Django
            # create_user() automáticamente encripta la contraseña
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password  # Django automáticamente encripta esto
            )
            print(f"Usuario '{username}' creado exitosamente")
            print(f"✅ Contraseña encriptada usando sistema estándar de Django")
        
        # Verificar que la contraseña funciona correctamente
        if user.check_password(password):
            print(f"✅ Verificación exitosa: la contraseña '{password}' es válida")
        else:
            print(f"❌ Error: la contraseña '{password}' no es válida")
            return False
        
        print("\n=== CREDENCIALES DE ACCESO ===")
        print(f"Email: {email}")
        print(f"Contraseña: {password}")
        print(f"Username: {username}")
        print("\n=== FLUJO DE ENCRIPTACIÓN ===")
        print("1. Usuario ingresa contraseña en texto plano")
        print("2. Django encripta con pbkdf2_sha256 y la guarda")
        print("3. Al validar, Django compara texto plano con hash")
        print("4. Nunca se desencripta, solo se compara")
        
    except Exception as e:
        print(f"Error al crear/actualizar el usuario: {str(e)}")
        return False
    
    return True

if __name__ == '__main__':
    print("=== CREANDO USUARIO 'toto' CON ENCRIPTACIÓN ESTÁNDAR ===")
    success = create_toto_user()
    
    if success:
        print("\n✅ Usuario creado/actualizado exitosamente!")
        print("Puedes usar estas credenciales para hacer login en el sistema.")
        print("La contraseña está encriptada de forma segura en la base de datos.")
    else:
        print("\n❌ Error al crear/actualizar el usuario.")
        sys.exit(1) 
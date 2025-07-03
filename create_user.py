#!/usr/bin/env python
"""
Script para crear el usuario "toto" con las credenciales especificadas
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
    email = 'hflores@gmail.com'
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
            
            # Actualizar contraseña
            user.set_password(password)
            user.save()
            print(f"Contraseña actualizada para el usuario '{username}'")
            
        else:
            # Crear nuevo usuario
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            print(f"Usuario '{username}' creado exitosamente")
            print(f"Email: {email}")
            print(f"Contraseña: {password}")
        
        print("\nCredenciales de acceso:")
        print(f"Email: {email}")
        print(f"Contraseña: {password}")
        print(f"Username: {username}")
        
    except Exception as e:
        print(f"Error al crear el usuario: {str(e)}")
        return False
    
    return True

if __name__ == '__main__':
    print("Creando usuario 'toto'...")
    success = create_toto_user()
    
    if success:
        print("\n✅ Usuario creado/actualizado exitosamente!")
        print("Puedes usar estas credenciales para hacer login en el sistema.")
    else:
        print("\n❌ Error al crear el usuario.")
        sys.exit(1) 
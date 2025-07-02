#!/usr/bin/env python
"""
Script para crear el usuario 'toto' con contraseña 'test123'
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from auth_app.models import CustomUser

def create_user():
    """Crear el usuario toto con contraseña test123"""
    try:
        # Verificar si el usuario ya existe
        if CustomUser.objects.filter(username='toto').exists():
            print("El usuario 'toto' ya existe.")
            return
        
        # Crear el usuario
        user = CustomUser.objects.create_user(
            username='toto',
            password='test123',
            email='toto@example.com',
            first_name='Toto',
            last_name='User'
        )
        
        print(f"Usuario 'toto' creado exitosamente con ID: {user.id}")
        print("Credenciales de acceso:")
        print("Usuario: toto")
        print("Contraseña: test123")
        
    except Exception as e:
        print(f"Error al crear el usuario: {e}")

if __name__ == '__main__':
    create_user() 
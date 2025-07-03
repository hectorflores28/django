#!/usr/bin/env python
"""
Script para verificar usuarios en la base de datos y actualizar la contraseña de 'toto'
Usando el sistema estándar de Django para encriptación de contraseñas
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from auth_app.models import CustomUser

def check_users():
    """Verificar usuarios en la base de datos"""
    print("=== USUARIOS EN LA BASE DE DATOS ===")
    
    users = CustomUser.objects.all()
    if not users:
        print("No hay usuarios en la base de datos")
        return
    
    for user in users:
        print(f"Username: {user.username}")
        print(f"Email: {user.email}")
        print(f"Is_active: {user.is_active}")
        print(f"Password hash: {user.password[:20]}...")
        print("-" * 40)
    
    # Verificar usuario específico
    print("\n=== VERIFICANDO USUARIO 'toto' ===")
    try:
        toto = CustomUser.objects.get(username='toto')
        print(f"Usuario 'toto' encontrado:")
        print(f"Email: {toto.email}")
        print(f"Is_active: {toto.is_active}")
        
        # Probar contraseña usando el sistema estándar de Django
        test_password = 'test123'
        print(f"\n=== VERIFICANDO CONTRASEÑA '{test_password}' ===")
        
        if toto.check_password(test_password):
            print(f"✅ Contraseña '{test_password}' es correcta")
            print("✅ El sistema de encriptación funciona correctamente")
        else:
            print(f"❌ Contraseña '{test_password}' es incorrecta")
            print("Actualizando contraseña de 'toto' a 'test123'...")
            
            # Usar el sistema estándar de Django para actualizar la contraseña
            toto.set_password(test_password)
            toto.save()
            
            # Verificar que la actualización funcionó
            if toto.check_password(test_password):
                print(f"✅ Contraseña de 'toto' actualizada correctamente a '{test_password}'")
                print("✅ Ahora puedes hacer login con estas credenciales")
            else:
                print(f"❌ Error al actualizar la contraseña de 'toto'")
            
    except CustomUser.DoesNotExist:
        print("❌ Usuario 'toto' no encontrado")

def explain_encryption_flow():
    """Explicar el flujo de encriptación de Django"""
    print("\n" + "="*50)
    print("FLUJO DE ENCRIPTACIÓN DE CONTRASEÑAS EN DJANGO")
    print("="*50)
    print("1. USUARIO INGRESA CONTRASEÑA:")
    print("   - Usuario escribe: 'test123' (texto plano)")
    print()
    print("2. DJANGO ENCRIPTA LA CONTRASEÑA:")
    print("   - Django usa pbkdf2_sha256 con salt único")
    print("   - Resultado: 'pbkdf2_sha256$600000$salt$hash...'")
    print("   - Se guarda en la base de datos")
    print()
    print("3. VALIDACIÓN DE CONTRASEÑA:")
    print("   - Usuario ingresa: 'test123' (texto plano)")
    print("   - Django encripta 'test123' con el mismo salt")
    print("   - Compara el hash resultante con el guardado")
    print("   - Si coinciden: ✅ Login exitoso")
    print("   - Si no coinciden: ❌ Login fallido")
    print()
    print("4. SEGURIDAD:")
    print("   - NUNCA se desencripta la contraseña guardada")
    print("   - Solo se compara el hash del texto plano con el hash guardado")
    print("   - Imposible recuperar la contraseña original desde la BD")
    print("="*50)

if __name__ == '__main__':
    check_users()
    explain_encryption_flow() 
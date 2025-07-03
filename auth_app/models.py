from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.signing import Signer
from django.conf import settings
import uuid
from datetime import datetime, timedelta

class CustomUser(AbstractUser):
    """Modelo de usuario personalizado con encriptación de contraseña"""
    
    # Campos adicionales si es necesario
    phone = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'custom_user'
    
    def set_password(self, raw_password):
        """Encripta la contraseña antes de guardarla"""
        signer = Signer()
        encrypted_password = signer.sign(raw_password)
        super().set_password(encrypted_password)
    
    def check_password(self, raw_password):
        """Verifica la contraseña encriptada"""
        try:
            signer = Signer()
            # Primero intentamos verificar si la contraseña actual está encriptada
            if self.password.startswith('pbkdf2_sha256$'):
                # Si es un hash de Django, usamos el método estándar
                return super().check_password(raw_password)
            else:
                # Si es nuestra encriptación personalizada
                decrypted_password = signer.unsign(self.password)
                return raw_password == decrypted_password
        except:
            return False
    
    def __str__(self):
        return self.username

class PasswordResetToken(models.Model):
    """Modelo para manejar tokens de reset de contraseña"""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'password_reset_token'
    
    def is_valid(self):
        """Verifica si el token es válido (no usado y no expirado)"""
        # Token válido por 24 horas
        expiration_time = self.created_at + timedelta(hours=24)
        return not self.used and datetime.now() < expiration_time
    
    def mark_as_used(self):
        """Marca el token como usado"""
        self.used = True
        self.save()
    
    @classmethod
    def create_token(cls, user):
        """Crea un nuevo token para un usuario"""
        # Eliminar tokens anteriores del usuario
        cls.objects.filter(user=user).update(used=True)
        
        # Crear nuevo token
        token = str(uuid.uuid4())
        return cls.objects.create(user=user, token=token)
    
    def __str__(self):
        return f"Token para {self.user.username} - {'Usado' if self.used else 'Válido'}"

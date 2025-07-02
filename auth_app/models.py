from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.signing import Signer
from django.conf import settings

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

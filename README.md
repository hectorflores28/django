# Dashboard de Datos con Autenticación Django

Un dashboard moderno y responsive que muestra gráficos de datos estáticos con sistema de autenticación personalizado usando Django.

## Características

- 🔐 **Autenticación personalizada** con encriptación usando `django.core.signing`
- 📊 **Dashboard interactivo** con gráficos usando Chart.js
- 🎨 **Interfaz moderna** con Bootstrap 5 y Font Awesome
- 📱 **Diseño responsive** que funciona en todos los dispositivos
- 🔄 **Datos dinámicos** cargados via AJAX
- 🔑 **Recuperación de contraseña** integrada

## Estructura del Proyecto

```
django/
├── dashboard/                 # Configuración principal del proyecto
├── auth_app/                 # App de autenticación
│   ├── models.py            # Modelo de usuario personalizado
│   ├── views.py             # Vistas de login, logout, forgot password
│   └── urls.py              # URLs de autenticación
├── dashboard_app/           # App del dashboard
│   ├── views.py             # Vistas del dashboard y APIs
│   └── urls.py              # URLs del dashboard
├── templates/               # Templates HTML
│   ├── base.html           # Template base
│   ├── auth_app/           # Templates de autenticación
│   └── dashboard_app/      # Templates del dashboard
├── static/                  # Archivos estáticos
└── create_user.py          # Script para crear usuarios
```

## Instalación y Uso

### 1. Instalar dependencias
```bash
pip install django
```

### 2. Ejecutar migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Crear usuario de prueba
```bash
python create_user.py
```

### 4. Ejecutar el servidor
```bash
python manage.py runserver
```

### 5. Acceder al dashboard
- URL: http://127.0.0.1:8000/
- Usuario: `toto`
- Contraseña: `test123`

## Funcionalidades

### Autenticación
- **Login**: `/auth/login/`
- **Logout**: `/auth/logout/`
- **Recuperar contraseña**: `/auth/forgot-password/`
- **API para crear usuarios**: `/auth/api/create-user/`

### Dashboard
- **Dashboard principal**: `/dashboard/`
- **API de estadísticas**: `/dashboard/api/stats/`
- **API de gráficos**: `/dashboard/api/chart-data/?type=sales|users|revenue`

## Gráficos Disponibles

1. **Ventas Mensuales**: Gráfico de línea con datos de ventas del año
2. **Ingresos por Categoría**: Gráfico de dona con distribución de ingresos
3. **Usuarios Activos**: Gráfico de barras con usuarios activos (últimos 30 días)

## Estadísticas Mostradas

- Usuarios totales
- Usuarios activos
- Ingresos totales
- Crecimiento mensual

## Encriptación de Contraseñas

El sistema utiliza `django.core.signing` para encriptar las contraseñas:
- Las contraseñas se encriptan antes de guardarse en la base de datos
- La validación se realiza comparando la contraseña en texto plano con la versión desencriptada
- Compatible con el sistema de autenticación estándar de Django

## API para Gestión de Usuarios

```bash
# Crear usuario via API
curl -X POST http://127.0.0.1:8000/auth/api/create-user/ \
  -H "Content-Type: application/json" \
  -d '{"username": "nuevo_usuario", "password": "password123", "email": "user@example.com"}'
```

## Tecnologías Utilizadas

- **Backend**: Django 5.2.3
- **Base de datos**: SQLite
- **Frontend**: Bootstrap 5, Chart.js, Font Awesome
- **Autenticación**: Django Auth con modelo personalizado
- **Encriptación**: django.core.signing

## Notas de Seguridad

- Las contraseñas se encriptan usando `django.core.signing`
- El sistema valida las credenciales en texto plano pero compara con la versión encriptada
- Se incluye protección CSRF en todos los formularios
- Las sesiones se manejan de forma segura con Django

## Desarrollo

Para agregar nuevos gráficos o estadísticas:

1. Modificar `dashboard_app/views.py` para agregar nuevos endpoints
2. Actualizar `templates/dashboard_app/dashboard.html` para mostrar nuevos gráficos
3. Agregar JavaScript correspondiente en el template

## Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

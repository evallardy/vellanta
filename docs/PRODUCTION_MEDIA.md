Configuración recomendada para servir STATIC y MEDIA en producción

1) Archivos estáticos (STATIC)
- Usa WhiteNoise para servir los archivos estáticos desde Django (útil en Heroku/similares).
- Instala: `pip install whitenoise`
- En `settings.py`:
  - Añadir `'whitenoise.middleware.WhiteNoiseMiddleware'` como primer middleware después de `SecurityMiddleware`.
  - `STATIC_ROOT = BASE_DIR / 'staticfiles'`
  - Ejecutar `python manage.py collectstatic` en despliegue.

2) Archivos cargados por usuarios (MEDIA)
- No se recomienda servir MEDIA desde Django en producción.
- Opciones recomendadas:
  - Subir a un bucket S3 (django-storages + boto3): `pip install django-storages[boto3]`
  - Configurar `DEFAULT_FILE_STORAGE` a `storages.backends.s3boto3.S3Boto3Storage` y variables de entorno para credenciales.
- Si necesitas servir MEDIA desde Django en una máquina propia, configura el servidor web (Nginx) para apuntar `MEDIA_URL` a la carpeta `MEDIA_ROOT` y que sirva archivos directamente.

3) Ejemplo mínimo de `settings.py` para producción con WhiteNoise (STATIC) y S3 comentado (no actives sin configurar credenciales):

```python
# Static files
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # ... resto del middleware
]

# Media (local, solo si es necesario)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Para usar S3 (ejemplo, requiere django-storages y credenciales)
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
# AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
```

4) Recordatorio
- En `vellanta/urls.py` ya añadimos el `static()` para servir `MEDIA` durante `DEBUG=True`.
- Asegúrate de no exponer credenciales en el repositorio y usar variables de entorno en producción.

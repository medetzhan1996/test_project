import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

SECRET_KEY = '*+rasdasddaxcvcwa3s7s@rdrfxcasoiumo'

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [STATIC_DIR]

import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

SECRET_KEY = '*+asdasdx#dsf^dsfg!vzo'

DEBUG = False

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'test_project_db',
        'USER': 'medet',
        'PASSWORD': 'medet-2021',
        'HOST': 'localhost',
        'PORT': '5432'
    }
}

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

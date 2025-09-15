from .base import *


ALLOWED_HOSTS = [
    '127.0.0.1',       #
    'localhost',
    'codefuse.sevalla.app',
    '*',

]
CSRF_TRUSTED_ORIGINS = [
    'https://yourdomain.com',
    'http://127.0.0.1:8000', 
    'https://codefuse.sevalla.app', # if testing locally
]





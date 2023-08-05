DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'djangobulk',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': 'localhost',
    }
}

INSTALLED_APPS = [
    'djangobulk',
]

MIDDLEWARE_CLASSES = tuple()

SECRET_KEY = 'lDg4H%065EQTllx#@roY@v98Jg1DCKMnGvhTJcxlS09H2b*t9C%zq*GCcxk'

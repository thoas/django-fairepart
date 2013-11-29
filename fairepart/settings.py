from django.conf import settings


BACKENDS = getattr(settings, 'FAIREPART_BACKENDS', (
    'fairepart.backends.facebook.FacebookBackend',
    'fairepart.backends.google.GoogleBackend',
))

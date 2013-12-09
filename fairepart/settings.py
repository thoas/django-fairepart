from django.conf import settings


BACKENDS = getattr(settings, 'FAIREPART_BACKENDS', (
    'fairepart.backends.facebook.FacebookBackend',
    'fairepart.backends.google.GoogleOAuth2Backend',
))

RELATION_LIST_PAGINATE_BY = getattr(settings, 'FAIREPART_RELATION_LIST_PAGINATE_BY', 5)

GOOGLE_APP_NAME = getattr(settings, 'FAIREPART_GOOGLE_APP_NAME', '')

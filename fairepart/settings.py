from django.conf import settings


BACKENDS = getattr(settings, 'FAIREPART_BACKENDS', (
    'fairepart.backends.facebook.FacebookBackend',
    'fairepart.backends.google.GoogleBackend',
))

RELATION_LIST_PAGINATE_BY = getattr(settings, 'FAIREPART_RELATION_LIST_PAGINATE_BY', 5)

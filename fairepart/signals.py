from django.dispatch import Signal


relation_linked = Signal(providing_args=['instance', 'user'])

relation_joined = Signal(providing_args=['instance', 'user'])

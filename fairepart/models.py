from random import random

from hashlib import sha1 as sha_constructor

import django

from django.db import models
from django.db.models import signals
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.conf import settings

from social.apps.django_app.default.fields import JSONField
from social.apps.django_app.default.models import UID_LENGTH, UserSocialAuth

from .signals import relation_linked, relation_joined


class RelationManager(models.Manager):
    def contribute_to_class(self, cls, name):
        signals.post_save.connect(self.post_save, sender=cls)

        super(RelationManager, self).contribute_to_class(cls, name)

    def post_save(self, instance, *args, **kwargs):
        if kwargs.get('created', False) and instance.to_user_id:
            relation_linked.send(sender=instance.__class__,
                                 instance=instance,
                                 user=instance.to_user)


class Relation(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='relations_sent')
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                related_name='relations_received',
                                null=True,
                                blank=True)
    provider = models.CharField(max_length=32, db_index=True)
    uid = models.CharField(max_length=UID_LENGTH, db_index=True)
    extra_data = JSONField()

    objects = RelationManager()

    class Meta:
        """Meta data"""
        unique_together = ('from_user', 'provider', 'uid')
        db_table = 'fairepart_relation'

    def is_uid_email(self):
        try:
            validate_email(self.uid)
        except ValidationError:
            return False
        else:
            return True


class Invitation(models.Model):
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='invitations_sent')
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                related_name='invitations_received',
                                null=True,
                                blank=True)
    email = models.EmailField()
    text = models.TextField(blank=True, null=True)
    token = models.CharField(max_length=40)

    class Meta:
        db_table = 'fairepart_invitation'

    def save(self, *args, **kwargs):
        if not self.token:
            salt = sha_constructor(str(random())).hexdigest()[:5]

            self.token = sha_constructor(salt + self.email).hexdigest()

        return super(Invitation, self).save(*args, **kwargs)


def handle_user(sender, instance, *args, **kwargs):
    if kwargs.get('created', False) and instance.email:
        relations = Relation.objects.filter(uid=instance.email, to_user__isnull=True)

        for relation in relations:
            relation.to_user = instance

            relation_joined.send(sender=Relation,
                                 instance=relation,
                                 user=instance)

        relations.update(to_user=instance)


def handle_user_social_auth(sender, instance, *args, **kwargs):
    if kwargs.get('created', False) and instance.uid:
        relations = Relation.objects.filter(uid=instance.uid, to_user__isnull=True)

        for relation in relations:
            relation.to_user = instance.user

            relation_joined.send(sender=Relation,
                                 instance=relation,
                                 user=instance.user)

        relations.update(to_user=instance.user)


signals.post_save.connect(handle_user_social_auth, sender=UserSocialAuth)

if django.VERSION < (1, 7):
    from .compat import User

    signals.post_save.connect(handle_user, sender=User)
else:
    from django.apps import apps

    if apps.ready:
        from .compat import User

        signals.post_save.connect(handle_user, sender=User)

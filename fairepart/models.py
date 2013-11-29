from django.db import models
from django.db.models import signals

from social.apps.django_app.default.fields import JSONField
from social.apps.django_app.default.models import UID_LENGTH, UserSocialAuth

from .compat import User
from .signals import relation_linked


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
    from_user = models.ForeignKey(User, related_name='relations_sent')
    to_user = models.ForeignKey(User,
                                related_name='relations_received',
                                null=True,
                                blank=True)
    email = models.EmailField(null=True, blank=True)
    provider = models.CharField(max_length=32, db_index=True)
    uid = models.CharField(max_length=UID_LENGTH, db_index=True)
    extra_data = JSONField()

    objects = RelationManager()

    class Meta:
        """Meta data"""
        unique_together = ('from_user', 'provider', 'uid')
        db_table = 'fairepart_relation'


def handle_user_social_auth(sender, instance, *args, **kwargs):
    if kwargs.get('created', False) and instance.uid:
        relations = Relation.objects.filter(uid=instance.uid)

        for relation in relations:
            relation.to_user = instance.user

            relation_linked.send(sender=Relation,
                                 instance=relation,
                                 user=instance.user)

        relations.update(to_user=instance.user)


signals.post_save.connect(handle_user_social_auth, sender=UserSocialAuth)

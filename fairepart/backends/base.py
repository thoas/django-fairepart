from ..exceptions import ProviderDoesNotExist
from ..models import Relation, UserSocialAuth


class BaseBackend(object):
    model = Relation

    def get_social_auth(self, user):
        model = self.get_social_model()

        try:
            return model.objects.get(user=user,
                                     provider=self.name)
        except model.DoesNotExist:
            raise ProviderDoesNotExist(self, 'SocialAuth instance does not exists for provider %s' % self.name)

    def get_social_model(self):
        return UserSocialAuth

    def import_from_user(self, user):
        raise NotImplementedError

    def get_relations(self, user):
        return self.model.objects.filter(from_user=user,
                                         provider=self.name)

    def imports(self, data):
        for entry in data:
            instance = self.model(**entry)
            instance.save()

    def get_social_auth_by_uids(self, uids):
        return self.get_social_model().objects.filter(uid__in=uids)

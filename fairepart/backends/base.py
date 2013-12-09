from ..exceptions import ProviderDoesNotExist, MissingParameter
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

    def get_access_token(self, user):
        social_auth = self.get_social_auth(user)

        extra_data = social_auth.extra_data

        access_token = extra_data.get('access_token', None)

        if not access_token:
            raise MissingParameter(self, 'access_token')

        return access_token

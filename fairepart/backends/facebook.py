import logging

from facepy import GraphAPI, FacepyError

from .base import BaseBackend

from ..exceptions import ImportFailed
from ..helpers import chunks

logger = logging.getLogger('fairepart')


class FacebookBackend(BaseBackend):
    name = 'facebook'
    title = 'Facebook'

    def import_from_user(self, user):
        access_token = self.get_access_token(user)

        relations = dict((relation.uid, relation)
                         for relation in self.get_relations(user))

        try:
            friends = self.get_friends(access_token)
        except FacepyError as e:
            logger.exception(e)

            raise ImportFailed(self, access_token, e.message)
        else:
            uids = {}

            for friend in friends['data']:
                if friend['id'] in relations:
                    continue

                data = {
                    'from_user': user,
                    'uid': friend['id'],
                    'name': friend['name'],
                    'provider': self.name
                }

                uids[friend['id']] = data

            for uid_list in chunks(uids.keys(), 10):
                socials = self.get_social_auth_by_uids(uid_list)

                for social in socials:
                    uids[social.uid]['to_user_id'] = social.user_id

            self.imports(uids.values())

    def get_friends(self, access_token):
        return GraphAPI(access_token).get('me/friends')

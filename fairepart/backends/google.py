from .base import BaseBackend

from atom.http import ProxiedHttpClient

import gdata.contacts.service

from .. import settings
from ..helpers import chunks


class OAuth2Token(object):
    def __init__(self, access_token):
        self.access_token = access_token

    def perform_request(self, *args, **kwargs):
        url = 'https://www.google.com/m8/feeds/contacts/default/full'
        http = ProxiedHttpClient()
        return http.request(
            'GET',
            url,
            headers={
                'Authorization': 'OAuth %s' % self.access_token
            }
        )


class GoogleOAuth2Backend(BaseBackend):
    name = 'google-oauth2'
    title = 'Google'

    def import_from_user(self, user):
        access_token = self.get_access_token(user)

        google = gdata.contacts.service.ContactsService(source=settings.GOOGLE_APP_NAME)
        google.current_token = OAuth2Token(access_token)
        feed = google.GetContactsFeed()

        relations = dict((relation.uid, relation)
                         for relation in self.get_relations(user))

        uids = {}

        for entry in feed.entry:
            if not all([entry.email, entry.title, entry.title.text]):
                continue

            for email in entry.email:
                if email.address in relations:
                    continue

                data = {
                    'from_user': user,
                    'uid': email.address,
                    'name': entry.title.text,
                    'provider': self.name
                }

                uids[email.address] = data

        for uid_list in chunks(uids.keys(), 10):
            socials = self.get_social_auth_by_uids(uid_list)

            for social in socials:
                uids[social.uid]['to_user_id'] = social.user_id

        self.imports(uids.values())

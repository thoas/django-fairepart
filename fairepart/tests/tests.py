from mock import patch

from django.test import TestCase
from django.conf import settings
from django.core.urlresolvers import reverse

from exam.decorators import fixture
from exam.cases import Exam

from fairepart.backends.facebook import FacebookBackend
from fairepart.models import Relation, UserSocialAuth, Invitation
from fairepart.compat import User

from facepy import GraphAPI


class FacebookBackendTests(Exam, TestCase):
    @fixture
    def user(self):
        return User.objects.create_user(username='thoas',
                                        email='florent@ulule.com',
                                        password='$ecret')

    @fixture
    def graph_user(self):
        graph = GraphAPI('%s|%s' % (settings.SOCIAL_AUTH_FACEBOOK_KEY,
                                    settings.SOCIAL_AUTH_FACEBOOK_SECRET))

        return graph.post('%s/accounts/test-users' % settings.SOCIAL_AUTH_FACEBOOK_KEY,
                          installed='true',
                          permissions=','.join(settings.SOCIAL_AUTH_FACEBOOK_SCOPE))

    @fixture
    def real_user_social_auth(self):
        return UserSocialAuth.objects.create(
            user=self.user,
            uid=self.graph_user['id'],
            provider='facebook',
            extra_data={
                'access_token': self.graph_user['access_token']
            }
        )

    @fixture
    def user_social_auth(self):
        return UserSocialAuth.objects.create(
            user=self.user,
            uid='662601795',
            provider='facebook',
            extra_data={
                'access_token': 'fake-one'
            }
        )

    def test_invite_view(self):
        self.client.login(username=self.user.username,
                          password='$ecret')

        response = self.client.get(reverse('fairepart_invite'))

        self.assertTemplateUsed(response, 'fairepart/invite.html')
        self.assertEqual(response.status_code, 200)

    def test_invite_errors(self):
        self.client.login(username=self.user.username,
                          password='$ecret')

        email = 'dummy@localhost.fr'

        Invitation.objects.create(from_user=self.user, email=email)

        response = self.client.post(reverse('fairepart_invite'), data={
            'email': email
        })

        self.assertEqual(response.status_code, 200)

        self.assertIn('email', response.context['form'].errors)

    def test_invite_complete(self):
        self.client.login(username=self.user.username,
                          password='$ecret')

        email = 'dummy@localhost.fr'

        response = self.client.post(reverse('fairepart_invite'), data={
            'email': email
        })

        self.assertRedirects(
            response,
            reverse('fairepart_invite_done'),
            status_code=302,
            target_status_code=200
        )

        qs = Invitation.objects.filter(from_user=self.user, email=email)
        self.assertEqual(qs.count(), 1)

        invitation = qs.get()

        self.assertFalse(invitation.token is None)

    @patch.object(FacebookBackend, 'get_friends')
    def test_import_from_user(self, get_friends):
        get_friends.return_value = {
            'data': [{
                'name': "Alix Heuer",
                'id': "529318992"
            }]
        }

        self.client.login(username=self.user.username,
                          password='$ecret')

        self.user_social_auth

        response = self.client.get(reverse('fairepart_import', args=['facebook']))

        self.assertEqual(response.status_code, 302)

        self.assertEqual(Relation.objects.filter(from_user=self.user, provider='facebook').count(), 1)

    @patch.object(FacebookBackend, 'get_friends')
    def test_import_from_user_with_exisiting(self, get_friends):
        get_friends.return_value = {
            'data': [{
                'name': "Alix Heuer",
                'id': "529318992"
            }]
        }

        self.client.login(username=self.user.username,
                          password='$ecret')

        self.user_social_auth

        alix = User.objects.create_user('alix', 'alix@ulule.com', '$ecret')

        UserSocialAuth.objects.create(user=alix, uid=529318992)

        self.client.get(reverse('fairepart_import', args=['facebook']))

        self.assertEqual(Relation.objects.get(from_user=self.user, provider='facebook').to_user, alix)

    def test_relation_linked(self):
        uid = 529318992

        relation = Relation.objects.create(from_user=self.user, uid=uid, extra_data={
            'name': 'Alix Heuer'
        })

        alix = User.objects.create_user('alix', 'alix@ulule.com', '$ecret')

        UserSocialAuth.objects.create(user=alix, uid=uid)

        relation = Relation.objects.get(pk=relation.pk)

        self.assertEqual(relation.to_user, alix)

    def test_relation_list_view(self):
        self.client.login(username=self.user.username,
                          password='$ecret')

        response = self.client.get(reverse('fairepart_relation_list', args=['facebook', ]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'fairepart/relation_list.html')

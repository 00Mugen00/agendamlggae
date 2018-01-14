# -*- coding: utf-8 -*-

from urllib import urlencode
from google.appengine.api import memcache
from oauth2client import client
from models import Usuario, agenda_key
from tokens import create_jwt_token, get_user_from_token
from util import to_json
import webapp2


def based_on(decorator, service):
    """
    Adapted from https://github.com/google/google-api-python-client/blob/master/samples/appengine/main.py

    :param decorator: The decorator instance
    :param service: Service from apiclient.discovery.build
    :return: Tuple with OAuthLogin, OAuthLogout, OAuthTest classes
    """
    class OAuthLogin(webapp2.RequestHandler):

        @decorator.oauth_aware
        def get(self):
            # Retreive the original url from parameter or Referer header
            if 'url' in self.request.params:
                original_url = self.request.params['url']
            else:
                original_url = self.request.headers.get('referer')

            self.response.status_int = 301
            if decorator.has_credentials():
                # It is already logged in, so, store information about the user in ndb
                try:
                    # Retreive the original url from memcache or from the upper method
                    come_from = memcache.get('come_from')
                    original_url = come_from if come_from else original_url
                    memcache.delete('come_from')
                    # Get user's info
                    http = decorator.http()
                    user = service.people().get(userId="me").execute(http=http)
                    user_id = user[u'id']
                    # Register or modify the user in ndb
                    user_or_not = Usuario.query(Usuario.idGoogle == user_id).fetch()
                    if not user_or_not:
                        Usuario(
                            idGoogle=user[u'id'],
                            tipo=1,
                            preferencias=[],
                            extra=to_json(user),
                            parent=agenda_key()
                        ).put()
                        newcomer = True
                    else:
                        user_or_not[0].extra = to_json(user)
                        user_or_not[0].put()
                        newcomer = False

                    jwt_token = create_jwt_token(user_id)
                    if original_url:
                        self.redirect('{}?token={}&newcomer={}'.format(original_url, jwt_token, newcomer))
                    else:
                        newcomer = str(newcomer).lower()
                        self.response.headers['Content-Type'] = 'application/json; charset=utf8'
                        self.response.write(u'{{"token": "{}", "newcomer": {}}}'.format(jwt_token, newcomer))
                except client.AccessTokenRefreshError:
                    self.redirect(self.request.path_url + '?' + urlencode({'url', original_url}))
            else:
                # Redirect to Google Authentication page
                # TODO Make a better way to store the original_url, that is unique for any login
                memcache.set('come_from', original_url) if original_url else None
                self.redirect(decorator.authorize_url())

    class OAuthTest(webapp2.RequestHandler):

        def get(self):
            user, _ = get_user_from_token(self.request.GET['token']) if 'token' in self.request.GET else (None, None)
            newcomer = self.request.GET['newcomer'] if 'newcomer' in self.request.GET else False
            if user:
                self.response.write(u"""<html>
    <body>
        <p>{} {}, your user id is {} {}</p>
        <p><a href="/agendamlg-api/session/test">Logout</a></p>
    </body>
    </html>
                """.format(u'Welcome' if newcomer else u'Hello', user[u'displayName'], user[u'id'], _.tipo))
            else:
                self.response.write(u"""<html>
        <body>
            <p>I don't know you :/</p>
            <p><a href="/agendamlg-api/session/">Login</a></p>
        </body>
    </html>""")

    return OAuthLogin, OAuthTest

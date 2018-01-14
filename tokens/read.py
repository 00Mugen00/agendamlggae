import os

from oauth2client.contrib import appengine
from util.json import from_json
import tokens


def read_tokens():
    tokens_file = open('tokens/tokens.json', 'r')
    json = from_json(tokens_file.read())
    tokens_file.close()
    tokens.flickr_api_key = json[u'flickr_api_key']
    tokens.google_api_key = json[u'google_api_key']
    tokens.jwt_token = json[u'jwt_token']
    oauth_tokens_path = os.path.join(os.path.dirname(__file__), 'oauth_tokens.json')
    tokens.google_oauth_decorator = appengine.OAuth2DecoratorFromClientSecrets(
        oauth_tokens_path,
        scope=['https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile'],
        message='Check that the file `{}` exists in your project'.format(oauth_tokens_path),
        callback_path='/agendamlg-api/oauth2callback'
    )

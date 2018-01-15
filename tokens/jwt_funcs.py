# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
import jwt
from facades.excepcion import NotAuthenticatedException
from models import Usuario
from tokens import jwt_token
from util import from_json


def create_jwt_token(google_id):
    """
    Creates a JWT token from the necessary values inside the payload, using HS512 algorithm with key `tokens.jwt_token`

    :param google_id: The user's Google ID
    :return: The JWT token as `str`
    """
    return jwt.encode(
        { u'id': google_id, u'exp': datetime.utcnow() + timedelta(hours=1), u'iss': u'agendamlggae' },
        jwt_token,
        algorithm="HS512"
    )


def decode_jwt_token(token):
    """
    Decodes a JWT produced from 'create_jwt_token'. If 'token' is False-evaluable, returns None.

    :param token: JWT Token
    :return: dict with the payload stored inside it
    :raises: facades.exception.NotAuthenticatedException if the token has expired
    """
    if token:
        try:
            return jwt.decode(token, jwt_token, algorithms='HS512')
        except jwt.ExpiredSignatureError as e:
            raise NotAuthenticatedException.expirado(e)


def get_user_from_token(token, raise_for_unauthenticated=True):
    # type: (unicode|str, bool) -> (dict, Usuario)
    """
    Decodes a JWT produced from the header `bearer` and returns the tuple Google User object associated with it and
    the user from the database. The dictionary has the following structure:

        {
            "verified":false,
            "id":"<ID>",
            "kind":"plus#person",
            "displayName":"<NAME>",
            "etag":"\"<ETAG>\"",
            "cover": {
                ...
            },
            "language": "es",
            "emails": [
                {
                    "value":"<EMAIL>",
                    "type":"account"
                }
            ],
            "isPlusUser": false,
            "image": {
                "isDefault":false,
                "url":"<URL>?sz=50"
            },
            "name": {
                "familyName":"<FAMILY_NAME>",
                "givenName":"<GIVEN NAME>"
            },
            "objectType":"person"
        }

    :param token: JWT from `bearer` header
    :param raise_for_unauthenticated: if the token is invalid, raises the exception ('True' by default)
    :return: (dict, models.Usuario) or (None, None)
    :raises: facades.exception.NotAuthenticatedException if the token has expired
    :raises: facades.exception.NotAuthenticatedException if the token is invalid and must be valid
    """
    payload = decode_jwt_token(token)
    if payload:
        usuario = Usuario.query(Usuario.idGoogle == payload[u'id']).fetch()
        return from_json(usuario[0].extra), usuario[0]
    elif raise_for_unauthenticated:
        raise NotAuthenticatedException.no_autenticado()
    else:
        return None, None

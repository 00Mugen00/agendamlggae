# -*- coding: utf-8 -*-

"""
Contiene las excepciones que se usan en la aplicación
"""


class AgendamlgException(Exception):
    """When you try to do something and something is wrong with the request"""
    def __init__(self, mensaje_error, error_id, cause=None):
        super(AgendamlgException, self).__init__()
        self.mensaje_error = mensaje_error
        self.error_id = error_id
        self.cause = cause

    @staticmethod
    def tipo_invalido(tipo):
        return AgendamlgException(u'Tipo de evento inválido {}'.format(tipo), 1)

    @staticmethod
    def evento_ya_validado():
        return AgendamlgException(u"El evento ya ha sido validado", 2)

    @staticmethod
    def sin_permisos(usuario):
        return AgendamlgException(u"El usuario '{}' no tiene permisos para realizar esta acción".format(usuario), 3)

    @staticmethod
    def evento_campos_invalidos(t=None):
        return AgendamlgException(u"Hay campos inválidos en el evento", 4, t)

    @staticmethod
    def flickr_username_invalido(username):
        return AgendamlgException(u"El usuario de Flickr '{}' no se ha podido encontrar".format(username), 5)

    @staticmethod
    def comentario_campos_invalidos(t=None):
        # type: (Exception) -> AgendamlgException
        return AgendamlgException(u"Hay campos inválidos en el comentario", 6, t)

    @staticmethod
    def usuario_ya_ha_comentado(usuario, t=None):
        # type: (unicode|str, Exception) -> AgendamlgException
        return AgendamlgException(u"El usuario {} ya ha comentado este evento".format(usuario), 7, t)

    @staticmethod
    def otro_error(mensaje, t):
        return AgendamlgException(mensaje, 1000, t)


class AgendamlgNotFoundException(Exception):
    """When you try to do something and one parameter doesn't exist in the DB"""
    def __init__(self, mensaje_error, error_id):
        super(AgendamlgNotFoundException, self).__init__()
        self.mensaje_error = mensaje_error
        self.error_id = error_id

    @staticmethod
    def categoria_no_existe(cat_id):
        return AgendamlgNotFoundException(u'No existe la categoría "{}"'.format(cat_id), 10)

    @staticmethod
    def usuario_no_existe(id_google=None):
        if id_google is not None:
            return AgendamlgNotFoundException(u'No existe el usuario {}'.format(id_google), 11)
        else:
            return AgendamlgNotFoundException(u'No existe el usuario', 11)

    @staticmethod
    def evento_no_existe(evento_id):
        return AgendamlgNotFoundException(u'No existe el evento "{}"'.format(evento_id), 12)

    @staticmethod
    def comentario_no_existe(comentario_id):
        return AgendamlgNotFoundException(u'No existe el comentario para el evento "{}"'.format(comentario_id), 13)

    @staticmethod
    def me_gusta_no_existe(mg_id):
        return AgendamlgNotFoundException(u'No existe el me gusta "{}"'.format(mg_id), 14)


class NotAuthenticatedException(Exception):
    """
    When you try to access a REST API endpoint that requires the user to be authenticated
    """

    def __init__(self, mensaje, error_id, causa=None):
        super(NotAuthenticatedException, self).__init__()
        self.error_id = error_id
        self.mensaje = mensaje
        self.causa = causa

    @staticmethod
    def no_autenticado():
        return NotAuthenticatedException(u"Debe haber un usuario autenticado para usar este servicio", 20)

    @staticmethod
    def expirado(causa):
        return NotAuthenticatedException(u"La sesión del usuario ha expirado", 21, causa)

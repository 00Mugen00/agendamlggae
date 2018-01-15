# -*- coding: utf-8 -*-

from facades import AgendamlgNotFoundException
from models import Comentario, Usuario, Evento
from google.appengine.ext import ndb
from util import parse_date, to_utc
from excepcion import NotAuthenticatedException


def crear_comentario(usuario, evento, comentario):
    # type: (Usuario, Evento, {unicode|str:object}) -> Comentario
    """
    :param usuario: Usuario que crea o edita el comentario
    :param evento: Evento al que pertenece el comentario
    :param comentario: comentario que se está creando o comentario que se está modificando
    :return: el Comentario nuevo
    """
    comentario = Comentario(
        parent=evento,
        creador=usuario.key,
        texto=comentario[u'texto'],
        fecha=parse_date(comentario[u'fecha']).replace(tzinfo=None) if u'fecha' in comentario else to_utc()
    )
    if 0 < usuario.tipo < 4:
        comentario.put()
        return comentario
    else:
        raise NotAuthenticatedException.no_autenticado()


def eliminar_comentario(usuario, comentario):
    # type: (Usuario, ndb.Key) -> None
    """
    :param usuario: usuario que elimina el comentario
    :param comentario: comentario que se quiere eliminar
    :return:
    """
    if usuario.tipo == 3 or usuario.key == comentario.get().creador:
        comentario.delete()
    else:
        raise AgendamlgNotFoundException.comentario_no_existe(comentario.urlsafe())


def buscar_comentarios_evento(usuario, evento):
    # type: (Usuario|None, ndb.Key) -> [Comentario]
    """
    :param usuario: usuario de la sesión, o 'None'
    :param evento: buscamos los comentarios de este evento
    :return:
    """
    evento = evento.get()
    tipo = usuario.tipo if usuario else 1
    if (tipo == 3 or evento.validado) or usuario.key == evento.key.parent():
        q = Comentario.query(ancestor=evento.key)
        return q.fetch()
    else:
        raise AgendamlgNotFoundException.evento_no_existe(evento.urlsafe())

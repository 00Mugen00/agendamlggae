# -*- coding: utf-8 -*-

from facades import AgendamlgNotFoundException, AgendamlgException
from models import Comentario, Usuario, Evento
from google.appengine.ext import ndb
from util import to_utc
from excepcion import NotAuthenticatedException


def crear_editar_megusta(usuario, evento, comentario):
    # type: (Usuario, Evento, {unicode|str:object}) -> Comentario
    """
    :param usuario: Usuario que crea o edita el comentario
    :param evento: Evento al que pertenece el comentario
    :param comentario: comentario que se está creando o comentario que se está modificando
    :return: el Comentario nuevo
    """
    if u'texto' not in comentario:
        raise AgendamlgException.comentario_campos_invalidos()

    otro_comentario = Comentario.query(Comentario.creador == usuario.key, ancestor=evento).fetch()
    if otro_comentario:
        raise AgendamlgException.usuario_ya_ha_comentado(usuario.idGoogle)

    comentario = Comentario(
        parent=evento,
        creador=usuario.key,
        texto=comentario[u'texto'],
        fecha=to_utc()
    )
    if 0 < usuario.tipo < 4:
        comentario.put()
        return comentario
    else:
        raise NotAuthenticatedException.no_autenticado()


def eliminar_comentario(usuario, evento):
    # type: (Usuario, ndb.Key) -> None
    """
    :param usuario: usuario que elimina el comentario
    :param evento: evento al que eliminar el comentario del usuario
    :return:
    """
    comentario = Comentario.query(Comentario.creador == usuario.key, ancestor=evento).fetch()
    if not comentario:
        AgendamlgNotFoundException.comentario_no_existe(evento.urlsafe())
    comentario = comentario[0]
    if usuario.tipo == 3 or usuario.key == comentario.get().creador:
        comentario.delete()
    else:
        raise AgendamlgException.sin_permisos(usuario.idGoogle)


def buscar_comentarios_evento(usuario, evento):
    # type: (Usuario|None, ndb.Key) -> [Comentario]
    """
    :param usuario: usuario de la sesión, o 'None'
    :param evento: buscamos los comentarios de este evento
    :return:
    """
    evento = evento.get()
    tipo = usuario.tipo if usuario else 1
    if evento is not None and (tipo == 3 or evento.validado or usuario.key == evento.key.parent()):
        q = Comentario.query(ancestor=evento.key)
        return q.fetch()
    else:
        raise AgendamlgNotFoundException.evento_no_existe(evento.urlsafe())

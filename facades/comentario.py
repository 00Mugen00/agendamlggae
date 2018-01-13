# -*- coding: utf-8 -*-

from models import Comentario
from excepcion import NotAuthenticatedException

def crear_editar_megusta(usuario,comentario):
    """
    :param usuario: usuario que crea o edita el comentario
    :param comentario: comentario que se está creando o comentario que se está modificando
    :return:
    """
    if usuario.tipo > 0 and usuario.tipo <4:
        comentario.put()
    else:
        raise NotAuthenticatedException.no_autenticado()


def eliminar_comentario(usuario,comentario):
    """
    :param usuario: usuario que elimina el comentario
    :param comentario: comentario que se quiere eliminar
    :return:
    """
    if usuario.tipo > 0 and usuario.tipo <4:
        comentario.key.delete()
    else:
        raise NotAuthenticatedException.no_autenticado()


def buscar_comentarios_evento(evento):
    """
    :param evento: buscamos los comentarios de este evento
    :return:
    """
    q = Comentario.query(ancestor=evento.key)
    return q.filter()
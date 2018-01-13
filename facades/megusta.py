# -*- coding: utf-8 -*-

from models import MeGusta
from excepcion import NotAuthenticatedException

def crear_me_gusta(usuario,me_gusta):
    """
    :param usuario: usuario que crea o edita el comentario
    :param me_gusta: megusta que queremos insertar en la base de datos
    :return:
    """
    if usuario.tipo > 0 and usuario.tipo <4:
        me_gusta.put()
    else:
        raise NotAuthenticatedException.no_autenticado()


def eliminar_me_gusta(usuario,me_gusta):
    """
    :param usuario: usuario que elimina el comentario
    :param me_gusta: megusta que queremos eliminar en la base de datos
    :return:
    """
    if usuario.tipo > 0 and usuario.tipo <4:
        me_gusta.key.delete()
    else:
        raise NotAuthenticatedException.no_autenticado()


def buscar_numero_me_gusta_evento(evento):
    """
    :param evento: buscamos el número de me_gusta de este evento
    :return:
    """
    q = MeGusta.query(ancestor=evento.key)
    return len(q.fetch())
# -*- coding: utf-8 -*-

from models import MeGusta
from excepcion import AgendamlgException

def crear_me_gusta(usuario, evento):
    """
    :param usuario: usuario que crea o edita el comentario
    :param evento: evento que me gusta
    :return:
    """
    me_gusta = MeGusta(
        parent=evento,
        creador=usuario.key
    )
    if 0 < usuario.tipo < 4 and evento.get().validado:
        me_gusta.put()
    else:
        raise AgendamlgException.sin_permisos(usuario.idGoogle)


def eliminar_me_gusta(usuario, evento):
    """
    :param usuario: usuario que elimina el comentario
    :param evento: evento que no me gusta
    :return:
    """
    me_gusta = MeGusta.query(MeGusta.creador == usuario.key, ancestor=evento).fetch()
    if 0 < usuario.tipo < 4 and evento.get().validado:
        me_gusta[0].key.delete() if me_gusta else None
    else:
        raise AgendamlgException.sin_permisos(usuario.idGoogle)


def buscar_numero_me_gusta_evento(evento):
    """
    :param evento: buscamos el número de me_gusta de este evento
    :return:
    """
    q = MeGusta.query(ancestor=evento.key)
    return q.count()


def usuario_ha_dado_me_gusta(usuario, evento):
    """
    Indica si un usuario le ha dado a me gusta al evento proporcionado

    :param usuario: Usuario
    :param evento: Evento
    :return: bool
    """
    # Obtener los me gusta para el evento proporcionado
    me_gusta = MeGusta.query(ancestor=evento.key).fetch()

    # Filtrar me gusta proporcionados por el usuario (comprobar creador)
    return len(filter(lambda x: x.creador == usuario.key, me_gusta)) > 0
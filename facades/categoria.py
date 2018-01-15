from models import Evento, Categoria, Usuario
from excepcion import AgendamlgException, AgendamlgNotFoundException

def buscar_preferencias_usuario(usuario):
    """
    :param usuario: Usuario el cual se presupone existe
    :return: list Categorias
    """

    if usuario:
        return [ c.get() for c in usuario.preferencias ]
    else:
        raise AgendamlgNotFoundException.usuario_no_existe()


def buscar_categorias_evento(evento):
    """
    :param evento: Evento
    :return: list Categorias
    """
    if evento:
        return [ c.get() for c in evento.categorias ]
    else:
        raise AgendamlgNotFoundException.evento_no_existe()


def eliminar_preferencia_usuario(usuario, preferencia):
    """
    :param usuario: Usuario
    :param preferencia: Categoria
    :return: boolean
    """
    if usuario:
        usuario.preferencias.remove(preferencia)
        usuario.put()


def agregar_preferencia_usuario(usuario, preferencia_key):
    """
    :param usuario: Usuario
    :param prefe: Categoria
    :return:
    """
    if usuario:
        usuario.preferencias.append(preferencia_key)
        usuario.put()


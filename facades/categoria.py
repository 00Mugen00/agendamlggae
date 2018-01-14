from models import Evento, Categoria, Usuario
from excepcion import AgendamlgException, AgendamlgNotFoundException

def buscar_preferencias_usuario(usuario):
    """
    :param usuario: Usuario
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

    q = Categoria.query(ancestor=usuario)
    q.filter(Categoria.key == preferencia.key)
    categories = q.fetch()
    if not categories:
        usuario.preferencias.remove(categories[0])
        return False
    else:
        return True


def agregar_preferencia_usuario(usuario, prefe):
    """
            :param usuario: Usuario
            :param prefe: Categoria
            :return:
            """
    if usuario:
        q = Categoria.query(Categoria.key == prefe.key)
        category = q.fetch()
        if category:
            usuario.preferencias.insert(category)
        else:
            AgendamlgNotFoundException.categoria_no_existe()


from models import Evento, Categoria, Usuario
from excepcion import AgendamlgException, AgendamlgNotFoundException

def buscar_preferencias_usuario(usuario):
    """
    :param usuario: Usuario el cual se presupone existe
    :return: list Categorias
    """
    claves_categorias_usuario = Usuario.query(Usuario.key == usuario.key).fetch()[0].preferencias

    return [Categoria.query(Categoria.key == categoria_clave).fetch()[0] for categoria_clave in claves_categorias_usuario]


def buscar_categorias_evento(evento):
    """
        :param evento: Evento
        :return: list Categorias
        """
    if evento:
        q = Categoria.query(ancestor=evento)
        return q.fetch()
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


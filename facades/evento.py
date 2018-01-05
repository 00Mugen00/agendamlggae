# -*- coding: utf-8 -*-

from models import Evento,Categoria
from agendamlgexception import AgendamlgException
from agendamlgnotfoundexception import AgendamlgNotFoundException
import datetime

def crear_evento_tipo_usuario(usuario,evento,categoriasEvento):
    """
    :param usuario: Usuario
    :param evento: Evento
    :param categoriasEvento: list str
    :return:
    """
    if evento.tipo<1 or evento.tipo>3:
        raise  AgendamlgException.tipo_invalido(evento.tipo)
    categorias = Categoria.query(Categoria.nombre.IN(categoriasEvento)).fetch()
    if usuario.tipo==1:
        evento.validado = False
    elif usuario.tipo>1:
        evento.validado = True
    evento.put()
    evento.categorias = [categoria.key() for categoria in categorias]
    #enviarCorreoInteresados(evento) -> PUEDE QUE NO LO NECESITEMOS


def buscar_eventos_usuario(usuario,todos):
    """
    :param usuario: Usuario
    :param todos: boolean
    :return: list Evento
    """
    if usuario:
        q = Evento.query(ancestor=usuario.key())
        if todos:
            q.filter(Evento.validado==True)
        q.order(Evento.fecha)
        return q.fetch()
    else:
        raise AgendamlgNotFoundException.usuario_no_existe()


def buscar_eventos_tipo_usuario(usuario):
    """
    :param usuario:
    :return: list Evento
    """
    current_datetime = datetime.datetime.today()
    q = Evento.query(Evento.fecha>current_datetime)
    q.order(Evento.fecha)
    if usuario and usuario.tipo!=3:
        q.filter(Evento.validado==True)
    return q.fetch()
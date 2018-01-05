# -*- coding: utf-8 -*-

from models import Evento,Categoria
from agendamlgexception import AgendamlgException

def crearEventoTipoUsuario(usuario,evento,categoriasEvento):
    if evento.tipo<1 or evento.tipo>3:
        raise  AgendamlgException.tipo_invalido(evento.tipo)
    categorias = Categoria.query('nombre IN', categoriasEvento)
    if usuario.tipo==1:
        evento.validado = False
        evento.categorias = [categoria.key() for categoria in categorias]
        evento.put()
    elif usuario.tipo>1:
        evento.validado = True
        evento.categorias = [categoria.key() for categoria in categorias]
        #enviarCorreoInteresados(evento) -> PUEDE QUE NO LO NECESITEMOS


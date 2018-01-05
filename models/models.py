# -*- coding: utf-8 -*-
from google.appengine.ext import ndb

# Nombre de la agenda, se trata del id para la clave raiz de tipo "Agenda"

AGENDA_NOMBRE = 'AGENDAMLG'


def agenda_key():
    """Construye una clave de DataStore de tipo Agenda, y con id
    AGENDA_NOMBRE. Funcion que crea una clave raiz para las entidades,
    de esta forma nos aseguramos que todas las entidades de la
    agenda estan en el mismo "entity group" haciendo las consultas
    en esta consistentes"""
    return ndb.Key('Agenda', AGENDA_NOMBRE)


# Modelo categoria
class Categoria(ndb.Model):
    """
    La clave tiene el siguiente aspecto:
    ('Agenda', AGENDA_NOMBRE, 'Categoria', XXX)

    La categoria se crea:
    categoria = Categoria(propiedades...,parent=agenda_key())
    categoria.put()
    """

    nombre = ndb.StringProperty(required=True)


# Modelo de usuario
class Usuario(ndb.Model):
    """
    La clave tiene el siguiente aspecto:
    ('Agenda', AGENDA_NOMBRE, 'Usuario', XXX)

    El usuario se crea:
    usuario = Usuario(propiedades....,parent=agenda_key())
    usuario.put()

    Representacion de las preferencias
    [('Agenda', AGENDA_NOMBRE, 'Categoria', 347298),('Agenda', AGENDA_NOMBRE, 'Categoria', 347298)]
    """

    idGoogle = ndb.StringProperty(required=True)
    tipo = ndb.IntegerProperty(required=True)
    preferencias = ndb.KeyProperty(kind='Categoria', repeated=True)


# Modelo de evento
class Evento(ndb.Model):
    """
    La clave tiene el siguiente aspecto:
    ('Agenda', AGENDA_NOMBRE, 'Usuario', XXX, 'Evento', XXX)

    Dado un usuario, un evento se crea:
    evento = Evento(propiedades..., parent=usuario.key)
    evento.put()
    """

    tipo = ndb.IntegerProperty(required=True)
    nombre = ndb.StringProperty(required=True)
    descripcion = ndb.StringProperty(required=True, indexed=False)
    fecha = ndb.DateTimeProperty(auto_now_add=True, required=True)
    precio = ndb.FloatProperty()
    direccion = ndb.StringProperty(required=True)
    validado = ndb.BooleanProperty(default=False, required=True)
    coordenadas = ndb.GeoPtProperty()
    flickrUserId = ndb.StringProperty()
    flickrAlbumId = ndb.StringProperty()
    categorias = ndb.KeyProperty(kind='Categoria', repeated=True)

# Modelo de meGusta
class MeGusta(ndb.Model):
    """
    La clave tiene el siguiente aspecto:
    ('Agenda', AGENDA_NOMBRE, 'Usuario', XXX, 'Evento', XXX, 'MeGusta', XXX)

    MeGusta se crea, dado un evento, ademas fijar la propiedad creador, teniendo usuaro la sesion iniciada:
    meGusta = MeGusta(creador=usuario.key(),parent=evento.key())
    """
    creador = ndb.KeyProperty(kind='Usuario', required=True)


# Modelo comentario
class Comentario(ndb.Model):
    """
    La clave tiene el siguiente aspecto:
    ('Agenda', AGENDA_NOMBRE, 'Usuario', XXX, 'Evento', XXX, 'Comentario', XXX)

    El comentario se crea, dado un evento, ademas fijar la propiedad creador, teniendo usuario la sesion inciada:
    comentario = Comentario(propiedades..., creador=usuario.key(),parent=evento.key())
    comentario.put()
    """

    texto = ndb.StringProperty(indexed=False)
    fecha = ndb.DateTimeProperty(auto_now_add=True)
    creador = ndb.KeyProperty(kind='Usuario', required=True)


class FlickrCache(ndb.Model):
    url = ndb.StringProperty(required=True)
    value = ndb.StringProperty(required=True, indexed=False)
    created = ndb.DateTimeProperty(required=True, auto_now_add=True)

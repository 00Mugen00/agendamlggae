#!/usr/bin/env python
# -*- coding: utf-8 -*-

from base import BaseHandler
from models import Evento
from tokens import get_user_from_token
from util import parse_date
from google.appengine.ext import ndb
from facades.evento import crear_evento_tipo_usuario, evento_largo_clave, buscar_evento_categorias, obtener_foto_url, \
    clave_evento_o_fallo
# Expresiones regulares
import re
import flickr
from facades.excepcion import AgendamlgException
import util.json
from salida_eventos_json import eventos_json
from geocode import encontrar_coordenadas


class EventoHandler(BaseHandler):

    # Creacion de un evento, es una ruta que necesita autenticacion
    # Se recibe una lista de categorias, que son sus claves en version urlsafe
    def post(self):
        # Si el usuario no est autenticado se lanza excepcion
        _, usuario = get_user_from_token(self.request.headers.get('bearer'), raise_for_unauthenticated=True)

        evento_from_json = self.json_body()

        # Construir un clave parent adecuada para el evento, la cual es la id del usuario
        evento = Evento(parent=usuario.key)

        # Rellenar el evento

        evento.tipo = int(evento_from_json.get('tipo'))
        evento.nombre = evento_from_json.get('nombre', None)
        evento.descripcion = evento_from_json.get('descripcion', None)
        evento.fecha = parse_date(evento_from_json.get('fecha', None)).replace(tzinfo=None)
        evento.precio = evento_from_json.get('precio', None)
        evento.direccion = evento_from_json.get('direccion', None)
        # Si esta validado o no se gestiona en el el metodo de la fachada

        evento.coordenadas = None

        # Rellenar las categorias del evento (lista de claves de categorias)
        # Ojo! las categorias tienen la siguiente forma
        # [{"id": X},{"id": X}....]
        evento.categorias = [ndb.Key(urlsafe=claveURLSafe['id']) for claveURLSafe in
                             evento_from_json.get('categoriaList', [])]
        # Gestionar datos de flickr
        modificar_datos_flickr(evento, evento_from_json.get('flickrUserID', None),
                               evento_from_json.get('flickrAlbumID', None))

        # Fijar las coordenadas del evento
        coordenadas_evento = encontrar_coordenadas(evento.direccion)

        if coordenadas_evento is not None:
            evento.coordenadas = coordenadas_evento

        # Persistir el evento
        crear_evento_tipo_usuario(usuario, evento)

        evento_dic = evento_largo_clave(evento.key, usuario)

        # Ponerle su fotoUrl!
        foto_url = obtener_foto_url(evento_dic)

        if foto_url is not None:
            evento_dic['fotoUrl'] = foto_url

        # Devolver evento recien creado completo
        self.response.write(util.json.to_json(evento_dic))

    # Obtener todos los eventos existentes en el sistema, es el equivalente a filtrar
    # con un filtro vacio, sirve estando logueado o no
    def get(self):
        _, usuario = get_user_from_token(self.request.headers.get('bearer'), raise_for_unauthenticated=False)

        eventos = buscar_evento_categorias(usuario)

        # Devolver respuesta
        self.response.write(eventos_json(eventos, True))

    def put(self):
        """
        Dado un evento como json, procede a actualizarlo

        :return: Evento modificado como json
        """

        # Esta ruta requiere de autenticacion
        _, usuario = get_user_from_token(self.request.headers.get('bearer'), raise_for_unauthenticated=True)

        # Evento recibido por json:
        evento_from_json = self.json_body()

        # Se obtiene el evento
        evento = clave_evento_o_fallo(evento_from_json.get('id', '')).get()

        # En este punto se ha obtenido con exito el evento, comprobar si pertenece al usuario o este es
        # periodista

        if usuario.tipo != 3 and usuario.key != evento.key.parent():
            raise AgendamlgException.sin_permisos(usuario)

        # Proceder a la edicion del evento

        # Actualizar categorias (el evento guarda una lista de claves de categoria
        evento.categorias = [ndb.Key(urlsafe=jsoncat['id']) for jsoncat in evento_from_json.get('categoriaList', [])]

        # Rellenar el evento

        evento.tipo = int(evento_from_json.get('tipo'))
        evento.nombre = evento_from_json.get('nombre', None)
        evento.descripcion = evento_from_json.get('descripcion', None)
        evento.fecha = parse_date(evento_from_json.get('fecha', None)).replace(tzinfo=None)
        evento.precio = evento_from_json.get('precio', None)
        evento.direccion = evento_from_json.get('direccion', None)
        # Si esta validado o no se gestiona en el el metodo de la fachada

        evento.coordenadas = None

        # Gestionar datos de flickr
        modificar_datos_flickr(evento, evento_from_json.get('flickrUserID', None),
                               evento_from_json.get('flickrAlbumID', None))

        # Fijar las coordenadas del evento
        coordenadas_evento = encontrar_coordenadas(evento.direccion)

        if coordenadas_evento is not None:
            evento.coordenadas = coordenadas_evento

        # Se procede a actualizar el evento
        evento.put()

        # Se devuelve la version larga del evento
        evento_dict = evento_largo_clave(evento.key, usuario)

        # Ponerle su fotoUrl!
        foto_url = obtener_foto_url(evento_dict)

        if foto_url is not None:
            evento_dict['fotoUrl'] = foto_url

        # Devolver evento recien creado completo
        self.response.write(util.json.to_json(evento_dict))


def modificar_datos_flickr(evento, user_id=None, album_id=None):
    """
    :param evento: ndb.Evento El evento que se va a almacenar en la base de datos
    :param user_id: string id de usuario como cadena que manda el cliente
    :param album_id: string id de album como cadena proporcionada por el cliente
    :return: void
    """
    if (user_id is not None) and (album_id is not None):
        if not album_id or album_id != evento.flickrAlbumId:
            evento.flickrAlbumId = album_id

        if not user_id or user_id != evento.flickrUserId:
            evento.flickrUserId = user_id

            expresion = re.compile('\d+@N\d{2}')

            if user_id and not (expresion.match(user_id)):
                # Se obtiene empleando la API de flickr el user ID
                url_peticion = "http://www.flickr.com/photos/{}/".format(user_id)
                # ID usuario
                id_usuario = flickr.urls.lookup_user(url_peticion)

                evento.flickrUserId = id_usuario

            if not evento.flickrUserId:
                # Lanzar excepcion de incidencia con flickr
                raise AgendamlgException.flickr_username_invalido(user_id)


class CoordenadasLatLong(BaseHandler):
    def get(self, direccion):

        _, usuario = get_user_from_token(self.request.headers.get('bearer'))
        coordenadas = encontrar_coordenadas(direccion)
        encontrado = True

        if coordenadas is None:
            encontrado = False

        self.response.write(util.json.to_json({
            'encontrado': encontrado,
            'latitud': coordenadas.lat if coordenadas else None,
            'longitud': coordenadas.lon if coordenadas else None
        }))

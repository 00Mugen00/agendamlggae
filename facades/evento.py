#!/usr/bin/env python
# -*- coding: utf-8 -*-

from models import Evento, Categoria, Usuario
from excepcion import AgendamlgException, AgendamlgNotFoundException, NotAuthenticatedException
import datetime
from datetime import datetime as dt
import math
from google.appengine.ext import ndb
from operator import itemgetter
from mail import send_mail
from facades import usuario


def enviar_correo_interesados(evento):
    categorias = Categoria.query(Categoria.nombre.IN(evento.categorias)).fetch()
    send_mail(usuario.buscar_usuarios_preferencias(categorias),u'Hay un evento que te puede gustar',evento.nombre+u' es un evento de tu preferencia')


def enviar_correo_creador(evento,creador):
    usuarios = [creador]
    send_mail(usuarios,u'Tu evento ha sido publicado',u'El evento '+evento.nombre+' ha sido publicado')


def crear_evento_tipo_usuario(usuario, evento, categorias_evento):
    """
    :param usuario: Usuario
    :param evento: Evento
    :param categorias_evento: list str
    :return:
    """
    if evento.tipo < 1 or evento.tipo > 3:
        raise AgendamlgException.tipo_invalido(evento.tipo)
    categorias = Categoria.query(Categoria.nombre.IN(categorias_evento)).fetch()
    if usuario.tipo == 1:
        evento.validado = False
    elif usuario.tipo > 1 and usuario.tipo <4:
        evento.validado = True
    else:
        raise NotAuthenticatedException.no_autenticado()
    evento.put()
    evento.categorias = [categoria.key for categoria in categorias]
    #enviar_correo_interesados(evento)


def buscar_eventos_usuario(usuario, todos):
    """
    :param usuario: Usuario
    :param todos: boolean
    :return: list Evento
    """
    if usuario:
        q = Evento.query(ancestor=usuario.key)
        if todos:
            q.filter(Evento.validado == True)
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
    q = Evento.query(Evento.fecha > current_datetime)
    q.order(Evento.fecha)
    if usuario and usuario.tipo != 3:
        q.filter(Evento.validado == True)
    return q.fetch()


def buscar_evento_categorias(usuario, **filtrado):
    """
    Dados unos criterios de filtrados proporcionados en filtrado, se devuelve
    una lista de Eventos que satisfagan esos criterios. El filtrado se pasa como
    un diccionario expandido: buscar_evento_categorias(**filtrado), filtrado tiene el siguiente
    aspecto:

    {
    categorias: list Categoria, # Lista de categorias para filtrado, objetos Categoria!
    filtroCercania: Boolean     # Indicar si se esta filtrando (ordenando) por cercania respecto a una posicion y radio dados
    coordenadas: ndb.GeoPt      # Objeto GeoPt de ndb que almacena las coordenadas, posicion dada por el usuario (procedente GeoLocalizacion normalmente)
    radio: float                # Radio alrededor del cual filtrar los eventos
    textoTitulo: string         # Filtrar eventos ademas en base al titulo
    }

    :param usuario: Usuario     # Usuario que hace la consulta (qué eventos mostrar)
    :param filtrado: Descrito anteriormente
    :return: list Evento
    """

    fecha_actual = dt.now()

    # Se construye una primera consulta, la cual irá refinándose
    # conforme los requisitos de filtrado

    # Ojo! Los objetos de consulta son inmutables, tener esto en cuenta
    consulta = Evento.query()

    # Filtrar por aquellos cuya fecha sea posterior a la actual o bien sean persistentes o frecuentes (tipo 2 y 3)
    consulta = consulta.filter(ndb.OR(Evento.fecha > fecha_actual, Evento.tipo == 2, Evento.tipo == 3))

    # Si no se pide filtrado por distancia, se hace ordenacion por fecha descendente
    if not filtrado['filtroCercania']:
        consulta = consulta.order(-Evento.fecha)

    else:
        # De lo contrario no se traen de la base de datos eventos que no tengan coordenadas
        consulta = consulta.filter(Evento.coordenadas != None)

    # Si el usuario no es periodista o no ha iniciado sesion se obtienen solo los eventos validados
    if not usuario or usuario.tipo != 3:
        consulta = consulta.filter(Evento.validado == True)

    # Si se da una lista de categorias y esta no es vacia considera tambien en la consulta
    if 'categorias' in filtrado and len(filtrado['categorias']) > 0:
        # Lista de claves de categorias
        consulta = consulta.filter(Evento.categorias.IN([cat.key for cat in filtrado['categorias']]))

    # El orden por distancia o el filtrado por titulo debe hacerse fuera de DataStore por la forma en que este funciona
    # https://stackoverflow.com/questions/23317280/appengine-search-api-vs-datastore
    # Las coordenadas del evento no pueden usarse para hacer una query por cercania a otra coordenada, es decir
    # datastore no las trata de forma especial, de ahi que sea necesaria la formula del Haversine:
    # https://stackoverflow.com/questions/1033240/how-do-i-query-for-entities-that-are-nearby-with-the-geopt-property-in-google
    # Es por esto que ahora se esta en condicion de obtener la lista de resultados para trabajar con ella

    resultados = consulta.fetch()

    # Se dispone de filtro de cercania, en consecuencia los eventos se ordenan por distancia a la proporcionada
    if filtrado['filtroCercania']:
        # Preparar un iterador con pares (distancia, evento). Donde distancia es la distancia del evento a
        # la posición proporcionada
        distancias = ((distancia((ev.coordenadas.lat, ev.coordenadas.lon),
                                 (filtrado['coordenadas'].lat, filtrado['coordenadas'].lon)), ev) for ev in resultados)

        # El siguiente iterador elimina los eventos que esten a una distancia mayor de la proporcionada
        # La distancia se pone negativa para que funcione la ordenacion descendente (a igual distancia,
        # se escoger la fecha mas reciente (mayor)
        lejanos_eliminados = ((-dist, ev) for (dist, ev) in distancias if dist <= filtrado['radio'])

        # Se ordenan los pares de esa lista de acuerdo a una funcion de ordenacion
        ordenacion = sorted(lejanos_eliminados, key=itemgetter(1, 2), reverse=True)

        # Se obtiene una lista de eventos
        resultados = [ev for (dist, ev) in ordenacion]

    # Fitrar resultados de nuevo, esta vez por el texto del titulo que se ofrezca (si se ofrece)

    if 'textoTitulo' in filtrado and len(filtrado['textoTitulo'].strip()) > 0:

        resultados = [evento_filtro for evento_filtro in resultados if filtrado['textoTitulo'].lower() in evento_filtro.nombre.lower()]

    return resultados


def distancia(origin, destination):
    # type: (object, object) -> object
    """

    :param origin: GeoPt
    :param destination:
    :return:
    """
    # Esto se conoce como tuple unpacking
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371  # km

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon / 2) * math.sin(dlon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = radius * c

    return d

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from models import Evento, Categoria
from excepcion import AgendamlgException, AgendamlgNotFoundException, NotAuthenticatedException
import datetime
from datetime import datetime as dt
import math
from google.appengine.ext import ndb
from operator import itemgetter
from mail import send_mail
from facades import usuario
from flickr import photosets
import truncar
import util
from megusta import buscar_numero_me_gusta_evento, usuario_ha_dado_me_gusta

# Maximo numero de caracteres que pueden aparecer en descripcion del evento
MAX_CARACTERES_DESCRIPCION = 150


def enviar_correo_interesados(evento):
    categorias = Categoria.query(Categoria.key.IN(evento.categorias)).fetch()
    usuarios = usuario.buscar_usuarios_preferencias(categorias)
    send_mail([ util.from_json(_usuario.extra)[u'emails'][0][u'value'] for _usuario in usuarios ],
              u'Hay un evento que te puede gustar - Agendamlggae',
              u'''{} es un evento de tu preferencias. Es nuevo y puede que te interese.
              https://agendamlggae-amjm.appspot.com/verEvento/{}
              '''.format(evento.nombre, evento.key.urlsafe()))


def enviar_correo_creador(evento, creador):
    usuarios = [ util.from_json(creador.extra)[u'emails'][0][u'value'] ]
    send_mail(usuarios,
              u'Tu evento {} ha sido publicado'.format(evento.nombre),
              u'''El evento {} ha sido publicado. Puedes verlo aqui:
              https://agendamlggae-amjm.appspot.com/verEvento/{}'''
              .format(evento.nombre, evento.key.urlsafe()))


def crear_evento_tipo_usuario(usuario, evento):
    """
    :param usuario: Usuario
    :param evento: Evento
    :return:
    """
    if evento.tipo < 1 or evento.tipo > 3:
        raise AgendamlgException.tipo_invalido(evento.tipo)

    if usuario.tipo == 1:
        evento.validado = False
    elif usuario.tipo > 1 and usuario.tipo < 4:
        evento.validado = True
    else:
        raise NotAuthenticatedException.no_autenticado()

    evento.put()

    if usuario.tipo > 1 and usuario.tipo < 4:
        # Mandar el correo a los usuarios interesados en ese evento
        enviar_correo_interesados(evento)


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
    categorias: list Categoria, # Lista de claves de Categoria para el filtrado, claves de Categoria!
    ordenarPorDistancia: Boolean     # Indicar si se esta filtrando (ordenando) por cercania respecto a una posicion y radio dados
    coordenadas: ndb.GeoPt      # Objeto GeoPt de ndb que almacena las coordenadas, posicion dada por el usuario (procedente GeoLocalizacion normalmente)
    radio: float                # Radio alrededor del cual filtrar los eventos
    textoTitulo: string         # Filtrar eventos ademas en base al titulo
    }

    :param usuario: Usuario     # Usuario que hace la consulta (qué eventos mostrar)
    :param filtrado: Descrito anteriormente
    :return: list Evento
    """

    fecha_actual = dt.utcnow()

    # Se construye una primera consulta, la cual irá refinándose
    # conforme los requisitos de filtrado

    # Ojo! Los objetos de consulta son inmutables, tener esto en cuenta
    consulta = Evento.query()

    # Filtrar por aquellos cuya fecha sea posterior a la actual o bien sean persistentes o frecuentes (tipo 2 y 3)
    consulta = consulta.filter(ndb.OR(Evento.fecha > fecha_actual, Evento.tipo == 2, Evento.tipo == 3))

    # Si no se pide filtrado por distancia, se hace ordenacion por fecha descendente
    if not filtrado.get('ordenarPorDistancia', '') == 'true':
        consulta = consulta.order(Evento.fecha)

    else:
        # De lo contrario no se traen de la base de datos eventos que no tengan coordenadas
        # consulta = consulta.filter(Evento.coordenadas != None)
        # Esto no se puede hacer, porque en una query solo se permite un unico filter de no
        # gualdad, que no sea ==
        # Ademas en el objeto filtrado hay que establecer la clave "coordenadas" que es un GeoPt
        # a partir de la latitud y longitud proporcionadas
        filtrado['coordenadas'] = ndb.GeoPt(filtrado['latitud']+', '+filtrado['longitud'])
        # Por otro lado se convierte el radio a float
        filtrado['radio'] = float(filtrado['radio'])

    # Si el usuario no es periodista o no ha iniciado sesion se obtienen solo los eventos validados
    if not usuario or usuario.tipo != 3:
        consulta = consulta.filter(Evento.validado == True)

    # Si se da una lista de categorias y esta no es vacia considera tambien en la consulta
    if len(filtrado.get('categorias', [])) > 0:
        consulta = consulta.filter(Evento.categorias.IN(filtrado['categorias']))

    # El orden por distancia o el filtrado por titulo debe hacerse fuera de DataStore por la forma en que este funciona
    # https://stackoverflow.com/questions/23317280/appengine-search-api-vs-datastore
    # Las coordenadas del evento no pueden usarse para hacer una query por cercania a otra coordenada, es decir
    # datastore no las trata de forma especial, de ahi que sea necesaria la formula del Haversine:
    # https://stackoverflow.com/questions/1033240/how-do-i-query-for-entities-that-are-nearby-with-the-geopt-property-in-google
    # Es por esto que ahora se esta en condicion de obtener la lista de resultados para trabajar con ella

    resultados = consulta.fetch()

    # Se dispone de filtro de cercania, en consecuencia los eventos se ordenan por distancia a la proporcionada
    if filtrado.get('ordenarPorDistancia', '') == 'true':

        # Dado que anteriormente el query de no igualdad no se ha podido hacer porque solo se puede
        # tener uno en una query, se eliminan a mano los eventos que no tienen coordenadas, es decir GeoPt
        resultados = [resultadogeo for resultadogeo in resultados if resultadogeo.coordenadas is not None]

        # Preparar un iterador con pares (distancia, evento). Donde distancia es la distancia del evento a
        # la posición proporcionada
        distancias = ((distancia((ev.coordenadas.lat, ev.coordenadas.lon),
                                 (filtrado['coordenadas'].lat, filtrado['coordenadas'].lon)), ev) for ev in resultados)

        # El siguiente iterador elimina los eventos que esten a una distancia mayor de la proporcionada
        # La distancia se pone negativa para que funcione la ordenacion descendente (a igual distancia,
        # se escoger la fecha mas reciente (mayor)
        lejanos_eliminados = ((-dist, ev) for (dist, ev) in distancias if dist <= filtrado['radio'])

        # Se ordenan los pares de esa lista de acuerdo a una funcion de ordenacion
        ordenacion = sorted(lejanos_eliminados, key=itemgetter(0, 1), reverse=True)

        # Se obtiene una lista de eventos
        resultados = [ev for (dist, ev) in ordenacion]

    # Fitrar resultados de nuevo, esta vez por el texto del titulo que se ofrezca (si se ofrece)

    if len(filtrado.get('textoTitulo', '').strip()) > 0:
        palabra_clave = filtrado.get('textoTitulo', '').strip().lower()
        resultados = [evento_filtro for evento_filtro in resultados if palabra_clave in evento_filtro.nombre.lower()]

    return resultados


def validar_evento(clave_evento):
    """
    Dada una clave de evento como urlsafe, se procede a la validacion de este
    :param clave_evento: Instancia de Key para un evento
    :return:
    """
    try:
        evento = ndb.Key(urlsafe=clave_evento).get()
        evento.validado = True
        evento.put()
        # Mandar correo de validacion y de informacion a usuarios
        enviar_correo_interesados(evento)
        enviar_correo_creador(evento, evento.key.get())

    except:
        # Si hay una excepcion, se lanza que el evento no se ha encontrado en la agenda o similar
        raise AgendamlgNotFoundException.evento_no_existe(clave_evento)


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


# Esta funcion permite asignar correctamente el atributo fotoUrl de un evento, en su version de diccionario
def obtener_foto_url(evento):
    """
    Diccionario
    :param evento: dic
    :return:
    """
    retorno = None

    if (evento.get('flickrUserID') is not None) and (evento.get('flickrAlbumID') is not None):
        try:

            info = photosets.get_info(evento['flickrUserID'], evento['flickrAlbumID'])

            if info is not None and info.primary:
                retorno = info.primary.medium_size_url

        except:
            pass

    return retorno


# Dado un texto devuelve la version corta de este


# Dada una clave de evento devuelve un diccionario con una version resumida del evento
def evento_corto_clave(clave):
    return evento_corto(clave.get())


# Dada una clave de evento devuelve un diccionario con una version extendida del evento
def evento_largo_clave(clave, usuario_sesion=None):
    return evento_largo(clave.get(), usuario_sesion)


# Dada un evento devuelve un diccionario con una version resumida del evento
def evento_corto(evento, adjuntar_datos_flickr=False):
    # Lanzar excepcion si no existe el evento
    if evento is None:
        raise AgendamlgNotFoundException.evento_no_existe(evento)

    retorno = {'descripcion': truncar.trunc(evento.descripcion, max_pos=MAX_CARACTERES_DESCRIPCION),
               'direccion': evento.direccion,
               'fecha': evento.fecha.isoformat(),
               'nombre': evento.nombre,
               'precio': evento.precio,
               'id': evento.key.urlsafe()}

    if evento.coordenadas:
        retorno['latitud'] = evento.coordenadas.lat
        retorno['longitud'] = evento.coordenadas.lon

    # Si se pide que se adjunten los datos de flickr, se hace
    if adjuntar_datos_flickr:
        if evento.flickrAlbumId:
            retorno['flickrAlbumID'] = evento.flickrAlbumId

        if evento.flickrUserId:
            retorno['flickrUserID'] = evento.flickrUserId

    return retorno


# Dada un evento devuelve un diccionario con una version extendida del evento
def evento_largo(evento, usuario_sesion=None):
    retorno = evento_corto(evento, True)

    retorno['categoriaList'] = [{'id': categoria.urlsafe(), 'nombre': categoria.get().nombre } for categoria in evento.categorias]
    retorno['creador'] = evento.key.parent().get().idGoogle
    # Descripcion completa
    retorno['descripcion'] = evento.descripcion

    retorno['validado'] = evento.validado

    # Devolver tambien el tipo del evento!
    retorno['tipo'] = evento.tipo

    # Fijar los me gusta que tiene el evento
    retorno['likes'] = buscar_numero_me_gusta_evento(evento)

    # Si se ha proporcionado un usuarion, se muestra si este le ha dado me gusta o no al evento
    if usuario_sesion is not None:
        # Indicar si el usuario que tiene la sesion iniciada le ha dado me gusta a este evento
        retorno['meGusta'] = usuario_ha_dado_me_gusta(usuario_sesion, evento)

    return retorno


# Dada una clave de un evento como urlsafe devuelve el evento o una excepcion

def clave_evento_o_fallo(eid):
    try:
        k = ndb.Key(urlsafe=eid)
        if not k.get():
            raise AgendamlgNotFoundException.evento_no_existe(eid)
        return k
    except Exception:
        raise AgendamlgNotFoundException.evento_no_existe(eid)

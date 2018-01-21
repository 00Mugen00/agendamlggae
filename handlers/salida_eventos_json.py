#!/usr/bin/env python
# -*- coding: utf-8 -*-

import util
from facades.evento import evento_corto, evento_largo, obtener_foto_url


def eventos_json(eventos, version_corta=True):
    """
    Dada una lista de eventos devuelve el json correspondiente para ser enviado al navegador
    :param eventos: list Eventos para ser convertidos a JSON
    :param version_corta: bool, indica si se quiere que se muestre la version corta de estos
    :return:
    """

    eventos_dic = lista_eventos_diccionario(eventos, version_corta)

    return util.to_json(eventos_dic)


def lista_eventos_diccionario(eventos=None, version_corta=True):
    """
    Dada una lista de Eventos devuelve otra listas de estos en version diccionario listos
    para ser parseados a JSON

    :param eventos: list Eventos para ser convertidos a JSON
    :param version_corta: bool, indica si se quiere que se muestre la version corta de estos
    :return:
    """
    if eventos is None:
        eventos = []

    if version_corta:
        # Se quiere la version corta de los eventos
        eventos_dic = [evento_corto(ev, True) for ev in eventos]

    else:
        # Se devuelve una version larga de los eventos
        eventos_dic = [evento_largo(ev) for ev in eventos]

    # Una vez hecho esto toca, de forma paralela, fijar el atributo fotoUrl de los eventos
    parallel = util.ParallelTasks()

    @parallel.async_call
    def foto_asincrono(evento):
        foto_url = obtener_foto_url(evento)
        if foto_url is not None:
            evento['fotoUrl'] = foto_url

        if version_corta:
            # Si se ha pedido la version corta de los eventos, se quitan los datos de flickr de estos
            evento.pop('flickrAlbumID', None)
            evento.pop('flickrUserID', None)

    [foto_asincrono(event) for event in eventos_dic]
    parallel.wait_ending()

    return eventos_dic

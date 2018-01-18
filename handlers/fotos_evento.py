#!/usr/bin/env python
# -*- coding: utf-8 -*-

import util.json
from base import BaseHandler
from facades.evento import evento_largo_clave, clave_evento_o_fallo
from facades.excepcion import AgendamlgException
from tokens import get_user_from_token
from flickr.photosets import get_photos


class FotosEventoHandler(BaseHandler):

    def get(self, claveEvento):
        # Esta ruta requiere de las mismas condiciones de permisos que la visualizacion de un
        # evento concreto
        # Obtener usuario para mostrar evento validado o no
        _, usuario = get_user_from_token(self.request.headers.get('bearer'), raise_for_unauthenticated=False)
        # Devuelve un evento concreto en version larga, proporcionada su clave en urlsafe

        claveEvento = clave_evento_o_fallo(claveEvento)
        eventoDic = evento_largo_clave(claveEvento, usuario)

        # Si el evento no esta validado lanzar excepcion, al no ser que el usuario este logueado y
        # sea o el creador o periodista
        if (not eventoDic['validado'] and usuario is None) or (
                not eventoDic['validado'] and usuario.tipo != 3 and usuario.key != claveEvento.parent()):
            # El usuario no tiene permisos para ver un evento sin validar
            raise AgendamlgException.sin_permisos(usuario)

        # Proceder a obtener el PhotoSet
        fotos_respuesta = {'fotos': []}

        # Si el evento tiene user id y album id se procede a obtener sus fotos
        if eventoDic.get('flickrUserID', None) is not None and eventoDic.get('flickrAlbumID', None) is not None:
            # Imprimimos lo que devuelve la peticion
            photo_set_photos = get_photos(eventoDic['flickrUserID'], eventoDic['flickrAlbumID'])

            # Si el objeto photoset no es None, proceder a rellenar la lista
            if photo_set_photos is not None:
                fotos_respuesta['fotoPrimariaUrl'] = photo_set_photos.primary.kind_large_size_url
                fotos_respuesta['fotos'] = [{'titulo': foto.title, 'url': foto.kind_large_size_url} for foto in photo_set_photos.photos]


        self.response.write(util.to_json(fotos_respuesta))

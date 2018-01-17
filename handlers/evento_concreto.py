#!/usr/bin/env python
# -*- coding: utf-8 -*-

import util.json
from base import BaseHandler
from facades.evento import evento_largo_clave, clave_evento_o_fallo, obtener_foto_url
from models import Usuario, agenda_key
from tokens import get_user_from_token
from google.appengine.ext import ndb
from facades.excepcion import AgendamlgException, AgendamlgNotFoundException


class EventoConcretoHandler(BaseHandler):

    def get(self, claveEvento):
        # Obtener usuario para mostrar evento validado o no
        _, usuario = get_user_from_token(self.request.headers.get('bearer'), raise_for_unauthenticated=False)
        # Devuelve un evento concreto en version larga, proporcionada su clave en urlsafe

        eventoDic = evento_largo_clave(clave_evento_o_fallo(claveEvento))

        if usuario is not None and usuario.tipo != 3 and not eventoDic['validado']:
            # El usuario no tiene permisos para ver un evento sin validar
            raise AgendamlgException.sin_permisos(usuario)

        # Muy importante, poner a este evento su fotoUrl
        foto_url = obtener_foto_url(eventoDic)

        if foto_url is not None:
            eventoDic['fotoUrl'] = foto_url

        self.response.write(util.to_json(eventoDic))

    def delete(self, claveEvento):
        """

        :param claveEvento: clave del evento como urlSafe
        :return: JSON de exito
        """
        # Para borrar un evento hay que estar autenticado
        _, usuario = get_user_from_token(self.request.headers.get('bearer'), raise_for_unauthenticated=True)

        # Obtener el evento
        eventoDic = clave_evento_o_fallo(claveEvento).get()

        if eventoDic is None:
            raise AgendamlgNotFoundException.evento_no_existe(None)

        # Comprobar que el evento pertenece al usuario o que este es tipo 3
        if usuario.tipo != 3 and eventoDic.key.parent() != usuario.key:
            # Excepcion por no tener permiso
            raise AgendamlgException.sin_permisos(usuario)

        #Proceder al borrado del evento
        eventoDic.key.delete()

        # Si se elimina con exito se devuelve este json
        self.response.write(r'{"status": "ok"}')
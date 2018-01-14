#!/usr/bin/env python
# -*- coding: utf-8 -*-

import webapp2
from facades import AgendamlgNotFoundException, AgendamlgException, NotAuthenticatedException
from util.json import to_json, from_json


class BaseHandler(webapp2.RequestHandler):
    """Handler Base para el resto de handlers"""
    def dispatch(self):
        """Añadir a todas las respuesta el header field de content type adecuado"""
        self.response.headers['Content-Type'] = 'application/json; charset=utf-8'
        super(BaseHandler, self).dispatch()

    def json_body(self):
        """Obtiene el cuerpo de la petición como un diccionario"""
        if self.request.body:
            return from_json(self.request.body)

    def handle_exception(self, exception, debug):
        if isinstance(exception, AgendamlgException):
            self.response.set_status(400)
            self.response.unicode_body = to_json({
                u'error': {
                    u'message': exception.mensaje_error,
                    u'otherMessage': str(exception.cause) if exception.cause is not None else None,
                    u'error_id': exception.error_id
                }
            })
        elif isinstance(exception, AgendamlgNotFoundException):
            self.response.set_status(404)
            self.response.unicode_body = to_json({
                u'error': {
                    u'message': exception.mensaje_error,
                    u'error_id': exception.error_id
                }
            })
        elif isinstance(exception, NotAuthenticatedException):
            self.response.set_status(401)
            self.response.unicode_body = to_json({
                u'error': {
                    u'message': exception.mensaje,
                    u'otherMessage': str(exception.causa) if exception.causa is not None else None,
                    u'error_id': exception.error_id
                }
            })
        elif isinstance(exception, webapp2.HTTPException):
            self.response.set_status(500)
            self.response.unicode_body = to_json({
                u'error': {
                    u'message': exception.message,
                    u'otherMessage': str(exception),
                    u'type': type(exception),
                    u'error_id': 1001
                }
            })
        else:
            self.response.set_status(500)
            self.response.unicode_body = to_json({
                u'error': {
                    u'message': str(exception),
                    u'otherMessage': exception.message,
                    u'type': str(type(exception)),
                    u'error_id': 1001
                }
            })

    def __do_error__(self, method):
        self.response.set_status(405)
        self.response.unicode_body = to_json({
            u'error': {
                u'message': u'Método no permitido',
                u'otherMessage': u'El método {} no está permitido para esta ruta'.format(method),
                u'error_id': 1002
            }
        })

    def get(self):
        self.__do_error__(u'GET')

    def post(self):
        self.__do_error__(u'POST')

    def put(self):
        self.__do_error__(u'PUT')

    def delete(self):
        self.__do_error__(u'DELETE')

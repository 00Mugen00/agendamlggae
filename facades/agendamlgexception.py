#!/usr/bin/env python
# -*- coding: utf-8 -*-

class AgendamlgException(Exception):
    def __init__(self,mensaje_error,error_id,cause=None):
        super(AgendamlgException,self).__init__()
        self.mensaje_error = mensaje_error
        self.error_id = error_id
        self.cause = cause

    @staticmethod
    def tipo_invalido(tipo):
        return AgendamlgException(u'Tipo de evento inválido {}'.format(tipo),1)
    
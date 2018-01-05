# -*- coding: utf-8 -*-

class AgendamlgNotFoundException(Exception):
    def __init__(self, mensaje_error, error_id):
        super(AgendamlgNotFoundException, self).__init__()
        self.mensaje_error = mensaje_error
        self.error_id = error_id

    @staticmethod
    def usuario_no_existe(idGoogle):
        return AgendamlgNotFoundException(u'No existe el usuario '+idGoogle, 11)
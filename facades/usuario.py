#!/usr/bin/env python
# -*- coding: utf-8 -*-

from models import Usuario


def buscar_usuarios_preferencias(categorias=None):
    """
    Dada una lista de categorias devuelve una lista de usuarios
    que están interesados en ellas
    :param categorias: list Categoria
    :return: list Usuario
    """

    if categorias is None:
        categorias = []

    if len(categorias):
        # Se proceden a obtener todos los usurios cuyas preferencias se encuentren entre
        # las categorias suministradas

        claves_categorias = map(lambda c: c.key, categorias)
        print claves_categorias
        resultado = Usuario.query(Usuario.preferencias.IN(claves_categorias)).fetch(projection=[Usuario.idGoogle, Usuario.tipo])
        return resultado

    else:
        return []

from google.appengine.ext import ndb

# Nombre de la agenda, se trata del id para la clave raiz de tipo "Agenda"

AGENDA_NOMBRE = 'AGENDAMLG'


""" 
Funcion que crea una clave raiz para las entidades,
de esta forma nos aseguramos que todas las entidades de la
agenda estan en el mismo "entity group" haciendo las consultas
en esta consistentes
"""

def agenda_key():
    """Construye una clave de DataStore de tipo Agenda, y con id
	AGENDA_NOMBRE
    """
    return ndb.Key('Agenda', AGENDA_NOMBRE)




# Modelo de evento

class Evento(ndb.Model):
    tipo = ndb.IntegerProperty()

    identity = ndb.StringProperty(indexed=False)
    email = ndb.StringProperty(indexed=False)


class Greeting(ndb.Model):
    """A main model for representing an individual Guestbook entry."""
    author = ndb.StructuredProperty(Author)
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)


class User()

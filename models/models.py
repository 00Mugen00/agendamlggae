from google.appengine.ext import ndb

# Nombre de la agenda, se trata del id para la clave raiz de tipo "Agenda"

AGENDA_NOMBRE = 'AGENDAMLG'


# Funcion que crea una clave raiz para las entidades,
# de esta forma nos aseguramos que todas las entidades de la
# agenda estan en el mismo "entity group" haciendo las consultas
# en esta consistentes


def agenda_key():
    # Construye una clave de DataStore de tipo Agenda, y con id
    # AGENDA_NOMBRE
    return ndb.Key('Agenda', AGENDA_NOMBRE)

# Modelo categoria
class Categoria(ndb.Model):
    nombre = ndb.StringProperty(required=True)

# Modelo de usuario
class Usuario(ndb.Model):
    idGoogle = ndb.StringProperty(required=True)
    tipo = ndb.IntegerProperty(required=True)
    preferencias = ndb.StructuredProperty(Categoria,repeated=True)

# Modelo de evento

class Evento(ndb.Model):
    tipo = ndb.IntegerProperty(required=True)
    nombre = ndb.StringProperty(required=True)
    descripcion = ndb.StringProperty(required=True)
    fecha = ndb.DateTimeProperty(auto_now_add=True, required=True)
    precio = ndb.FloatProperty()
    direccion = ndb.StringProperty(required=True)
    validado = ndb.BooleanProperty(default=False, required=True)
    creador = ndb.StructuredProperty(Usuario, required=True)
    latitud = ndb.FloatProperty()
    longitud = ndb.FloatProperty()
    flickrUserId = ndb.StringProperty()
    flickrAlbumId = ndb.StringProperty()
    categorias = ndb.StructuredProperty(Categoria, repeated=True)

# Modelo comentario
class Comentario(ndb.Model):
    texto = ndb.StringProperty()
    creador = ndb.StructuredProperty(Usuario, required=True)
    evento = ndb.StructuredProperty(Evento, required=True)
    fecha = ndb.DateTimeProperty(auto_now_add=True)


comentario = Comentario(texto='Hola',parent=agenda_key())
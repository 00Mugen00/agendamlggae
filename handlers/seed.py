# -*- coding: utf-8 -*-

"""
From https://github.com/melchor629/agendamlgr/blob/master/sql/seed.sql, imported everything into Google App Engine
Datastore, and adding invented comments and likes.
"""

from datetime import datetime as dt
import random
import re

from google.appengine.ext import ndb
from google.appengine.ext.ndb import GeoPt

from handlers.base import BaseHandler
from models import Categoria, Usuario, Evento, Comentario, MeGusta, agenda_key


def add_categories():
    Categoria(nombre=u'Teatro', parent=agenda_key()).put()
    Categoria(nombre=u'Cine', parent=agenda_key()).put()
    Categoria(nombre=u'Música', parent=agenda_key()).put()
    Categoria(nombre=u'Gastronomía', parent=agenda_key()).put()
    Categoria(nombre=u'Deporte', parent=agenda_key()).put()
    Categoria(nombre=u'Pintura', parent=agenda_key()).put()
    Categoria(nombre=u'Escultura', parent=agenda_key()).put()
    Categoria(nombre=u'Fotografía', parent=agenda_key()).put()
    Categoria(nombre=u'Videojuegos', parent=agenda_key()).put()
    Categoria(nombre=u'eSports', parent=agenda_key()).put()
    Categoria(nombre=u'Conferencia', parent=agenda_key()).put()
    Categoria(nombre=u'Cultural', parent=agenda_key()).put()
    Categoria(nombre=u'Informática', parent=agenda_key()).put()


def cat_id(num):
    id_to_name = [u'Teatro', u'Cine', u'Música', u'Gastronomía', u'Deporte', u'Pintura', u'Escultura', u'Fotografía',
                  u'Videojuegos', u'eSports', u'Conferencia', u'Cultural', u'Informática']
    return Categoria.query(Categoria.nombre == id_to_name[num-1]).fetch()[0].key


def cats_id(nums):
    return [ cat_id(_id) for _id in nums ]


def add_users():
    Usuario(idGoogle=u'113090457812971237278', tipo=3, preferencias=cats_id([ 1, 2, 3 ]), parent=agenda_key()).put()
    Usuario(idGoogle=u'107740629189585787589', tipo=2, preferencias=cats_id([ 1, 4, 5 ]), parent=agenda_key()).put()
    Usuario(idGoogle=u'117448827855359481250', tipo=1, preferencias=cats_id([ 1, 7, 9 ]), parent=agenda_key()).put()
    Usuario(idGoogle=u'101525104652157188456', tipo=3, preferencias=cats_id([ 1, 5, 9, 10, 11 ]), parent=agenda_key()) \
        .put()


def user_id(uid):
    return Usuario.query(Usuario.idGoogle == uid).fetch()[0].key


def parse_datetime(time_str):
    match = re.match(r'(\d+)-(\d+)-(\d+) (\d+):(\d+):(\d+).\d*', time_str)
    return dt(
        year=int(match.group(1)),
        month=int(match.group(2)),
        day=int(match.group(3)),
        hour=int(match.group(4)),
        minute=int(match.group(5)),
        second=int(match.group(6))
    )


def add_events():
    events = [Evento(
        tipo=1,
        nombre=u'Diseño De Personajes De Cómic',
        descripcion=u'''Una de las partes fundamentales a la hora de contar historias dibujadas, tanto en cómic como en
animación, consiste en diseñar bien los personajes que van a protagonizar nuestra historia. El objetivo de estas
 actividades dirigidas a un público adolescente y juvenil -de 13 a 18 años- sería que los asistentes aprendieran a crear
 cualquier personaje, superando las limitaciones que nos autoimponemos, con una base sólida y documentada, o en 
cualquier caso tener un punto de partida. Aunque se haga una breve introducción teórica explicando las bases del diseño 
de personajes, la actividad se centrará en la práctica, se verán diferentes estilos y también se intentará que los 
asistentes creen personajes desde cero. Cualquier estilo de dibujo puede ser apto para un proyecto personal; para ello 
se estudiarían diferentes estéticas, desde el "cartoon", pasando por el estilo "americano", "disney" o "manga". A lo 
largo de este curso-taller estudiaremos por dónde empezar, la teoría de las proporciones, la psicología de los 
personajes, la interpretación, postura, detalles, etc, así como ejemplos de diseñadores de personajes en la historia de 
la historieta. Teniendo en cuenta el contenido y las actividades programadas, se ha estimado una duración de tres 
semanas, una clase por semana de dos horas de duración cada una.''',
        fecha=parse_datetime(u'2018-01-31 11:26:42.76'),
        precio=12.99,
        direccion=u'Avenida de los Guindos, 48 29004, Málaga',
        validado=True,
        coordenadas=GeoPt(36.68969999999999, -4.44508),
        flickrUserId=u'142458589@N03',
        flickrAlbumId=u'72157667134867210',
        categorias=cats_id([1, 2, 3, 6, 9, 11]),
        parent=user_id(u'113090457812971237278')
    ).put(), Evento(
        tipo=2,
        nombre=u'The Primitals',
        descripcion=u'''Yllana y Primital Bros se unen para sorprendernos con una divertidísima comedia musical a capela.
Cuatro aborígenes de un planeta que podría ser el nuestro reclaman el escenario, dispuestos a conquistar al público – a 
carcajadas o a machetazos- pero siempre rebosando música de mil géneros que, como esponjas, han ido absorbiendo en sus 
viajes por los confines del espacio tiempo.
THE PRIMITALS... la extraña y surrealista historia de una tribu ligeramente disfuncional, con luchas intestinas, sueños 
de grandeza, desequilibrios mentales y farmacopea milenaria.
Chamanismo a cuatro voces. Tragicomedia a capela. Vanguardismo ancestral. Todo esto y mucho más en THE PRIMITALS.''',
        fecha=parse_datetime(u'2018-01-05 11:29:00.487'),
        precio=19.99,
        direccion=u'Calle Molina Lario, 9 29015 , Málaga',
        validado=True,
        coordenadas=GeoPt(36.72015160000001, -4.419282),
        flickrUserId=u'127818489@N07',
        flickrAlbumId=u'72157663381642946',
        categorias=cats_id([1, 2, 3, 6, 9, 11, 1, 3, 8]),
        parent=user_id(u'107740629189585787589')
    ).put(), Evento(
        tipo=3,
        nombre=u'La Útlima Salida de Sancho Panza',
        descripcion=u'''El Ayuntamiento de Estepona, a través del Área Sociocultural y Servicios, informa que la Compañía
 Escudero Andante Teatro presentará el viernes, 1 de diciembre de 2017, a las 20:00 horas, en el Auditorio Felipe VI, la
 obra "La última salida de Sancho Panza", a beneficio de Cáritas Española. Con esta obra de Ignasi García y dirección de
 Andreu, y protagonizada por Jesús Luque en el papel de Sancho, se presentó esta compañía, nacida de la mano de J. Luque
 y Chus Bernal. Desde su exitoso estreno el pasado mes de febrero, en el Centro Cultural Padre Manuel, ha ido haciéndose
 un hueco en el panorama escénico nacional. Luque: "la colaboración de "Andreu" en la 3 dirección escénica, con más de 
30 espectáculos a sus espaldas, y uno de los fundadores de la compañía malagueña InduoTeatro, que lleva ya casi 10 años 
de vida, y la generosidad de Ignasi García escribiendo el texto para la compañía, aportan un plus de calidad al
proyecto" que, en palabras de su autor, podríamos resumir así: Sinopsis: Tras la muerte de Don Quijote, Sancho Panza ha 
intentado volver a su antigua vida de labriego, pero no ha podido. Pesa demasiado en su ánimo el recuerdo de las 
aventuras que vivió con su señor, y siente que, de alguna manera, le está fallando por no seguir con el cometido de 
satisfacer agravios, enderezar entuertos, castigar insolencias y vencer gigantes. Y más en los tiempos presentes, en los
 que sigue habiendo tantas o incluso más injusticias que antes. Sancho, además, se ve capaz de intentar ser de nuevo 
gobernador de una ínsula porque, en vistas de cómo gobiernan actualmente los políticos, piensa que él no lo hizo tan 
mal. Así pues, alternando fragmentos adaptados de la novela con un lenguaje más contemporáneo, en un mundo rural en el 
que tecnología empieza a invadirlo todo, Sancho ensaya ante una silla cómo decirle por enésima vez a Teresa Panza, su 
esposa, que esta vez sí se irá y no podrá retenerle. Y es que... si estuviéramos en el lugar de Sancho Panza, ¿podríamos
 volver a nuestra antigua vida, después de las experiencias y aventuras compartidas con Don Quijote? ¿Cómo 
sobrellevaríamos el vacío que deja la ausencia del amigo? ¿Podríamos permanecer indiferentes a esas injusticias y 
agravios que intentamos reparar en su compañía? ¿Serían esas injusticias del s. XVI muy distintas a las que existen en 
nuestro Siglo XXI? Este es el viaje que el autor propone al espectador en la obra, acompañar a un Sancho Panza que 
intenta seguir con su vida tras la muerte de don Quijote, en sus dudas, sus sueños, sus esperanzas y sus frustraciones. 
Parte de la recaudación se destinará a Cáritas Parroquial de San José Estepona.''',
        fecha=parse_datetime(u'2017-12-28 11:30:53.035'),
        precio=9.99,
        direccion=u'Plaza Ignacio Mena, 143 29680, Estepona',
        validado=True,
        coordenadas=None,
        flickrUserId=u'51283549@N02',
        flickrAlbumId=u'72157624693864784',
        categorias=cats_id([1, 3, 8, 4]),
        parent=user_id(u'107740629189585787589')
    ).put(), Evento(
        tipo=2,
        nombre=u'P05. J.L. Turina, M. Castelnuovo-Tedesco',
        descripcion=u'''Director MANUEL HERNÁNDEZ SILVA
–
Fantasía sobre una fantasía de Alonso Mudarra, J.L. Turina
Concierto para guitarra en re mayor, Op.99, M. Castelnuovo-Tedesco
Marco Socías guitarra
– –
Sinfonía nº 1 en sol menor, V. Kalinnikov

1.15 h. (c/i)
orquestafilarmonicademalaga.com

Encargada por la Orquesta Sinfónica de Tenerife, la Fantasía sobre una fantasía de Alonso Mudarra fue compuesta por 
José Luis Turina en la primavera de 1988. Pensada para el lucimiento de la mencionada formación, especialmente en la 
sección de metales, recrea las falsas que contiene la Fantasía X para vihuela del aludido músico del siglo XVI.
Andrés Segovia es el peticionario, dedicatario, asesor y primer intérprete del Concierto para guitarra en re mayor del 
compositor florentino de ascendencia sefardí Mario Castelnuovo-Tedesco, que lo terminó de escribir en el mes de enero 
de 1939, antes de emigrar a Estados Unidos a causa de la persecución de judíos en Italia.
Tres hechos marcaron la vida de Vasili Kalinnikov; la imposibilidad de su familia de costearle sus estudios en el 
conservatorio, enfermar de tuberculosis, y cierto aislamiento de los principales centros musicales de Rusia al tener 
que residir en Crimea por razones de salud. Su memoria ha quedado vinculada a su Sinfonía nº 1 compuesta entre 1894 y 
1895.''',
        fecha=parse_datetime(u'2018-01-22 11:32:56.201'),
        precio=24,
        direccion=u'C/ Ramos Marín, s/n 29012, Málaga',
        validado=True,
        coordenadas=GeoPt(36.7245972, -4.4184243),
        flickrUserId=u'144925109@N04',
        flickrAlbumId=u'72157673558721461',
        categorias=cats_id([4, 1, 7]),
        parent=user_id(u'113090457812971237278')
    ).put(), Evento(
        tipo=1,
        nombre=u'Stingers (Tributo A Scorpions) + Güru',
        descripcion=u'''STINGERS, la mejor banda tributo a Scorpions del mundo además de hacer un importante repaso a la 
extensa carrera de los alemanes se permitirá el lujo de dar a conocer, recien sacado del horno su primer larga duración 
de temas propios muy muy a lo SCORPIONS, hazte con él si te gusta la banda alemana, recomendadisimo.

GURU, la banda del conocido guitarrista David Palau presenta su último trabajo "RED" aquí en Sevilla por primera vez. 
Grupazo, no te los pierdas.''',
        fecha=parse_datetime(u'2017-12-14 11:34:48.519'),
        precio=10.00,
        direccion=u'Calle la Orotova, 25 29006, Málaga',
        validado=True,
        coordenadas=GeoPt(36.7048592, -4.4764286),
        flickrUserId=u'clickclique',
        flickrAlbumId=u'72157600621551614',
        categorias=cats_id([1, 7, 1, 8, 11]),
        parent=user_id(u'107740629189585787589')
    ).put(), Evento(
        tipo=3,
        nombre=u'Concierto de Navidad Jingle Bells',
        descripcion=u'''El Ayuntamiento de Estepona, a través del Área Sociocultural y Servicios, informa que la artista 
Oksana Kraynichuk volverá el próximo viernes, 1 de diciembre de 2017, al Centro Cultural Padre Manuel, donde ofrecerá el
 Concierto de Navidad "Jingle Bells", con interpretaciones de piano y voz. La pianista y cantante ucraniana presenta un
selecto programa con grandes canciones, como "The Beautiful Blue Danube" de Johann Strauss Jr., "Beautiful Blue Danube",
 "Let it Snow", "White Christmas", "Winter Wonderland", "Noche de Pax" y "Jingle Bell Rock", entre otras
muchas. Oksana Kraynichuk nació en Ucrania. Está diplomada en música por el Conservatorio Profesional Estatal de D.V. 
Sichinskyy. Desde 8 años actúa como cantante y pianista en grupos y como solista e imparte clases de música. Llegó a 
España en 2001, y reside en la Costa del Sol.''',
        fecha=parse_datetime(u'2018-03-16 11:39:58.161'),
        precio=5.00,
        direccion=u'C/ San Fernando, 2 29680, Estepona',
        validado=True,
        coordenadas=GeoPt(36.4302, -5.15186),
        flickrUserId=u'82567656@N06',
        flickrAlbumId=u'72157686606416222',
        categorias=cats_id([1, 8, 11, 4, 7, 8, 9]),
        parent=user_id(u'113090457812971237278')
    ).put(), Evento(
        tipo=2,
        nombre=u'Casita Navidad',
        descripcion=u'''La casita de Navidad de Muelle Uno es el lugar más acogedor y Slow de toda Málaga. El mismísimo 
Papá Noel pasa toda esta temporada viviendo allí y recibiendo a los peques para darles caramelos y recibir sus cartas. 
Y como no puede ser de otra manera, también el Paje de los Reyes Magos se instala unos días para que todos los peques 
puedan conocerlo y pedirles sus deseos, que él transmitirá a sus majestades el 5 de enero.''',
        fecha=parse_datetime(u'2018-02-09 11:42:16.679'),
        precio=15.99,
        direccion=u'Puerto de Málaga, s/n 29001, Málaga',
        validado=True,
        coordenadas=GeoPt(36.7141686, -4.422710299999999),
        flickrUserId=u'64056743@N07',
        flickrAlbumId=u'72157652310686415',
        categorias=cats_id([4, 7, 8, 9, 2, 8, 9, 10]),
        parent=user_id(u'107740629189585787589')
    ).put(), Evento(
        tipo=3,
        nombre=u'Historia Del Flamenco, Con Juan Vergillos',
        descripcion=u'''Muchos son los puntos de conexión entre el brazo cultural de la Sociedad General de Autores y 
Editores, la Fundación SGAE, y el centro de creación contemporánea La Térmica, dependiente de la Diputación de Málaga. 
En este caso, con el objetivo común de ofrecer visibilidad a la obra de creadores así como a diversas propuestas 
formativas en torno al arte jondo, ambas entidades han sellado un convenio de colaboración cultural por el que organizan
 una serie de actividades en torno al mundo flamenco.

Una historia del flamenco elaborada a partir de los últimos hallazgos de la investigación. Estudiaremos los orígenes del
 flamenco y su evolución, desde las danzas barrocas, pasando por los bailes de palillos, el nacimiento de lo jondo en el
 contexto del romanticismo andaluz, los cafés cantantes, las vanguardias, la posguerra y la realidad actual de los 
festivales globales. Veremos en acción y escucharemos a los grandes creadores e intérpretes de la historia del flamenco,
 desde las grabaciones en cilindros de cera del siglo XIX hasta hoy. Asistiremos al nacimiento de cada uno de los 
 estilos del flamenco, bien a través de documentación fidedigna o, desde 1894, con una selección de películas, muchas 
 de ellas inéditas, protagonizadas por los grandes bailaores de la historia. Por primera vez se explica la Historia del 
 Flamenco en el marco general de la Historia del Arte y de la Historia de España.

El taller se articula a través de explicaciones, visionado de películas, pinturas, grabados, fotografías y otros 
documentos históricos, esquemas, mapas, audiciones con comentarios del profesor y de los miembros del taller, 
coordinados por el profesor.''',
        fecha=parse_datetime(u'2018-02-25 11:44:47.191'),
        precio=12.00,
        direccion=u'Avenida de los Guindos, 48 29004, Málaga',
        validado=True,
        coordenadas=GeoPt(36.68969999999999, -4.44508),
        flickrUserId=u'158969919@N03',
        flickrAlbumId=u'72157686508330221',
        categorias=cats_id([2, 8, 9, 10, 4, 6, 7, 9]),
        parent=user_id(u'113090457812971237278')
    ).put(), Evento(
        tipo=1,
        nombre=u'La Igualdad Como Práctica Creadora ',
        descripcion=u'''Ellas y ellos

No cabe duda de que la cultura refleja la sociedad, pero también produce efectos sobre ella: crea relatos, modela
subjetividades, naturaliza y legitima comportamientos, o al contrario, los cuestiona y propone otros modelos. Por eso, 
la cultura es un terreno crucial para plantearnos la pregunta sobre la condición femenina, sobre todo en sociedades como
 la nuestra en las que impera la igualdad formal entre los sexos, pero en las que incomprensiblemente, se perpetúa una 
desigualdad real que ya no puede explicarse apelando a las leyes, a la religión oficial o a la falta de educación de 
las mujeres. De ahí que sea tan importante analizar los mecanismos, sutiles y a menudo inconscientes, que operan en las
 artes plásticas, el cine, la publicidad, la ciencia, el teatro, la literatura… en lo que se refiere a la representación
 de mujeres y hombres, una representación de cuya influencia sobre la realidad somos cada vez más conscientes. En este 
ciclo global hablaremos de feminismos no excluyentes, de evolución de la mirada femenina integradora.

"La igualdad como práctica creadora y activismo feminista en el sistema de las artes."

1ª parte: Como indicadores significativos de la creación escénica de mujeres se proyectarán imágenes del ámbito 
iberoamericano para señalar lo diverso de sus narrativas y lenguajes, divulgar contenidos y estimular el estudio y la 
distribución. El arte escénico de creadoras no es del todo reconocido con el rango emblemático que merece.

2ª parte: La Ley Igualdad MH 3/2007 necesita implicación de la sociedad civil para su cumplimiento. Esta conciencia 
activista ya tuvo fundamento en O. de Gouges, María Lejárraga y H.G. Wells. Se aportarán materiales, estrategias, formas
 organizativas y la Hoja de Ruta del Mouvement HF en Francia, adoptada en CyM, sus resultados aquí, y el avance hacia 
Europa que adoptamos durante los Estados Generales de la Cultura (Lyon, 2016).

El taller tiene características de divulgación de imágenes y contenidos de determinadas creaciones escénicas de autoras 
y directoras contemporáneas, significativas del ámbito del habla hispana y portuguesa. Incluye información detallada de 
los elementos del programa "Temporadas Igualdad Mujeres Hombres en las artes escénicas" que divulga Clásicas y Modernas 
y para cuya hoja de ruta se suman adhesiones en todo el país .

Dirigido a personas interesadas o formadas en teatro, danza, performance o video, ya sea como estudiantes, creadora/es, 
y profesionales de diseño, producción, distribución o gestión cultural. Investigadora/es de la escena contemporánea 
interesados en la perspectiva de género. Periodistas culturales y de la crítica de espectáculos. También espectadora/es 
con fundamentos de teoría feminista, o interés por combatir el desigual de acceso de las obras de creadoras 
contemporáneas.''',
        fecha=parse_datetime(u'2018-02-04 11:50:15.352'),
        precio=14.00,
        direccion=u'Avenida de los Guindos, 48 29004',
        validado=True,
        coordenadas=GeoPt(36.68969999999999, -4.44508),
        flickrUserId=u'150697594@N06',
        flickrAlbumId=u'72157684396891654',
        categorias=cats_id([4, 6, 7, 9, 11]),
        parent=user_id(u'107740629189585787589')
    ).put(), Evento(
        tipo=1,
        nombre=u'Amy',
        descripcion=u'''Documental "Amy" (2015), con British Council / 21.30 horas

Director: Asif Kapadia.Sobre la famosa cantante Amy Winehouse. Duración 128 minutos

Documental sobre la famosa cantante británica Amy Winehouse, que cuenta con imágenes inéditas de archivo y entrevistas 
con la malograda estrella, que murió en julio del 2011 a los 27 años de edad por parada cardíaca consecuencia de sus 
excesos con las drogas y el alcohol, adicciones agravadas por su bulimia. Amy Winehouse, ganadora de 6 Premios Grammys, 
se vio desde muy joven afectada por el divorcio de sus padres. Tenía un talento natural para el jazz y el soul y una voz
 prodigiosa que pronto la hizo una estrella mundial a pesar de lanzar sólo dos discos, pero la fama, la prensa 
sensacionalista, los intereses de la industria -y de su entorno- y su turbulento amor con el que fue su pareja Blake 
Fielder-Civil la condujeron finalmente a su trágico destino en su piso de Camden, Londres. (FILMAFFINITY)''',
        fecha=parse_datetime(u'2018-01-31 11:53:22.991'),
        precio=7.99,
        direccion=u'Avenida de los Guindos, 48 29004, Málaga',
        validado=True,
        coordenadas=GeoPt(36.68969999999999, -4.44508),
        flickrUserId=u'142458589@N03',
        flickrAlbumId=u'72157628580032735',
        categorias=cats_id([11, 2, 5, 11]),
        parent=user_id(u'117448827855359481250')
    ).put(), Evento(
        tipo=3,
        nombre=u'Rastro Cultural Nocturno',
        descripcion=u'''Desde noviembre de 2014, La Térmica ha celebrado 20 ediciones del rastro Cultural con stands, 
puestos gastronómicos así como animación musical y escénica. En esta nueva temporada esta actividad evoluciona y pasa a 
celebrarse el primer viernes de cada mes, por la noche, a partir de las 19.00 horas.

Además de la incorporación de nuevas propuestas, contará con la presencia de músicos, desfiles de moda, dju's, una pista 
de patinaje, programas de cortometrajes, puestos gastronómicos y mucho más. Hay más de 40 puestos nuevos, donde el 
público encontrará objetos y colecciones de decoración, ilustración y grabados, antigüedades, juguetes vintage, vinilos,
 cdu's y casettes, marcas de ropa y complementos, puestos de cerámica, merchandising, reciclaje de objetos, fotografía, 
interiorismo y letreros, merchandising y mucho más.

Una iniciativa que viene a poner en valor el coleccionismo, una actividad que consiste en la agrupación y organización 
de objetos de una determinada categoría según el gusto de las personas y que aglutina a adeptos en todo el mundo. De 
esta forma, los aficionados malagueños encontrarán un nuevo punto de encuentro donde lo u'vintage' cobra más sentido, 
en un tiempo en el que objetos de valor cultural de décadas pasadas están muy revalorizados.''',
        fecha=parse_datetime(u'2018-05-12 11:54:30.104'),
        precio=8.99,
        direccion=u'Avenida de los Guindos, 48 29004, Málaga',
        validado=True,
        coordenadas=GeoPt(36.68969999999999, -4.44508),
        flickrUserId=u'40116219@N08',
        flickrAlbumId=u'72157684241220423',
        categorias=cats_id([2, 5, 11, 1, 2, 5, 7, 8]),
        parent=user_id(u'117448827855359481250')
    ).put(), Evento(
        tipo=2,
        nombre=u'El Hilo De Sangre',
        descripcion=u'''Este ciclo toma el sello de las actividades del festival literario anual Málaga 451 para 
emprender una programación que incluya presentación de novedades editoriales, puntos de encuentro y reflexión sobre los 
caminos de la palabra escrita y citas para amplificar las tendencias más interesantes del panorama editorial nacional e 
internacional.

Ernesto Mallo: El hilo de sangre
Presenta: Antonio Fontana
1 de diciembre dentro del Rastro Cultural, 20:00 horas
El hilo de sangre
Un inesperado giro del destino ha hecho súbitamente rico al Perro Lascano: el comisario ha recuperado el amor de Eva y 
se ha jubilado de su puesto en la policía. Su vida se ha vuelto previsible, tranquila y segura. Pero, siendo desde 
siempre un hombre de acción, el Perro no sabe aburrirse. Por eso, cuando un criminal que agoniza en un hospital 
penitenciario dice saber quién asesinó a los padres de Lascano cuando este era solo un niño, el excomisario se embarca 
de inmediato en una obsesiva persecución entre Buenos Aires y Barcelona, poniendo así en peligro cuanto ama, para 
despejar la incógnita que lo ha acompañado toda la vida. Pero la verdad que le aguarda será muy distinta de cuanto 
hubiera podido imaginar…

Intenso, emocionante y conmovedor, el último caso del ya mítico investigador creado por el argentino Ernesto Mallo es 
mucho más que una novela policiaca. Se trata de un relato certero y desnudo sobre la condición humana, construido como 
un preciso mecanismo de relojería que, a la vez que tensa y pone en guardia todos los sentidos del lector, fascinado y 
temeroso por lo que pueda acontecer a continuación, lo empuja inevitablemente a volver la página y dejarse arrastrar de 
lleno por la inigualable potencia de lo narrado. Justo Navarro, para Babelia.

Ernesto Mallo (La Plata, 1948), guionista, dramaturgo y periodista independiente argentino. Ganó entre otros, el Premio 
Memorial Silverio Cañada de la Semana Negra de Gijón (2007). Ha publicado, además de las novelas de la serie del 
comisario Lascano, El relicario y Me verás caer, y más de diez obras de teatro. Sus novelas han sido traducidas a doce 
idiomas.''',
        fecha=parse_datetime(u'2017-12-27 11:56:07.64'),
        precio=6.99,
        direccion=u'Avenida de los Guindos, 48 29004, Málaga',
        validado=True,
        coordenadas=GeoPt(36.68969999999999, -4.44508),
        flickrUserId=u'142458589@N03',
        flickrAlbumId=u'72157645580501643',
        categorias=cats_id([1, 2, 5, 7, 8, 5, 6, 7, 10]),
        parent=user_id(u'107740629189585787589')
    ).put(), Evento(
        tipo=2,
        nombre=u'Comparativa fotográfica',
        descripcion=u'''Sala de exposiciones "El Portón"
Exposición: "Comparativa fotográfica. Ayer y hoy Alhaurín de la Torre".
Artista: Mª Carmen Carrera Sedeño

Descripción:
Nos adentra en los orígenes de la localidad mediante imágenes o grabados de los siglos XVIII al
XXI, para que desde esas imágenes hacer las mismas fotografías dentro de lo posible en la
actualidad.
Todo ello desde el punto de vista de una fotografa lugareña.
El proyecto de investigación ofrece un recorrido por la historia contemplando los profundos
cambios sociales, urbanos y culturales de la villa.
La muestra está compuesta por fotomurales de grandes dimensiones, que acompañados de textos
informativos permiten al espectador apreciar la importante transformación que ha experimetado la
localidad.
Nada tiene que ver el Laulin medieval y el Laurinejo de fuertes contrastes entre terratenientes y el
pueblo llano calzando alpargatas, con el Alhaurín de la Torre actual, moderno y acogedor.
´Las imágenes antiguas han sio aportadas de fondos públicos y privados. Todos ellos están
reflejados en el catálogo.
Pasado y presentede unen en esta muestra fotográfica para disfrute de todos.''',
        fecha=parse_datetime(u'2018-03-28 11:57:13.632'),
        precio=7.99,
        direccion=u'C/ Juan Carlos I, s/n 29130, Alhaurín de la Torre',
        validado=True,
        coordenadas=GeoPt(36.6607403, -4.5711905),
        flickrUserId=u'142458589@N03',
        flickrAlbumId=u'72157668672403853',
        categorias=cats_id([5, 6, 7, 10, 2, 5, 7]),
        parent=user_id(u'117448827855359481250')
    ).put(), Evento(
        tipo=2,
        nombre=u'Hécate y La Frontera',
        descripcion=u'''Factoría Echegaray

Autor Samuel Pinazo
Con Carmen Baquero [Elena]
Ana Varela [Virginia]
Almudena Puyo [Ioana]
Dirección Jose Padilla
Tres mujeres planean introducir en Europa a un grupo de refugiadas, todas ellas mujeres jóvenes musulmanas. Elena y 
Virginia trabajaron para la misma empresa de telefonía como teleoperadoras; Ioana era la limpiadora. Las tres fueron 
despedidas cuando la empresa trasladó sus oficinas de atención al cliente a Colombia. La acción transcurre en la casa de 
Virginia, donde ha llegado Elena con Ioana, un personaje peculiar con quien Virginia no contaba para el viaje.''',
        fecha=parse_datetime(u'2018-03-13 11:59:35.967'),
        precio=20.99,
        direccion=u'Calle Echegaray, 6 29015, Málaga',
        validado=True,
        coordenadas=GeoPt(36.7214409, -4.4192984),
        flickrUserId=u'142458589@N03',
        flickrAlbumId=u'72157658962424370',
        categorias=cats_id([2, 5, 7, 1, 4, 9, 10]),
        parent=user_id(u'117448827855359481250')
    ).put(), Evento(
        tipo=1,
        nombre=u'Viejovenes',
        descripcion=u'''Sinopsis:

En 2015 los muchachos crearon un espectáculo con motivo de sus 12 años de
trayectoría. Desde entonces no han parado de realizar una multitud de actuaciones por todo el país. Con una asistencia 
que supera los 200.000 espectadores.

Ambos se presentan ahora como dúo cómico (nunca antes lo habían hecho de forma profesional), haciendo sketchs en directo
 y dejándose de tanto monólogo. En este segundo año han preparado alguna que otra sorpresa…

Viejovenes ¿Cómo lo veis? ¿Estáis preparados para esta movida tan tocha? No respondáis ahora, habladlo en casa y 
meditadlo antes de ir al teatro.

Avisamos: Venid descomidos son 2 horas de chorradas sin parar…''',
        fecha=parse_datetime(u'2017-12-20 12:00:50.423'),
        precio=5.99,
        direccion=u'Calle Córdoba, 9 29001, Málaga',
        validado=True,
        coordenadas=GeoPt(36.7165986, -4.4220161),
        flickrUserId=u'100174764@N05',
        flickrAlbumId=u'72157637236184805',
        categorias=cats_id([1, 4, 9, 10, 2, 12]),
        parent=user_id(u'113090457812971237278')
    ).put(), Evento(
        tipo=2,
        nombre=u'Presencias 45. Aplama 20 Años',
        descripcion=u'''INAUGURACIÓN: Viernes 24 de noviembre a las 19:30h

20 AÑOS DE APLAMA Y 45 PRESENCIAS
FRANCISCO JURADO TERNERO
PRESIDENTE DE APLAMA

Este título no puede resumir mejor nuestra labor de trabajo. Hemos
cumplido 20 años de vida activa dentro de las artes plásticas
malagueñas y a la misma vez hemos llegado a nuestra Presencias
número 45, colectiva en la que siempre intentamos aunar desde la
base a todos los artistas de APLAMA.
Las cifras de estos 20 años son mareantes, cientos de exposiciones
individuales y colectivas, certámenes, concursos de pintura al aire libre,
bienales, homenajes, charlas, subastas benéficas y un largo etcétera. Y
cómo no, dentro de las exposiciones colectivas las Presencias juegan
un papel muy activo e importante en nuestra labor, siendo toda una
seña de identidad de APLAMA que ha conseguido desde el primer
momento, hace ya 20 años, acuñar el término de Presencias como
algo propio y genuino, que no es otro que la presencia de todos y
cada uno de los artistas que conforman la asociación.
No ha sido fácil, detrás de cada exposición hay mucho trabajo, trabajo
que se multiplica con las Presencias, pues por regla general son
exposiciones muy multitudinarias y multidisciplinares y esta Presencias
45 es una muestra clara y fiel del espíritu de las Presencias, pues desde
la figuración a la abstracción, desde la base hasta llegar a artistas con
trayectorias plagadas de premios y reconocimientos, es posible tomar
el pulso del arte contemporáneo malagueño.
Desde ya, estamos trabajando por otros 20 años más en favor del arte
y por otras tantas Presencias.
Larga vida al arte y a las Presencias.''',
        fecha=parse_datetime(u'2018-02-27 12:02:25.847'),
        precio=29.99,
        direccion=u'Calle Molina Lario, 9 29015, Málaga',
        validado=True,
        coordenadas=GeoPt(36.72015160000001, -4.419282),
        flickrUserId=u'142458589@N03',
        flickrAlbumId=u'72157627573542024',
        categorias=cats_id([2, 12, 1, 7, 9]),
        parent=user_id(u'117448827855359481250')
    ).put(), Evento(
        tipo=3,
        nombre=u'Economistas en el Arte',
        descripcion=u'''Exposición para conmemorar el 50 aniversario de la Facultad de Ciencias Económicas y 
Empresariales. Se compone de acuarelas, óleos, fotografías...
Entrada gratuita''',
        fecha=parse_datetime(u'2017-12-13 12:05:28.127'),
        precio=14.99,
        direccion=u'Avda. Antonio Machado, 33 29630, Benalmádena',
        validado=True,
        coordenadas=GeoPt(36.5956045, -4.520447799999999),
        flickrUserId=None,
        flickrAlbumId=None,
        parent=user_id(u'113090457812971237278')
    ).put(), Evento(
        tipo=1,
        nombre=u'Como dos gotas de poesía',
        descripcion=u'''Inauguración de la exposición Como dos gotas de poesía
30 de noviembre a las 20 hs.

Exposición Como dos gotas de Poesía en la que los lenguajes poético y fotográfico se dan la mano. Organizada por Centro 
Cultural Generación del 27, dependiente de la Delegación de Cultura de la Diputación, esta exposición, comisariada por 
el fotógrafo Paco Negre, se inauguró en el mes de abril de este mismo año en las salas del Centro María Victoria Atencia
 (MAV) de Málaga y va a recorrer la provincia en los próximos meses a disposición de los municipios que la soliciten 
como, en este caso, el de Fuengirola.

Como sugiere su título, la exposición Como dos gotas de Poesía propone un diálogo entre imágenes de naturaleza e 
imágenes de arquitectura acompañadas por el verso de poetas. Producida por el Centro Cultural Generación del 27, dicha 
exposición presenta una serie de fotografías enfrentadas junto a una reunión de textos de poetas malagueños, o 
residentes en Málaga. Estas fotografías, obra de Nuria Morillo y Mercedes Higuero, representan el contraste de lo 
natural con la construcción humana, ilustrado con un comentario lírico. Estos poemas que acompañan a las fotos, 
recogidos en el catálogo, son obra de María Victoria Atencia, Rosa Romojaro, Cristina Consuegra, María Navarro, María 
Eloy-García, Violeta Niebla, Kris León, Isabel Bono, Carmen López, Alejandro Simón Partal, Abraham Gragera, 
Sergio Navarro, Isabel Pérez Montalbán, Ángel Luis Montilla, Aurora Luque, Chantal Maillard, Juan Manuel Villalba y 
María Cegarra. Autores que cedieron estos poemas para la exposición y que ahora los ven expuestos a doble página con lo 
que podemos apreciarlos tanto en su forma original manuscrita como en su transcripción tipográfica colocada enfrente 
para el pleno disfrute del lector.

Acompaña el catálogo Como dos gotas de Poesía, editado por el CEDMA, que recoge las imágenes y textos de esta 
exposición.''',
        fecha=parse_datetime(u'2017-12-31 12:06:46.896'),
        precio=12.99,
        direccion=u'Av. Juan Gómez, 12 29640 ',
        validado=False,
        coordenadas=GeoPt(36.5394652, -4.6253874),
        flickrUserId=u'142458589@N03',
        flickrAlbumId=u'72157648820582920',
        categorias=cats_id([1, 7, 9, 2, 3, 9]),
        parent=user_id(u'117448827855359481250')
    ).put(), Evento(
        tipo=3,
        nombre=u'Swing: Curso de Lindy Hop y Balboa',
        descripcion=u'''Número de plazas: Máximo 15 parejas. De 18 a 65 años.

Precio: 30 €/mes o 70 €/trimestre (Estos precios son por persona). Cada persona debe cumplimentar su solicitud,
independientemente de si se apunta en pareja o no.

Horario:

LINDY HOP.

Nivel 1 Iniciación (No has bailado nunca): Martes 19:45 – 20:45 horas.

Nivel 2 Iniciación (llevas bailando de 0 a 3 meses): Martes 20:45 – 21:45 horas.

Nivel Intermedio (llevas bailando de 6 meses a 1 año):

Grupo A lunes 19:45-20:45 horas.
Grupo B jueves, 20:45 – 21:45 horas.
Nivel Avanzado (llevas bailando de un año y medio en adelante): Lunes 20:45 – 21:45 horas.

BALBOA.

Nivel iniciación. Jueves 19:45 a 20:45 horas.

Sala 021



Lindy Hop y Balboa son dos estilos de bailes surgido al amparo de la música swing y que combinan elementos de pareja y 
bailes en solitario. Se popularizó en Nueva York por bailarines afro-americanos en una sala de baile llamada Savoy 
Ballroom. A mediados de la década de 1920 los bailarines del Savoy bailaban el estilo Charlestón, incorporando elementos
 de otros estilos como el "Texas Tommy", el "Black Bottom" y el "Cakewalk". Todos esos estilos y variaciones te los 
enseñaremos en este curso. Al ofrecerse en cinco niveles (Iniciación 1 y 2, Nivel Intermedio 1 y 2 y Avanzado) te 
permitirá tanto acercarte por vez primera a este estilo como perfeccionar las figuras básicas del Lindy hop (swing out, 
charlestón, tandem…) si ya hiciste el curso de iniciación anteriormente. O, por qué no, convertirte ya en un experto en 
los salones. También tendrás la oportunidad de estrenarte con el curso de Balboa. En el Lindy Hop hay dos roles: líder –
 la persona que suele tomar la iniciativa a la hora de marcar los pasos- y seguidor. Tradicionalmente, se ha asignado el
 rol de líder al hombre y el de seguidor a la mujer. Desde Málaga Swing, no obstante, queremos difuminar estas 
 diferencias y ofrecer a todas la personas que se apunte el aprendizaje de ambos roles. De este modo, se multiplican las
 opciones para bailar y disfrutar de la música. Por el momento, en Balboa, mantenemos una dinámica diferente en el que 
 cada persona aprende un único rol: leader o follower.

Málaga Swing es un colectivo local de bailarines y monitores movido por el interés y la pasión por esta danza alegre y 
energética. De forma periódica y espontánea, invaden espacios y organizan talleres para enseñarnos la fuerza de un baile
 con más de un siglo de historia. Desde su formación, están creando y fomentando la escena swing malagueña para poder 
 disfrutar de este baile más allá de las clases.''',
        fecha=parse_datetime(u'2018-02-24 12:16:56.408'),
        precio=4,
        direccion=u'Avenida de los Guindos, 48 29004, Málaga',
        validado=False,
        coordenadas=GeoPt(36.68969999999999, -4.44508),
        flickrUserId=None,
        flickrAlbumId=None,
        categorias=cats_id([2, 3, 9, 10, 11]),
        parent=user_id(u'107740629189585787589')
    ).put(), Evento(
        tipo=2,
        nombre=u'Teatro Cósmico',
        descripcion=u'''Sala de Exposiciones "Bryan Hartley Robinson"
Exposición: "Teatro Cósmico" Artista: Isaac Roldán

Biografía:
Isaac Roldan nace el 5 de junio de 1979 en Cártama (Málaga). Desde muy temprana edad, este
artista empezó a iniciarse en el dibujo aprendiendo técnicas e indagando cada vez más en el mundo
del arte y la pintura, destacando en el colegio en artes plásticas y manualidades. Su paso por la
adolescencia fue una transición rebelde y muy productiva en la práctica de otras vertientes artísticas
como son la escultura, la poesía e incluso la música. Participó en grupos y bandas de rock donde
compuso canciones y aportó su particular y surrealista forma de ver la vida, siendo líder vocalista
del grupo de punk malagueño" Kmorra" durante más de una década. En la actualidad, este
polifacético artista ha madurado su técnica de pintura acercando a galerías y exposiciones su trabajo
pictórico haciendo uso de la "cromoterapia", llevando una armonía de vibración curativa en la
mayoría de sus cuadros y trabajos. Su obra es fruto de su continua dedicación y estudio personal del
alma, reflejando en cada una de sus pinturas e ilustraciones una novedosa e impactante forma de
entender el mundo y la vida volcando su esencia en los diferentes estados de conciencia, en los
sueños y signos místicos para trasmitir mensajes de planos espirituales dando vida a infinitas
formas y paisajes surrealistas que hacen al espectador reflexionar y disfrutar de cualquiera de los
cuadros de la colección. Su temática es amplia y su base es el estudio al plano espiritual paseando
por el complejo mundo del subconsciente y las dimensiones no físicas, los temas conspiranoicos y
la crítica social, desde un profundo respeto y un punto de vista personal hacia el despertar de la
conciencia y la evolución humana con el arte y la pintura; en búsqueda de la felicidad y la paz.''',
        fecha=parse_datetime(u'2017-12-28 12:18:19.529'),
        precio=5.99,
        direccion=u'C/ Juan Carlos I, s/n 29130, Alhaurín de la Torre',
        validado=False,
        coordenadas=GeoPt(36.6607403, -4.5711905),
        flickrUserId=u'142458589@N03',
        flickrAlbumId=u'72157681205425174',
        categorias=cats_id([10, 11, 1, 2, 3]),
        parent=user_id(u'113090457812971237278')
    ).put(), Evento(
        tipo=1,
        nombre=u'Estepona CREA 2018',
        descripcion=u'''El Ayuntamiento de Estepona ha convocado la cuarta edición del Certamen "Estepona CREA" con el 
objetivo de promover e incentivar la cultura y el arte de los jóvenes entre 15 y 35 años, empadronados en Estepona.

Con carácter cíclico, cada año se establecen diferentes modalidades (Danza, Pintura, Literatura, Artes Visuales, 
Fotografía, Gastronomía, Moda, Música, Teatro, Artes Gráficas, Escultura…). Mientras que el Certamen debutó con las 
modalidades de Pintura y Danza en 2015, siguió Música y Literatura y teatro y fotografía, para el cuarto certamen 
"Estepona CREA 2018" se han establecido las modalidades de Escultura y Creación Audiovisual, con el fin de fomentar 
proyectos escultóricos y de vídeo creación, respectivamente, en los que destaquen la originalidad, calidad, creatividad,
 la innovación y la experimentación.

La inscripción, documentación y material solicitado deberá presentarse conforme a las bases, desde la fecha hasta el 31 
de diciembre de 2017 indicando el nombre del certamen "Estepona CREA" y la modalidad, en la siguiente dirección: 
Delegación de Cultura del Excmo.''',
        fecha=parse_datetime(u'2018-01-13 12:20:58.321'),
        precio=8.99,
        direccion=u'Plaza Ignacio Mena, 143 29680, Estepona',
        validado=False,
        coordenadas=None,
        flickrUserId=u'142458589@N03',
        flickrAlbumId=u'72157681049275611',
        categorias=cats_id([1, 2, 3, 4, 8, 9]),
        parent=user_id(u'117448827855359481250')
    ).put()]
    add_comments(events)
    add_likes(events)


def add_comments(events):
    melchor = user_id(u'113090457812971237278')
    john = user_id(u'107740629189585787589')
    antonio = user_id(u'117448827855359481250')
    manu = user_id(u'101525104652157188456')
    rand = random.randint

    for i in range(len(events)):
        day = i * 2 + 5
        month = 1 + day / 31
        day = 1 + day % 31
        Comentario(
            texto=u'¡¡ Madre mia como mola !!',
            fecha=dt(year=2018, month=month, day=day, hour=10 + i / 2, minute=rand(0, 59), second=rand(0, 59)),
            creador=manu,
            parent=events[i]
        ).put()

        if (i % 3) == 0:
            Comentario(
                texto=u'Ostia tu, m\'agrada això, asistiré 😁',
                fecha=dt(year=2018, month=month, day=day, hour=18 + (i % 5), minute=rand(0, 59), second=rand(0, 59)),
                creador=melchor,
                parent=events[i]
            ).put()
        elif (i % 3) == 1:
            Comentario(
                texto=u'Eh, una pena que no pueda ir, el horario me va mal :( Pero me gustaria ir, tiene buena pinta',
                fecha=dt(year=2018, month=month, day=day, hour=12 + (i % 4), minute=rand(0, 59), second=rand(0, 59)),
                creador=john,
                parent=events[i]
            ).put()
        elif (i % 3) == 2:
            Comentario(
                texto=u'⬆️😁💪🏿',
                fecha=dt(year=2018, month=month, day=day, hour=14 + (i % 7), minute=rand(0, 59), second=rand(0, 59)),
                creador=antonio,
                parent=events[i]
            ).put()


def add_likes(events):
    # https://stackoverflow.com/questions/18945109/how-to-delete-all-entities-for-ndb-model-in-google-app-engine-for-python
    melchor = user_id(u'113090457812971237278')
    john = user_id(u'107740629189585787589')
    antonio = user_id(u'117448827855359481250')
    manu = user_id(u'101525104652157188456')

    for i in range(len(events)):
        event = events[i]
        MeGusta(creador=melchor, parent=event).put() if (i % 5) == 1 else None
        MeGusta(creador=john,    parent=event).put() if (i % 4) == 1 else None
        MeGusta(creador=antonio, parent=event).put() if (i % 3) == 1 else None
        MeGusta(creador=manu,    parent=event).put() if (i % 2) == 1 else None


def do_it():
    ndb.delete_multi(Comentario.query().fetch(keys_only=True))
    ndb.delete_multi(MeGusta.query().fetch(keys_only=True))
    ndb.delete_multi(Evento.query().fetch(keys_only=True))
    ndb.delete_multi(Usuario.query().fetch(keys_only=True))
    ndb.delete_multi(Categoria.query().fetch(keys_only=True))

    add_categories()
    add_users()
    add_events()


class SeedHandler(BaseHandler):
    def get(self):
        self.put()

    def put(self):
        do_it()
        self.response.unicode_body = u'{"True": "False"}'

    def delete(self):
        ndb.delete_multi(Comentario.query().fetch(keys_only=True))
        ndb.delete_multi(MeGusta.query().fetch(keys_only=True))
        ndb.delete_multi(Evento.query().fetch(keys_only=True))
        ndb.delete_multi(Usuario.query().fetch(keys_only=True))
        ndb.delete_multi(Categoria.query().fetch(keys_only=True))
        self.response.unicode_body = u'{"True": "👌🏿"}'

# agendamlggae
Trabajo Ingeniería Web en Google App Engine

## Breve Introducción
agendamlggae proporciona un servicio REST, parecido a [agendamlgr][1] que nos permite gestionar eventos en Málaga.
Para mostrar la información acerca de los eventos se proporciona un cliente realizado con **Angular 2** y **Bootstrap**.      

## Características
agendamlggae proporciona los siguientes servicios:     
* Diferentes tipos de usuarios con diferentes permisos: anónimo, registrado, superusuario y periodista.      
* Iniciar Sesión y Cerrar Sesión, mediante Google OAuth 2.0.     
* Ver perfil de Usuario.    
* Ver todos los evento no caducados y validados
* Filtrar eventos en función de su categoría
* Filtrar eventos según su posición geográfica
* Creación de eventos
* Validación de eventos
* Eliminación de eventos
* Añadir álbums de Flickr para la visualización de imágenes en los eventos
* Visualización de mapa mediante Google Maps
* Envío de correo acerca de eventos recién publicados a usuarios interesados
* Envío de correo al usuario cuyo evento ha sido validado
el cliente permite acceder todos los servicios de la lista.

## Configuración
 1. Instalar las dependencias de Python con `pip install -t lib -r requirements.txt`
 2. Instalar dependencias de node.js del proyecto _webapp_ con `npm install`
 3. Compilar la versión _debug_ (`npm run build-debug`) o _release_ (`npm run build`) del cliente
 4. Crear el archivo `tokens/tokens.json` que tiene las *API-Keys* de Google y Flickr. Tiene esta estructura:
 `{ "jwt_token": "...", "google_api_key": "...", "flickr_api_key": "..."}`. El token JWT lo generas tu.
 5. Obtener los tokens Google OAuth de la consola de desarrollador y ponerlo en `tokens/oauth_tokens.json`.

## Quieres instalar AngularMaps (o cualquier otra nueva dependencia) y peta?
Si después del pull `npm install` no funciona, haz lo siguiente: `npm i -f` y luego `npm install`

## Requisitos
Hay que tener instalado:
* Python
* Google App Engine
* node.js

## Creado a partir de:
* [node.js][2] - Parte del frontend
* [Bootstrap 4][3] - Diseño y estrucutra del frontend
* [Angular][4] - Aplicación web y estructuración del código
* [AngularMaps][5] - Google Maps API para Angular
* [date-time-picker][6] - Polyfill bonito para `input[type="date-time-local"]` para Angular

## Autores
* **Antonio Ángel Cruzado Castillo**
* **John Carlo Purihin**
* **Melchor Alejo Garau Madrigal**
* **Manuel Jesús Rodríguez Rodríguez**

  [1]: https://github.com/melchor629/agendamlgr
  [2]: http://nodejs.org
  [3]: http://getbootstrap.com
  [4]: https://angular.io
  [5]: https://angular-maps.com
  [6]: https://github.com/DanielYKPan/date-time-picker


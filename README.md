# Creando Plugins Para Sublime Text
## 2017-10-17

Sublime Text es un editor de texto potente y __extensible__. Sus plugins se escriben en Python, y tiene un Python 3.3 interpreter que los corre.

[Su plugin API](https://www.sublimetext.com/docs/3/api_reference.html) está muy completo y bastante bien documentado.

Puedes importar cualquier módulo de la standard library con tus plugins, más los módulos `sublime` y `sublime_plugin` que exponen al plugin API, más [unos cuantos packages](https://github.com/wbond/package_control_channel/blob/master/repository/dependencies.json) que no están en la standard library.

Hoy vamos a explorar los plugins de Sublime Text y su API de 2 formas:

- escribir un plugin que abre directorios, archivos, y URLs
- explorar un cliente HTTP escrito para Sublime Text [que se llama Requester](https://github.com/kylebebak/Requester/)

Veremos que plugins útiles son bastante fáciles de escribir, y que Sublime Text puede ser una plataforma para crear aplicaciones muy poderosas usando Python.


## Preparación
- Instalar [Sublime Text 3](https://www.sublimetext.com/)
- Instalar [https://packagecontrol.io/installation](https://www.sublimetext.com/)
- Clonar este repo a su packages directory
- Abrir `commands.py`


## URL Opener
Vamos a escribir un plugin que agarra el texto seleccionado y lo abre como directorio, archivo, o URL, dependiendo de que opción es la apropiada. Queremos que tenga unas características básicas:

- construir selección
  + si están seleccionados uno o más caracteres, ellos se toman como la selección
  + si no está seleccionado ningún caracter, se expande la selección hasta llegar a caracteres __delimeter__: estos se pueden especificar por el usuario
- construir una ruta absoluta al directorio/archivo si la ruta no es absoluta
  + si la selección viene de un view que corresponde a un archivo, construye la ruta con el directorio del archivo como base
  + de lo contrario, checa si el window tiene un project, y toma el directorio del project como base
- abre el URL con el web browser si no correponse ni a un archivo ni a un directorio


### Mejoras
- ?
- ?


### Subiendo el Plugin a Package Control
Si escribes un plugin y te gustaría compartirlo con el mundo, el paso final sería [subirlo a Package Control](https://packagecontrol.io/docs/submitting_a_package).

No podríamos subir el plugin a Package Control porque ya existe uno similar que se llama [open-url](https://github.com/noahcoad/open-url/tree/st3), y no lo aceptarían. [Yo tengo un fork](https://github.com/kylebebak/open-url) que tiene más features por si lo quieren clonar directo a su directorio de paquetes. Hice un PR pero no me contestó.


## Requester
Abre el command palette usando <kbd>shift+cmd+p</kbd>, busca __Package Control: Install Package__, luego busca __Requester__ (no ~~Http Requester~~) e instálalo.

Para estar seguro que se instaló bien, reinicia Sublime Text (ciérrala y ábrela de nuevo). Corre __Requester: Show Interactive Tutorial__.


### Resumen
- Features básicos y sintaxis
  + Request Body, Query Params, Custom Headers, Cookies
  + Variables de ambiente
  + Sintaxis (Requests), Parser, y convenience methods
- UI y UX
  + Colecciones de peticiones y navegación
  + Pestañas de respuesta
  + Historial de peticiones
  + Guardando peticiones a su requester file
- Pruebas
  + Test Runner
    + Sintaxis
    + JSON Schema
    + Integración con build process (generar scripts de pruebas)
- Portabilidad y Equipos
  + Exportar a cURL, HTTPie
  + Importar de cURL
    * Debugging peticiones AJAX/XHR mandados por tu browser
    * <https://www.nytimes.com/>, `commentData.json`, `commentCount`
- Autenticación: Twitter API
  + Extensiones a Requester, `requests-oauthlib`
  + <https://developer.twitter.com/en/docs/api-reference-index>
  + Explorando hyperlinked APIs (HATEOAS)
- Bonus: GraphQL support

~~~py
###env
from requests_oauthlib import OAuth1
auth = OAuth1(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
###env

get('https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=stackoverflow&count=1000', auth=auth)
~~~

~~~py
requests.get('https://api.graphloc.com/graphql')
# curl ipinfo.io/ip
~~~


## Preguntas

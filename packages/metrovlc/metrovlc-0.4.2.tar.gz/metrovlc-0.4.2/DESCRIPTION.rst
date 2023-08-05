METROVLC
========

|pypi-version| |License|

Utilidad en línea de comandos para
`MetroValencia <http://www.metrovalencia.es/page.php?idioma=_es>`__,
también funciona como módulo.

Descripción
-----------

Recupera alguna de las funcionalidades de la web de MetroValencia.

Requerimientos
--------------

-  Python3

Instalación
-----------

.. code:: shell

    pip install metrovlc

Ayuda
-----

Uso
~~~

::

    # metrovlc --help
    usage: metrovlc [-h] [-b BONO] [-d ORIGEN DESTINO] [-ss] [-v]

    optional arguments:
      -h, --help            show this help message and exit
      -b BONO, --bono BONO  Bono info
      -d ORIGEN DESTINO, --horario ORIGEN DESTINO
                            Horarios para ORIGEN -> DESTINO
      -ss, --solo-saldo     Solo muestra el saldo disponible
      -v, --version         show program's version number and exit

Ejemplos
~~~~~~~~

.. code:: shell

    # Mirar saldo de tu tarjeta TuiN
    $ metrovlc -b 4065483771
    Bono: 4065483771, Título: TuiN, saldo: 5,67 Euros

    # Mirar saldo de tu tarjeta TuiN, solo saldo
    $ metrovlc -b 4065483771 -ss
    5,67

    # Horarios de Llíria a Campanar
    $ metrovlc -horarios lliria campanar

    Estación de Origen: Llíria
    Estación de Destino: Campanar
    Franja horaria: de 00:00 a 23:59
    Día: 16/03/2017
    Duración aproximada del trayecto: 48 minutos aprox.
    Para efectuar este trayecto es necesario un billete de las zonas: ABC
    De Llíria a Campanar, Trenes con destino: València Sud, Torrent Avinguda, Hora de salida

    02 | 02:38 | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
    06 | 06:09 | 06:37 | 06:52 | ----- | ----- | ----- | ----- | ----- |
    07 | 07:07 | 07:22 | 07:37 | 07:52 | ----- | ----- | ----- | ----- |
    08 | 08:07 | 08:22 | 08:39 | ----- | ----- | ----- | ----- | ----- |
    09 | 09:09 | 09:39 | ----- | ----- | ----- | ----- | ----- | ----- |
    10 | 10:09 | 10:39 | ----- | ----- | ----- | ----- | ----- | ----- |
    11 | 11:09 | 11:39 | ----- | ----- | ----- | ----- | ----- | ----- |
    12 | 12:09 | 12:39 | ----- | ----- | ----- | ----- | ----- | ----- |
    13 | 13:09 | 13:39 | ----- | ----- | ----- | ----- | ----- | ----- |
    14 | 14:09 | 14:37 | 14:52 | ----- | ----- | ----- | ----- | ----- |
    15 | 15:07 | 15:22 | 15:39 | ----- | ----- | ----- | ----- | ----- |
    16 | 16:09 | 16:39 | ----- | ----- | ----- | ----- | ----- | ----- |
    17 | 17:09 | 17:39 | ----- | ----- | ----- | ----- | ----- | ----- |
    18 | 18:09 | 18:39 | ----- | ----- | ----- | ----- | ----- | ----- |
    19 | 19:09 | 19:39 | ----- | ----- | ----- | ----- | ----- | ----- |
    20 | 20:09 | 20:39 | ----- | ----- | ----- | ----- | ----- | ----- |
    21 | 21:09 | 21:39 | ----- | ----- | ----- | ----- | ----- | ----- |
    22 | 22:09 | 22:41 | ----- | ----- | ----- | ----- | ----- | ----- |
    23 | 23:14 | ----- | ----- | ----- | ----- | ----- | ----- | ----- |

Como módulo
-----------

Es posible cargar el módulo ``metrovlc`` y utilizar su funcionalidad.

Ejemplo
-------

.. code:: python

    import metrovlc
    # Recupera el saldo a partir de tu número de tarjeta
    metrovlc.metrosaldo(4065483771)
    > ('TuiN', '10,44 Euros')

Licencia
--------

MIT

.. |pypi-version| image:: https://img.shields.io/pypi/v/metrovlc.svg?style=flat-square
   :target: https://pypi.python.org/pypi?:action=display&name=metrovlc
.. |License| image:: http://img.shields.io/badge/license-MIT-blue.svg?style=flat-square
   :target: LICENSE

IFTTT-CML
=========

|Codacy Badge|

ITFFF Custom *maker* launcher

Descripción
-----------

Una especie de utilidad para usar el ``Maker Event`` de IFTTT y que sea
fácilmente ampliable por plugins creados en Python.

Requerimientos
--------------

-  Python3

Una cuenta en IFTTT, y al un menos evento creado con ``Maker Webhooks``.
La clave (``key``) se puede pasar por parámetro o (mucho mejor) definir
la siguiente variable de entorno:

-  ``IFTTT_API_KEY``

Instalación
-----------

.. code:: shell

    $ pip install iftttcml

Uso
---

::

    usage: iftttcml [-h] [-e EVENT] [-p PARAMS] [-k KEY] [-v]

    optional arguments:
      -h, --help            show this help message and exit
      -e EVENT, --maker-event EVENT
                            Maker Event
      -p PARAMS, --params PARAMS
                            Params for maker Event in JSON
      -k KEY, --key KEY     IFTTT API key
      -v, --version         show program's version number and exit

Ejemplo creación nuevo evento paso a paso
-----------------------------------------

Podemos ver un ejemplo paso a paso:

-  `Ejemplo <EXAMPLE.md>`__

Eventos creados ya
------------------

people\_in\_space
~~~~~~~~~~~~~~~~~

Evento de ejemplo que envía a tu aplicación IFTTT el número de personas
en el espacio.

metrovlc\_sin\_saldo
~~~~~~~~~~~~~~~~~~~~

Recupera y te envía un mensaje a tu aplicación IFTTT usando el evento
``metrovlc_sin_saldo``.

Uso
^^^

::

    $ iftttcml --maker-event metrovlc_sin_saldo --params "{'bono': 3611230999, 'limite': 20}"

Y en tu movil aparecéra el mensaje:

::

    Tarjeta 3611230999: 18.3 Euros

.. |Codacy Badge| image:: https://api.codacy.com/project/badge/Grade/6e8f982ceb8347b888a5d4b57d35f64b
   :target: https://www.codacy.com/app/penicolas/ifttt-cml?utm_source=github.com&utm_medium=referral&utm_content=penicolas/ifttt-cml&utm_campaign=Badge_Grade



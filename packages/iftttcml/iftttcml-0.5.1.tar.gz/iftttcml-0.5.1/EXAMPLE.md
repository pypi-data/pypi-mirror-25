# EJEMPLO

Vamos a seguir paso a paso un ejemplo para que nos llegue una notificación
cuando el número de personas en el espacio sea mayor que 1.

## Crear un Maker Event en IFTTT

Seleccionamos en IFTTT:

 * IF THIS: `Maker Weebhooks`
 * EVENT NAME: `people_in_space`
 * THAT: `Notifications`, y añadir una variable `values1`

Quedaría así:

![iftttmakereventconfig](http://i.imgur.com/kuWQAs9.png)

## Generar un nuevo evento a partir de la plantilla

Partimos de la plantilla `iftttcml/events/template.py` y añadimos el código
siguiente que pasamos a estudiar, revisamos la plantilla:

### La plantilla, paso a paso

```python
# -*- coding: utf-8 -*-

from iftttcml import iftttmakerevent


def launch(key, event, params):
    """ TEMPLATE:
        Launch one maker events in IFTTT
            key: API IFTTT key
            event: Event of IFTTT
            params: dictionary of parameters """

    notify = False
    values = dict()

    # begin: write your magic code --------------------------------------------
    #
    # some_beautiful_code()
    #
    # notify = True or False
    # event parameters, if need
    # like values['value1'] = 'some text'
    #
    # end: write your magic code ----------------------------------------------

    # call ifttt event
    if notify:
        iftttmakerevent.call_event(key, event, values)
```

Únicamente tenemos que meter código entre el begin y el end, para al final
decidir por medio de la variable `notify` si vamos a notificar o no.
Resumiendo, tu te curras el código que quieras, y únicamente tendrás indicar:

 - `values`: Los posibles valores que tiene el evento
 - `notify`: Variable booleana que indica si hay que notificar o no


### La plantilla con las personas en el espacio

```python
# -*- coding: utf-8 -*-

import requests
import json
from iftttcml import iftttmakerevent


def launch(key, event, params):
    """ EXAMPLE PEOPLE IN SPACE
        Nofity if there is more tan params['min_people_in_space']
        people in space """

    notify = False
    values = dict()

    # Mi código
    # 1. how many people in space
    url = 'http://api.open-notify.org/astros.json'
    resp = requests.get(url)
    data = json.loads(resp.text)

    # 2. need launch maker event?
    if params['min_people_in_space'] < data['number']:
        values['value1'] = data['number']
        notify = True
    # Fin de mi código


    # 3. send event
    if notify:
        iftttmakerevent.call_event(key, event, values)

```

Las partes más importantes:

 - Recuperamos con requests las personas en el espacio, que utilizaremos para
   ver si tenemos que llamar a la notificación o no.
 - En caso de notificar, metemos la información en `values` y marcamos
   `notify`a `True`

Ahora podremos ver en nuestro movil la notificación:

![iftttnotify](http://i.imgur.com/FnmHUrCm.png)

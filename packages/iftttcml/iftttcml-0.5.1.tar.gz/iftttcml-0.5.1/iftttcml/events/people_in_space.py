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

    if 'min_people_in_space' in params:
        min_people_in_space = params['min_people_in_space']
    else:
        min_people_in_space = 1

    # Mi código
    # 1. how many people in space
    url = 'http://api.open-notify.org/astros.json'
    resp = requests.get(url)
    data = json.loads(resp.text)

    # 2. need launch maker event?
    if min_people_in_space < data['number']:
        values['value1'] = data['number']
        notify = True
    # Fin de mi código

    # 3. send event
    if notify:
        iftttmakerevent.call_event(key, event, values)

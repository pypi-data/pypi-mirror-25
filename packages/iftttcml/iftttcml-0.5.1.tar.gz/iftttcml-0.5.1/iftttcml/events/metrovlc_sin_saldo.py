# -*- coding: utf-8 -*-

import metrovlc
from iftttcml import iftttmakerevent


def launch(key, event, params):

    limite = params['limite']
    bono = params['bono']

    info = metrovlc.metrosaldo(bono)

    if float(info['saldo']) < limite:
        saldo_y_moneda = '{} {}'.format(info['saldo'], info['moneda'])
        values = {'value1': bono, 'value2': saldo_y_moneda}
        # llamo a ifttt
        iftttmakerevent.call_event(key, event, values)

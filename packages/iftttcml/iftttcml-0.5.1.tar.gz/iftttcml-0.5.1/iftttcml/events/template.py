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
    # nofity = True or False
    # event parameters, if need
    # like values['value1'] = 'some text'
    #
    # end: write your magic code ----------------------------------------------

    # call ifttt event
    if notify:
        iftttmakerevent.call_event(key, event, values)

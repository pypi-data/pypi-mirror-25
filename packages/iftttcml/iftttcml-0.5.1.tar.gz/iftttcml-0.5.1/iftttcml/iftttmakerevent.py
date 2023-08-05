# -*- coding: utf-8 -*-

import requests


def call_event(api_key, event, params):
    url = "https://maker.ifttt.com/trigger/{e}/with/key/{k}/".format(e=event,
                                                                     k=api_key)
    return requests.post(url, data=params)

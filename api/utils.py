# -*- coding: utf-8 -*-

"""
Fonctions utiles pour l'ensemble de l'API

"""

import json
import datetime


class MyJsonEncoder(json.JSONEncoder):
    """
    Hérite de json.JSONEncoder pour permettre la sérialization JSON des dates

    """

    def default(self, obj):
        if isinstance(obj, datetime.date):
            return obj.strftime('%d-%m-%Y')

        return json.JSONEncoder.default(self, obj)

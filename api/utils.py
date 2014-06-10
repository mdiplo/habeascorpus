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
            # On sérialie une date en ne mettant que son année
            return obj.strftime('Y')

        return json.JSONEncoder.default(self, obj)


def get_article_by_id(id, docid_file):
    """Renvoie l'index dans le corpus de l'article dont l'id est id"""

    with open(docid_file, 'r') as f:
        for i, line in enumerate(f):
            if id == int(line):
                return i


def get_article_by_corpus_number(n, docid_file):
    with open(docid_file, 'r') as f:
        for i, line in enumerate(f):
            if i == n:
                return int(line)

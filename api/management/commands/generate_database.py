# -*- coding: utf-8 -*-

"""
Génère la base de données sqlite nécessaire pour explorer le corpus.
"""

import glob
import os.path
import datetime
import json
from api import utils
from gensim import corpora
from django.core import management
from django.core.management.base import BaseCommand
from api.models import Topic, Document, DocumentTopic
from django.db import transaction
from django.db.models import Sum, Min, Max


class Command(BaseCommand):
    arg = 'Nom du corpus'
    #help = 'Génère la base de données du corpus corpus_name' => problème unicode

    def handle(self, *args, **options):

        corpus_data_dir = os.getcwd()

        tsv_corpus = glob.glob(os.path.join(corpus_data_dir, '*.tsv'))
        lda_corpus = glob.glob(os.path.join(corpus_data_dir, '*_lda.mm'))
        topics = glob.glob(os.path.join(corpus_data_dir, '*_topics.txt'))

        if not tsv_corpus:
            raise IOError("""Impossible de trouver le fichier .tsv
            dans le dossier %s""" % (os.getcwd()))
        if not lda_corpus:
            raise IOError("""Impossible de trouver le fichier _lda.mm
            dans le dossier %s""" % (os.getcwd()))
        if not topics:
            raise IOError("""Impossible de trouver le fichier topics.txt
            dans le dossier %s""" % (os.getcwd()))

        management.call_command('syncdb')
        topics = add_topics(topics[0])
        add_documents(tsv_corpus[0], lda_corpus[0], topics)
        for topic in topics:
            compute_topic_history(topic)


def add_topics(topics_file):
    """

    Ajoute les topics dans la table topics à partir du fichier topics.txt généré
    par lda.py

    :Parameters:
        -`topics_file`: Le fichier topics.txt contenant les topics

    """
    
    topics = []
    with open(topics_file, 'r') as inp:
        transaction.set_autocommit(False)
        for i, line in enumerate(inp):
            topic = Topic(related_words=line, weight_in_corpus=0)
            topic.save()
            topics.append(topic)
        transaction.commit()

    return topics

def add_documents(raw_corpus_file, lda_corpus_file, topics):
    """
    Ajoute dans la table documents les articles d'un fichier .tsv contenant 8 colonnes :
        - id_article
        - titre
        - chapo
        - texte
        - langue
        - auteur
        - mots
        - date
        
    Ajoute également les topics liés à chaque document.
        
    :Parameters:
        -`raw_corpus_file`: Le fichier .tsv contenant les documents
        -`lda_corpus_file`: Le fichier _lda.mm 
        -`topics` : Une liste l contenant tous les topics telle que l[i] = Topic(id = i+1)

    """
    try:
        lda = corpora.mmcorpus.MmCorpus(lda_corpus_file)
    except:
        raise IOError("""Impossible de charger le fichier _lda.mm""")
        
    with open(raw_corpus_file, 'r') as raw:
        raw.readline() #on ignore la première ligne qui contient les noms des colonnes
        transaction.set_autocommit(False)
        for docno, raw_line in enumerate(raw):
            #lda[docno] donne les topics associés au document raw_line sous la forme
            #d'une liste de tuples (id_topic, poids du topic id_topic dans le document docno)  
            print "Document n°" + str(docno)
            doc = Document.create_document(raw_line.rstrip().split('\t'))
            doc.save()
            for id_topic, weight_in_document in lda[docno]:
                doc_topic = DocumentTopic(document=doc,
                        topic=topics[id_topic],
                        weight_in_document=weight_in_document)
                doc_topic.save()

            if docno % 1000 == 0:
                transaction.commit()


def compute_topic_history(topic):
    """
    Calcule l'historique du topic sous la forme d'un dictionnaire
    {year: weight, ...} où weight est le poids du topic calculé sur tous les
    articles écrits avant year. Ainsi, on peut retrouver le poids entre 
    year1 et year2 par soustraction.

    """

    bounds = Document.objects.aggregate(min_date=Min('date'), max_date=Max('date'))
    firstyear = bounds['min_date']
    lastyear = bounds['max_date']

    history = []
    total_weight = 0
    for year in range(firstyear.year, lastyear.year+1):
        query = DocumentTopic.objects.filter(document__date__year=year).\
                filter(topic__id=topic.id).\
                aggregate(weight=Sum('weight_in_document'))

        if query['weight']:
            history.append({'date': datetime.date(year, 1, 1), 'weight': query['weight']})
            total_weight += query['weight']
        else:
            history.append({'date': datetime.date(year, 1, 1), 'weight': 0.0})

    topic.history = json.dumps(history, cls=utils.MyJsonEncoder)
    print topic.history
    #poids total = poids des articles écrits avant lastyear
    topic.weight_in_corpus = total_weight
    topic.save()
    transaction.commit()

    print "Historique topic %d" % (topic.id)

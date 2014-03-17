# -*- coding: utf-8 -*-

"""
Génère la base de données sqlite nécessaire pour explorer le corpus.
"""

import glob
import os.path
from gensim import corpora
from django.core import management
from django.core.management.base import BaseCommand
from api.models import Topic, Document, DocumentTopic
from django.db import transaction
from django.db.models import Sum


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
        calculate_topic_weights(topics)


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
            doc = Document.objects.create_document(raw_line.rstrip().split('\t'))
            doc.save()
            for id_topic, weight_in_document in lda[docno]:
                doc_topic = DocumentTopic(document=doc,
                        topic=topics[id_topic],
                        weight_in_document=weight_in_document)
                doc_topic.save()

            if docno % 1000 == 0:
                transaction.commit()

def calculate_topic_weights(topics):
    """
    Calcule pour chaque topic son poids total dans le corpus

    """

    transaction.set_autocommit(False)
    for topic in topics:
        result = DocumentTopic.objects.\
                filter(topic__id=topic.id).\
                aggregate(weight_in_corpus=Sum('weight_in_document'))

        topic.weight_in_corpus = result['weight_in_corpus']
        topic.save()

    transaction.commit()

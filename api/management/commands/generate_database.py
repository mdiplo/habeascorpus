# -*- coding: utf-8 -*-

"""
Génère la base de données sqlite nécessaire pour explorer le corpus.
"""

import glob
import os.path
import json
from api import utils
from gensim import corpora, similarities
from django.core import management
from django.core.management.base import BaseCommand
from api.models import Topic, Document, DocumentTopic, NeighbourGraphEdge
from django.db import transaction
from django.db.models import Sum, Min, Max


class Command(BaseCommand):
    arg = 'Nom du corpus'
    # help = 'Génère la base de données du corpus corpus_name' => problème unicode

    def handle(self, *args, **options):

        corpus_data_dir = os.getcwd()

        tsv_corpus = glob.glob(os.path.join(corpus_data_dir, '*.tsv'))
        lda_corpus = glob.glob(os.path.join(corpus_data_dir, '*_lda.mm'))
        topics = glob.glob(os.path.join(corpus_data_dir, '*_topics.txt'))
        docid = glob.glob(os.path.join(corpus_data_dir, '*_docid.txt'))

        if not tsv_corpus:
            raise IOError("""Impossible de trouver le fichier .tsv
            dans le dossier %s""" % (os.getcwd()))
        if not lda_corpus:
            raise IOError("""Impossible de trouver le fichier _lda.mm
            dans le dossier %s""" % (os.getcwd()))
        if not topics:
            raise IOError("""Impossible de trouver le fichier topics.txt
            dans le dossier %s""" % (os.getcwd()))
        if not docid:
            raise IOError("""Impossible de trouver le fichier topics.txt
            dans le dossier %s""" % (os.getcwd()))


        management.call_command('syncdb')
        topics = add_topics(topics[0])
        add_documents(tsv_corpus[0], lda_corpus[0], topics)
        for topic in topics:
            compute_topic_history(topic)
        find_neighbours(lda_corpus[0], docid[0])


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
        topics_from_file = eval(inp.read())  # topics_from_file = [[{'word': 'chine', weight_in_topic: 0.8},...], [...]]
        for t in topics_from_file:
            topic = Topic(related_words=t, weight_in_corpus=0)
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
        -`docid` : Un fichier de correspondance id diplo <-> id corpus

    """
    try:
        lda = corpora.mmcorpus.MmCorpus(lda_corpus_file)
    except:
        raise IOError("""Impossible de charger le fichier _lda.mm""")

    with open(raw_corpus_file, 'r') as raw:
        raw.readline()  # on ignore la première ligne qui contient les noms des colonnes
        transaction.set_autocommit(False)
        for docno, raw_line in enumerate(raw):
            # lda[docno] donne les topics associés au document raw_line sous la forme
            # d'une liste de tuples (id_topic, poids du topic id_topic dans le document docno)

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
    Calcule l'historique du topic sous la forme d'une liste
    [{'year': 1958, 'weight': 0.4 ...}, {...}] où weight est le poids du topic
    calculé sur tous les articles écrits pendant l'année year. 

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
            history.append({'date': year, 'weight': query['weight']})
            total_weight += query['weight']
        else:
            history.append({'date': year, 'weight': 0.0})

    topic.history = json.dumps(history, cls=utils.MyJsonEncoder)
    topic.weight_in_corpus = total_weight
    topic.save()
    transaction.commit()

    print "Historique topic %d" % (topic.id)


def find_neighbours(lda_corpus_file, docid_file):
    """
    Construit le graphe des documents qui indique pour chaque document les
    documents qui lui sont proches sémantiquement

    """

    try:
        lda_corpus = corpora.mmcorpus.MmCorpus(lda_corpus_file)
    except:
        raise IOError("""Impossible de charger le fichier _lda.mm""")

    transaction.set_autocommit(False)
    index = similarities.MatrixSimilarity(lda_corpus)

    for i, document in enumerate(Document.objects.all()):
        sims = index[lda_corpus[utils.get_article_by_id(document.id, docid_file)]]
        sims = sorted(enumerate(sims), key=lambda item: -item[1])

        for neighbour in sims[:10]:
            document2 = Document.objects.get(pk=utils.get_article_by_corpus_number(neighbour[0], docid_file))
            edge = NeighbourGraphEdge(document1=document, document2=document2, similarity=neighbour[1])
            edge.save()

        if i % 1000 == 0:
            transaction.commit()

        print "Voisins du document %d " % (i)

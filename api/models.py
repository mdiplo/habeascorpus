# -*- coding: utf-8 -*-
from datetime import datetime
from django.db import models

"""
Les différents modèles utilisés pour l'API :
    - Document : Un document du corpus, typiquement un article
    - Topic : Une liste de mots (typiquement 10 mots) affectés de poids
        ex: [{'mot': 'chine', 'poids': 2.3}, {'mot': 'mao', 'poids': 1.9},...]

"""


class Topic(models.Model):
    """
    Un topic du corpus.

    Attributs:
        - related_words : les mots représentatifs du Topic
        - weight_in_corpus : le poids total du Topic dans le corpus
        - history : l'historique du Topic, i.e la liste des poids dans le
            corpus pour chaque année

    """

    related_words = models.TextField()
    weight_in_corpus = models.FloatField()
    history = models.TextField()

    class Meta:
        db_table = 'topics'

    def get_related_words(self):
        """
        Renvoie les mots les plus représentatifs du Topic sous la forme d'une 
        liste de dictionnaires {'word' : ..., 'weight_in_topic' : ...}
        
        """
        
        return eval(self.related_words)

    def get_history(self):
        """
        Renvoie l'historique d'un Topic : pour chaque année, le poids du topic dans
        le corpus et les 3 articles les  plus représentatifs du Topic à cette date.

        """

        history = DocumentTopic.objects.filter(topic__id=self.id).\
                            values('document__date').\
                            extra(select={'key': "strftime('%Y', date)"}).\
                            values('key').\
                            annotate(value=models.Sum('weight_in_document')) 

        return history

class Document(models.Model):
    """
    Un document du corpus

    """

    titre = models.CharField(max_length=150)
    chapo = models.TextField()
    langue = models.CharField(max_length=2)
    auteur = models.CharField(max_length=30)
    mots = models.CharField(max_length=100)
    date = models.DateField(null=True)
    topics = models.ManyToManyField(Topic, through='DocumentTopic', related_name='documents')
    neighbours = models.ManyToManyField('self', through='NeighbourGraphEdge', related_name='documents', symmetrical=False)

    class Meta:
        db_table = 'documents'

    @classmethod
    def create_document(cls, l):
        """
        Créé un objet document en fournissant les propriétés du document
        dans une liste l

        """

        doc = Document()

        doc.id = int(l[0])
        doc.titre = l[1].decode('utf-8')
        doc.chapo = l[2].decode('utf-8')
        doc.texte = l[3].decode('utf-8')
        doc.langue = l[4].decode('utf-8')
        doc.auteur = l[5].decode('utf-8')
        doc.mots = l[6].decode('utf-8')
        try:
            doc.date = datetime.strptime(l[7].decode('utf-8'), '%Y-%m')
        except ValueError:
            doc.date = None
            #python n'accepte pas la date 0000-00

        return doc

    def get_neighbours(self):
        neighbours = NeighbourGraphEdge.objects.filter(document1__id=self.id)
        return [{'document': n.document2, 'similarity': n.similarity} for n in neighbours]


class DocumentTopic(models.Model):
    """
    Cette classe représente la relation many-to-many entre la classe Document
    et la classe Topic.

    Attributs:
        - document : Un Document du corpus
        - topic : Un Topic du corpus
        - weight_in_dcument : Le poids du Topic dans le Document
    """

    document = models.ForeignKey(Document)
    topic = models.ForeignKey(Topic)
    weight_in_document = models.FloatField()

    class Meta:
        db_table = "documents_topics"


class NeighbourGraphEdge(models.Model):
    """
    Cette classe représente la relation many-to-many entre des documents
    afin d'indiquer la proximité sémantique entre deux documents

    """

    document1 = models.ForeignKey(Document, related_name="document1")
    document2 = models.ForeignKey(Document, related_name="document2")
    similarity = models.FloatField()

    class Meta:
        db_table = "documents_graph"

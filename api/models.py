# -*- coding: utf-8 -*-
import json
from datetime import datetime
from django.db import models


class Topic(models.Model):
    """
    Un topic du corpus.
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
        
        words_tuples = map(eval, self.related_words.split('\t'))
        words_tuples = sorted(words_tuples, reverse=True)
        return [{'word': word, 'weight_in_topic': weight_in_topic}
                for (weight_in_topic, word) in words_tuples]

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


class DocumentManager(models.Manager):
    def create_document(self, l):
        """
        Créé un objet document en fournissant les propriétés du document
        dans une liste l

        """

        super(Document, self).__init__()
        self.id = int(l[0])
        self.titre = l[1].decode('utf-8')
        self.chapo = l[2].decode('utf-8')
        self.texte = l[3].decode('utf-8')
        self.langue = l[4].decode('utf-8')
        self.auteur = l[5].decode('utf-8')
        self.mots = l[6].decode('utf-8')
        try:
            self.date = datetime.strptime(l[7].decode('utf-8'), '%Y-%m')
        except ValueError:
            self.date = None
            #python n'accepte pas la date 0000-00

        
class DocumentTopic(models.Model):
    """
    Cette classe représente la relation many-to-many entre la classe Document 
    et la classe Topic. 
    """ 
    
    document = models.ForeignKey(Document)
    topic = models.ForeignKey(Topic)
    weight_in_document = models.FloatField()  # poids du topic dans le document

    class Meta:
        db_table = "documents_topics"

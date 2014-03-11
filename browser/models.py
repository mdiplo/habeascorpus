# -*- coding: utf-8 -*-
from django.db import models

class Topic(models.Model):
    """
    Un topic du corpus.
    """

    related_words = models.TextField()
    weight_in_corpus = models.FloatField()

    class Meta:
        db_table = 'topics'

class Document(models.Model):
    """
    Un document du corpus

    """

    titre = models.CharField(max_length=150)
    chapo = models.TextField()
    langue = models.CharField(max_length=2)
    auteur = models.CharField(max_length=30)
    mots = models.CharField(max_length=100)
    date = models.DateField()
    topics = models.ManyToManyField(Topic, through='DocumentTopic')

    class Meta:
        db_table = 'documents'

class DocumentTopic(models.Model):
    """
    Cette classe représente la relation many-to-many entre la classe Document 
    et la classe Topic. 
    """ 
    
    document = models.ForeignKey(Document)
    topic = models.ForeignKey(Topic)
    weight_in_document = models.FloatField() #poids du topic dans le document

    class Meta:
        db_table = "documents_topics"

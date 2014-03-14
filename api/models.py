# -*- coding: utf-8 -*-
from django.db import models

class Topic(models.Model):
    """
    Un topic du corpus.
    """

    related_words = models.TextField()
    weight_in_corpus = models.FloatField()

    def get_related_words(self):
        """
        Renvoie les mots les plus représentatifs du Topic sous la forme d'une 
        liste de dictionnaires {'word' : ..., 'weight_in_topic' : ...}
        
        """
        
        words_tuples = map(eval, self.related_words.split('\t'))
        words_tuples = sorted(words_tuples, reverse=True)
        return [{'word' : word, 'weight_in_topic' : weight_in_topic} 
                for (weight_in_topic, word) in words_tuples]


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
    topics = models.ManyToManyField(Topic, through='DocumentTopic', related_name='documents')

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

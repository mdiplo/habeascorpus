# -*- coding: utf-8 -*-

import json
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.sql import func
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from base import Base
import document

class Topic(Base):
    """
    Un topic du corpus.
    """
    
    __tablename__ = 'topics'
    
    id = Column(Integer, primary_key = True)
    related_words = Column(String)
    weight_in_corpus = Column(Float)
    
    def get_related_words(self, n=None):
        """
        Renvoie les n mots les plus représentatifs du Topic sous la forme d'une 
        liste de dictionnaires {'word' : ..., 'weight_in_topic' : ...}
        
        """
        
        words_tuples = map(eval, self.related_words.split('\t'))
        words_tuples = sorted(words_tuples, reverse=True)
        return [{'word' : word, 'weight_in_topic' : weight_in_topic} 
                for (weight_in_topic, word) in words_tuples[:n]]
        
    def set_weight_in_corpus(self, session):
        """
        Calcule le poids total du topic dans le corpus. Pour le topic n°i, ce poids
        total s'obtient en sommant la i-ème composante de tous les vecteurs LDA 
        représentant un document.
        
        """
        
        query = session.query(func.sum(document.DocumentTopic.weight_in_document)).\
                        join(Topic).\
                        filter(Topic.id == self.id)
                                                            
        self.weight_in_corpus = query.scalar()
        session.commit()
        
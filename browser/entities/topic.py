# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String
from base import Base

class Topic(Base):
    """
    Un topic du corpus.
    """
    
    __tablename__ = 'topics'
    
    id = Column(Integer, primary_key = True)
    related_words = Column(String)
    
    def get_related_words(self):
        """
        Renvoie les mots associés au Topic sous la forme d'une liste de dictionnaires
        {'word' : ..., 'topic_score' : ...}
        """
        
        words_tuples = map(eval, self.related_words.split('\t'))
        return [{'word' : word, 'topic_score' : topic_score} 
                for (topic_score, word) in words_tuples]
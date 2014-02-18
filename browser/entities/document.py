# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
import sys, os.path

entities = os.path.dirname(os.path.realpath(__file__))
sys.path.append(entities)

import topic

class Document(topic.Base):
    """
    Un document du corpus.
    """
    
    __tablename__ = 'documents'
    
    id = Column(Integer, primary_key = True)
    titre = Column(String)
    chapo = Column(String)
    texte = Column(String)
    langue = Column(String) 
    auteur = Column(String)
    mots = Column(String)
    topics = relationship("DocumentTopic", order_by="-DocumentTopic.score", backref="documents")
    #date = Column(DateTime)
    
    def __init__(self, l):
        self.id = int(l[0])
        self.titre = l[1].decode('utf-8')
        self.chapo = l[2].decode('utf-8')
        self.texte = l[3].decode('utf-8')
        self.langue = l[4].decode('utf-8')
        self.auteur = l[5].decode('utf-8')
        self.mots = l[6].decode('utf-8')
        #self.date = l[7]
        
class DocumentTopic(topic.Base):
    """
    Cette classe représente la relation many-to-many entre la classe Document 
    et la classe Topic. 
    """
    
    __tablename__ = 'documents_topics'   
    
    document_id = Column(Integer, ForeignKey('documents.id'), primary_key=True)
    topic_id = Column(Integer, ForeignKey('topics.id'), primary_key=True)
    score = Column(Integer) #valeur de topic_id pour le document document_id
    topic = relationship("Topic")
    
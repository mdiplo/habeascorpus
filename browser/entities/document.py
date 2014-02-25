# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, Date, Float
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from datetime import datetime
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
    date = Column(Date)
    topics = relationship("DocumentTopic", order_by="-DocumentTopic.weight_in_document",
                           backref="documents")
    
    def __init__(self, l):
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
            self.date = datetime(1, 1, 1)
            #python n'accepte pas la date 0000-00, on la remplace par 0000-01
            
class DocumentTopic(topic.Base):
    """
    Cette classe représente la relation many-to-many entre la classe Document 
    et la classe Topic. 
    """
    
    __tablename__ = 'documents_topics'   
    
    document_id = Column(Integer, ForeignKey('documents.id'), primary_key=True)
    topic_id = Column(Integer, ForeignKey('topics.id'), primary_key=True)
    weight_in_document = Column(Float) #poids du topic dans le document
    topic = relationship("Topic")
    
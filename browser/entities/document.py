# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, DateTime
from base import Base

class Document(Base):
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
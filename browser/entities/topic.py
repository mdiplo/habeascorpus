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
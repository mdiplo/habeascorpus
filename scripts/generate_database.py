# -*- coding: utf-8 -*-

"""
Génère la base de données sqlite nécessaire pour explorer le corpus.
"""

import argparse
import glob
import os.path
import sys
import logging
from gensim import corpora, similarities
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import utils

# Les arguments à fournir en ligne de commande
parser = argparse.ArgumentParser(description="""Génère la base de données sqlite nécessaire pour explorer le corpus.""")
parser.add_argument('corpus_name', type=str,
                    help="Le nom du corpus (i.e le nom du fichier sans l'extension .tsv)")
parser.add_argument('-v', '--verbose', action='store_true',
                    help="Afficher les messages d'information")
args = parser.parse_args()

corpus_file = args.corpus_name + '.tsv'

engine = create_engine('sqlite:///%s.db' % (args.corpus_name), echo=True)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Topic(Base):

    __tablename__ = 'topics'
    
    id = Column(Integer, primary_key=True)
    related_words = Column(String)
    #weight_in_corpus = Column(Float)
    
class Article(Base):

    __tablename__ = 'articles'
    
    id = Column(Integer, primary_key=True)
    
    def __init__(self, raw_line):
        id, title, chapo, text, lang, authors, keywords, date = raw_line.rstrip('\n').split('\t') 
        self.id = id
    
Base.metadata.create_all(engine)

# Ajout des articles
with open(args.corpus_name + '.tsv') as f:
    
    f.readline()  # on passe la première ligne qui contient l'entête
    
    for i, raw_line in enumerate(f):
        doc = Article(raw_line)
        session.add(doc)
        
        if i% 10 == 0 and args.verbose:
            print "Ajout de l'article n° %d" % (i)
        
        if i % 1000 == 0:
            session.commit()

# Ajout des topics
# On créé une table pour chaque modèle de topics (lda50, lda100,...)

def add_topics(model_file, session):
    topics_file = model_file.rstrip('_model') + '_topics'
    
    with open(topics_file) as f:
        topics = eval(f.read())
        session.add_all([Topic(related_words = str(topic)) for topic in topics])
    session.commit()

for method in glob.glob('*lda[0-9]*_model')

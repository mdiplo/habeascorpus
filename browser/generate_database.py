# -*- coding: utf-8 -*-

"""
Génère la base de données sqlite nécessaire pour explorer le corpus.
"""

import argparse
import glob
import os.path
import sys
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from gensim import corpora

root_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(root_dir) #TODO : faire fonctionner les import relatif (from .. import utils)
entities_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'entities')
sys.path.append(entities_dir)

import utils
from base import Base  # @UnresolvedImport
from document import Document, DocumentTopic  # @UnresolvedImport
from topic import Topic  # @UnresolvedImport

def add_topics(topics_file, session):
    """
    Ajoute les topics dans la table topics à partir du fichier topics.txt généré
    par lda.py
    
    :Parameters:
        -`topics_file`: Le fichier topics.txt contenant les topics
        -`session`: L'objet Sonnexion de sqlalchemy
        
    :return:
        La liste l telle que l[i] = Topic(id = i+1)
    
    """
    
    topics = []
    
    with open(topics_file, 'r') as inp:
        for line in inp:
            topic = Topic(related_words = line)
            session.add(topic)
            topics.append(topic)
        session.commit()
        
    return topics

def add_documents(raw_corpus_file, lda_corpus_file, topics, session):
    """
    Ajoute dans la table documents les articles d'un fichier .tsv contenant 8 colonnes :
        - id_article
        - titre
        - chapo
        - texte
        - langue
        - auteur
        - mots
        - date
        
    Ajoute également les topics liés à chaque document.
        
    :Parameters:
        -`raw_corpus_file`: Le fichier .tsv contenant les documents
        -`lda_corpus_file`: Le fichier _lda.mm 
        -`topics` : Une liste l contenant tous les topics telle que l[i] = Topic(id = i+1)
        -`session`: L'objet Session de sqlalchemy'

    """
    try:
        lda = corpora.mmcorpus.MmCorpus(lda_corpus_file)
    except:
        raise IOError("""Impossible de trouver le fichier _lda.mm
        dans le dossier %s""" % (os.getcwd()))
        
    with open(raw_corpus_file, 'r') as raw:
        raw.readline() #on ignore la première ligne qui contient les noms des colonnes
        for docno, raw_line in enumerate(raw):
            #lda[docno] donne les topics associés au document raw_line sous la forme
            #d'une liste de tuples (id_topic, score)  
            
            doc = Document(raw_line.split('\t'))
            for id_topic, score in lda[docno]:
                doc_topic = DocumentTopic(score=score)
                doc_topic.topic = topics[id_topic - 1]
                doc.topics.append(doc_topic)
            session.add(doc)
            
        session.commit()
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="""Génère la base de données sqlite 
    d'exploration d'un corpus.""");
    parser.add_argument('-v', '--verbose', action='store_true',
                    help="Afficher les messages d'information")
    arg = parser.parse_args()
    
    if arg.verbose:
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    
    tsv_corpus = glob.glob('*.tsv')
    lda_corpus = glob.glob('*_lda.mm')
    topics = glob.glob('*_topics.txt')
    
    if not tsv_corpus:
        raise IOError("""Impossible de trouver le fichier .tsv
        dans le dossier %s""" % (os.getcwd()))
    if not lda_corpus:
        raise IOError("""Impossible de trouver le fichier _lda.mm
        dans le dossier %s""" % (os.getcwd()))
    if not topics:
        raise IOError("""Impossible de trouver le fichier topics.txt 
        dans le dossier %s""" % (os.getcwd()))
        
    corpus_name = os.path.splitext(tsv_corpus[0])[0]
    
    engine = create_engine('sqlite:///%s.db' % (corpus_name), echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    Base.metadata.create_all(engine)
    
    #On ajoute les topics à la base, et on les récupère dans la variable topics
    topics = add_topics(topics[0], session)
    
    add_documents(tsv_corpus[0], lda_corpus[0], topics, session)
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

root_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(root_dir) #TODO : faire fonctionner les import relatif (from .. import utils)
entities_dir = os.path.dirname(os.path.realpath(__file__)) + '/entities'
sys.path.append(entities_dir)

import utils
from base import Base  # @UnresolvedImport
from document import Document  # @UnresolvedImport
from topic import Topic  # @UnresolvedImport

def add_documents(corpus_file, session):
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
        
    :Parameters:
        -`corpus_file`: Le fichier .tsv contenant les documents
        -`session`: L'objet Session de sqlalchemy'

    """

    with open(corpus_file, 'r') as inp:
        inp.readline()
        for raw_line in inp:
            session.add(Document(raw_line.split('\t')))
        session.commit()
    
        
def add_topics(topics_file, session):
    """
    Ajoute les topics dans la table topics à partir du fichier topics.txt généré
    par lda.py
    
    :Parameters:
        -`topics_file`: Le fichier topics.txt contenant les topics
        -`session`: L'objet Sonnexion de sqlalchemy
    
    """
    
    with open(topics_file, 'r') as inp:
        for line in inp:
            session.add(Topic(related_words = line))
        session.commit()
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="""Génère la base de données sqlite 
    d'exploration d'un corpus""");
    parser.add_argument('data_path', type=str, help="""Le dossier contenant les
     données calculées sur le corpus. Ce dossier doit contenir :
         - le corpus au format .tsv
         - le fichier topics.txt généré par lda.py""")
    parser.add_argument('-v', '--verbose', action='store_true',
                    help="Afficher les messages d'information")
    arg = parser.parse_args()
    
    if arg.verbose:
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    
    tsv_corpus = glob.glob(arg.data_path + '/*.tsv')
    topics = glob.glob(arg.data_path + '/*_topics.txt')
    
    if not tsv_corpus:
        raise IOError("""Impossible de trouver le fichier .tsv
        dans le dossier %s""" % (arg.data_path))
    if not topics:
        raise IOError("""Impossible de trouver le fichier topics.txt 
        dans le dossier %s""" % (arg.data_path))

    corpus_name = utils.split_path(tsv_corpus[0])['name']
    
    engine = create_engine('sqlite:///%s.db' % (corpus_name), echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    Base.metadata.create_all(engine)
    
    add_topics(topics[0], session)
    add_documents(tsv_corpus[0], session)
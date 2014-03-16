# -*- coding: utf-8 -*-

"""
Génère la base de données sqlite nécessaire pour explorer le corpus.
"""

import argparse
import glob
import os.path
import sys
import logging
from gensim import corpora

root_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(root_dir)  #TODO : faire fonctionner les import relatif (from .. import utils)
entities_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'entities')
sys.path.append(entities_dir)

import utils
from api.models import Topic, Document 

def add_topics(topics_file, session):
    """
    Ajoute les topics dans la table topics à partir du fichier topics.txt généré
    par lda.py
    
    :Parameters:
        -`topics_file`: Le fichier topics.txt contenant les topics
        
    """

    with open(topics_file, 'r') as inp:
        for i, line in enumerate(inp):
            Topic.create(related_words = line)

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
        -`topics` : Une liste l contenant tous les topics telle que l[i] = Topic(id = i)
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
            #d'une liste de tuples (id_topic, poids du topic id_topic dans le document docno)  
            
            doc = Document(raw_line.rstrip().split('\t'))
            for id_topic, weight_in_document in lda[docno]:
                doc_topic = DocumentTopic(weight_in_document=weight_in_document)
                doc_topic.topic = topics[id_topic]
                doc.topics.append(doc_topic)
            session.add(doc)

            if docno % 500 == 0:
                session.commit()

        session.commit()
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="""Génère la base de données sqlite 
    d'exploration d'un corpus.""");
    parser.add_argument('-v', '--verbose', action='store_true',
                    help="Afficher les messages d'information")
    args = parser.parse_args()
    
    if args.verbose:
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
    
    #On ajoute les topics à la base, et on les récupère dans la variable topics
    add_topics(topics[0])
    
    #add_documents(tsv_corpus[0], lda_corpus[0], topics, session)
    #
    ##On calcule pour chaque topic son poids total dans le corpus
    #for topic in topics:
    #    topic.set_weight_in_corpus(session)

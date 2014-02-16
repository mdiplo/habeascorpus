# -*- coding: utf-8 -*-

"""
Génère la base de données sqlite nécessaire pour explorer le corpus.
"""

import argparse
import sqlite3
import glob
import os.path
import sys

root_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(root_dir) #TODO : faire fonctionner les import relatif (from .. import utils)

import utils

def create_documents_table(corpus_file, conn):
    """
    Génère la table documents à partir d'un fichier .tsv contenant 8 colonnes :
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
        -`conn`: L'objet Connexion à la base sqlite'

    """
    
    c = conn.cursor()
    c.execute("""CREATE TABLE document
    (id_ INTEGER PRIMARY KEY, titre TEXT, chapo TEXT, texte TEXT, langue TEXT, 
    auteur TEXT, mots TEXT, date NUMERIC)""")
    conn.commit()
    
    with open(corpus_file, 'r') as inp:
        inp.readline()
        insert_query = """INSERT INTO document VALUES(?, ?, ?, ?, ?, ?, ?, ?)"""
        for raw_line in inp:
                c.execute(insert_query, raw_line.split('\t'))
        conn.commit()
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="""Génère la base de données sqlite 
    d'exploration d'un corpus""");
    parser.add_argument('data_path', type=str, help="""Le dossier contenant les
     données calculées sur le corpus. Ce dossier doit contenir :
         - le corpus au format .tsv
         - le fichier topics.txt généré par lda.py""")
    arg = parser.parse_args()
    
    tsv_corpus = glob.glob(arg.data_path + '/*.tsv')
    topics = glob.glob(arg.data_path + '/*_topics.txt')
    
    if not tsv_corpus:
        raise IOError("""Impossible de trouver le fichier .tsv
        dans le dossier %s""" % (arg.data_path))
    if not topics:
        raise IOError("""Impossible de trouver le fichier topics.txt 
        dans le dossier %s""" % (arg.data_path))

    corpus_name = utils.split_path(tsv_corpus[0])['name']
    conn = sqlite3.connect(corpus_name + '.db') 
    conn.text_factory = str
    
    create_documents_table(tsv_corpus[0], conn)
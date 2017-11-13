# -*- coding: utf-8 -*-

"""
Ce script prend en entrée un corpus de référence et un corpus "étranger", 
puis recherche pour chaque article du corpus étranger s'il possède une traduction
dans le corpus de référence.
Les résultats sont enregistrés dans un fichier.

"""

"""
Google has updated its translation service recently with a ticket mechanism to prevent simple crawler program like goslate from accessing. Though a more sophisticated crawler may still work technically, however it would have crossed the fine line between using the service and breaking the service. goslate will not be updated to break google’s ticket mechanism. Free lunch is over. Thanks for using.
https://pypi.python.org/pypi/goslate
"""

import sys
import os
import string
import argparse
import logging
import numpy
import goslate
from gensim import corpora, similarities, models

import utils
    

def find_translation(text, corpus_name, index, dico, corpus, tfidfmodel):

    docid_path = corpus_name + '_docid.txt'

    gs = goslate.Goslate(timeout=100)
    
    # On traduit en français le texte fourni par l'utilisateur
    # Utilise l'API google qui détexte automatiquement le langage 
    try:
        translated_text = gs.translate(text, 'fr')
    except Exception:
        translated_text = text
       
    # On tokenize le texte fourni grâce au dictionnaire 
    vec_bow = dico.doc2bow(utils.tokenize(translated_text))
    
    # On applique la transformation tfidf 
    vec_tfidf = tfidfmodel[vec_bow]

    # On renvoie le plus proche voisin de la traduction dans le corpus
    sims = index[vec_tfidf]
    sims = sorted(enumerate(sims), key=lambda item: -item[1])
    return (utils.get_article_by_corpus_number(sims[0][0], docid_path), sims[0][1])
   
    
if __name__ == '__main__':

    print ("no more free lunch. https://pypi.python.org/pypi/goslate")
    return

    # Les arguments à fournir en ligne de commande
    parser = argparse.ArgumentParser(description="""Vérifie si le texte en entrée standard possède une traduction dans le corpus""")
    parser.add_argument('corpus_fr', type=str, help='Le nom du corpus')
    parser.add_argument('corpus_etranger', type=str, help='Le nom du corpus')
    parser.add_argument('translate_file', type=str, help='Le nom du corpus')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help="Afficher les messages d'information")
    args = parser.parse_args()

    # L'option -v affiche les messages d'information
    if args.verbose:
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
        
    index_file = args.corpus_fr + '_tfidf_index'
    dic_path = args.corpus_fr + '_wordids.txt'
    corpus_path = args.corpus_fr + '_tfidf.mm'
    corpus_etranger = args.corpus_etranger + '.tsv'
    tfidfmodel_path = args.corpus_fr + '_tfidf_model'
    
    # Chargement du corpus  
    try:
        corpus = corpora.mmcorpus.MmCorpus(corpus_path)
    except Exception:
        raise IOError("""Impossible de charger le fichier %s. Avez-vous bien appliqué le script corpus_to_matrix.py ?""" % (corpus_path))
    
    # Chargement du fichier d'index
    try:
        index = similarities.docsim.Similarity.load(index_file)
    except Exception:
        raise IOError("""Impossible de charger le fichier %s. Avez-vous bien appliqué le script tfidf.py avec l'option --saveindex ?""" % (index_file))
        
    # Chargement du dictionnaire
    try:
        dico = corpora.Dictionary.load_from_text(dic_path)
    except Exception:
        raise IOError('Impossible de charger le fichier %s' % (dic_path))
     
    # Chargement du modèle   
    try:
        tfidfmodel = models.tfidfmodel.TfidfModel.load(tfidfmodel_path)
    except Exception:
        raise IOError("""Impossible de charger le fichier %s. Avez-vous bien appliqué le script tfidf ?""" % (tfidfmodel_path))
        
    f = open(corpus_etranger)
    o = open(args.translate_file, 'w')
        
    for i, l in enumerate(f):
    
        # Pour chaque document, on récupère la traduction supposée et le score de proximité
        doc = utils.Document(l)
        trad, score = find_translation(doc.text, args.corpus_fr, index, dico, corpus, tfidfmodel)
        
        # Si le score est supérieur à 0.4, la traduction a de très fortes chances d'être la bonne
        if score >= 0.4:
            o.write(str(doc.id) + '\t' + str(trad) + '\n')
        
        # Si le score est compris entre 0.35 et 0.4, la traduction supposée est peut-être inexacte
        elif score >= 0.35 and score < 0.4:
            o.write(str(doc.id) + '\t' + str(trad) + '?\n')
        
        # En dessous de 0.35, le texte ne possède probablement pas de traduction dans le 
        # corpus de référence
        else:
            o.write(str(doc.id) + '\t?\n')
        
        if args.verbose:
            print "Document %d traité" % (i)

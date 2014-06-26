# -*- coding: utf-8 -*-
"""
À partir d'un corpus au format bag-of-words sous forme d'un fichier Matrix Market (.mm)
et du dictionnaire associé, ce script applique l'algorithme LDA et génère :

    - nom_du_corpus_lda_nbtopics.mm : La représentation matricielle du corpus une fois appliqué
    l'algorithme LDA à chaque document

"""

import logging
import os
import argparse
import glob
import json
from gensim import corpora, models, similarities

# Les arguments à fournir en ligne de commande
parser = argparse.ArgumentParser(description="""Applique l'algorithme LDA sur un corpus""")
parser.add_argument('corpus_name', type=str,
                    help="Le nom du corpus (i.e le nom du fichier sans l'extension .tsv)")
parser.add_argument('nb_topics', type=int,
                    help="Le nombre de topics voulus")
parser.add_argument('--nb_passes', type=int, default=3,
                    help="""Le nombre de passes effectuées par l'algorithme.
                    Par défaut : 3""")
parser.add_argument('--saveindex', action='store_true',
                    help="Si vrai, le script enregistre l'index de similarité pour le corpus")
parser.add_argument('--savetopics', action='store_true',
                    help="Si vrai, le script enregistre les topics trouvés")
parser.add_argument('-v', '--verbose', action='store_true',
                    help="Afficher les messages d'information")
args = parser.parse_args()

# L'option -v affiche les messages d'information
if args.verbose:
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
      
corpus_file = args.corpus_name + '_bow.mm'
dictionary_file = args.corpus_name + '_wordids.txt'

# Chargement du corpus
try:
    corpus = corpora.mmcorpus.MmCorpus(corpus_file)
except Exception:
    raise IOError("""Impossible d'ouvrir le fichier %s. Avez-vous bien appliqué le script corpus_to_matrix.py ?""" % corpus_file)

# Chargement du dictionnaire
try:
    id2word = corpora.dictionary.Dictionary.load_from_text(dictionary_file)
except Exception:
    raise IOError("""Impossible d'ouvrir le fichier %s""" % dictionary_file)

# Application de l'algorithme LDA
lda = models.ldamodel.LdaModel(corpus=corpus, id2word=id2word, num_topics=args.nb_topics, passes=args.nb_passes)

# Enregistrement du modèle
lda.save(args.corpus_name + '_lda'  + str(args.nb_topics) + '_model')

# Enregistrement du corpus LDA-ifié
corpora.mmcorpus.MmCorpus.serialize(args.corpus_name + '_lda' + str(args.nb_topics) + '.mm', lda[corpus], progress_cnt=1000)

# L'option --saveindex enregistre un fichier d'index qui permet de faire de la
# recherche de similarité entre les articles
if args.saveindex:
    corpus = corpora.mmcorpus.MmCorpus(args.corpus_name + '_lda' + str(args.nb_topics) + '.mm')
    index = similarities.docsim.Similarity(os.path.join(os.getcwd(), args.corpus_name + '_lda' + str(args.nb_topics) + '_index'), corpus, num_features=corpus.num_terms)
    index.save(args.corpus_name + '_lda' + str(args.nb_topics) + '_index')

# L'option --savetopics enregistre dans un fichier les topics trouvés par l'algorithme
if args.savetopics:
    with open(args.corpus_name + '_topics.txt', 'w') as f:
        topics = [[{'word': x[1], 'weight_in_topic': x[0]} for x in lda.show_topic(i)] for i in range(args.nb_topics)]
        f.write(json.dumps(topics))

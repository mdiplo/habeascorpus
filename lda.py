# -*- coding: utf-8 -*-
"""
À partir d'un corpus au format bag-of-words sous forme d'un fichier Matrix Market (.mm) 
et du dictionnaire associé, ce script applique l'algorithme LDA et génère deux fichiers :
    
    - nom_du_corpus_lda.mm : La représentation matricielle du corpus une fois appliqué
    l'algorithme LDA à chaque document
    
    - nom_du_corpus_topics.txt : Les topics trouvés par l'algorithme
"""

import logging  
import os
import argparse
import re
    
import utils
from gensim import corpora, models

parser = argparse.ArgumentParser(description="""Applique l'algorithme LDA sur un corpus""");
parser.add_argument('nb_topics', type=int, 
                    help="Le nombre de topics voulus")
parser.add_argument('--nb_passes', type=int, default=3,
                    help="""Le nombre de passes effectuées par l'algorithme. 
                    Par défaut : 3""")
parser.add_argument('corpus_path', type=str,
                    help= """Le fichier bow.mm représentant le corpus sous forme bag-of-words.
                    Ce fichier est généré par le script corpus_to_matrix.py""")
parser.add_argument('dictionary_path', type=str,
                    help="""Le fichier wordids.txt indiquant un id pour chaque mot du
                    corpus. Ce fichier est généré par le script corpus_to_matrix.py""")
parser.add_argument('-v', '--verbose', action='store_true',
                    help="Afficher les messages d'information")
args = parser.parse_args()

if args.verbose:
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

corpus_name = re.split(r'_bow', utils.split_path(args.corpus_path)['name'])[0]

if os.path.isfile(corpus_name + '_lda.mm'):
    raise IOError("Le corpus LDA existe déjà sous forme matricielle")

try:
    corpus = corpora.mmcorpus.MmCorpus(args.corpus_path)
except Exception:
    raise IOError("""Impossible d'ouvrir le corpus. 
    Vérifiez que le fichier %s existe bien""" % (args.corpus_path))

try:    
    id2word = corpora.dictionary.Dictionary.load_from_text(args.dictionary_path)
except Exception:
    raise IOError("""Impossible d'ouvrir le dictionnaire.
    Vérifiez que le fichier %s existe bien""" % (args.dictionary_path))

lda = models.ldamodel.LdaModel(corpus=corpus,id2word=id2word,
                                       num_topics=args.nb_topics, passes=args.nb_passes) 
lda.save(corpus_name + '_ldamodel')
corpora.mmcorpus.MmCorpus.serialize(corpus_name + '_lda.mm', lda[corpus], progress_cnt=1000)

with open(corpus_name + '_topics.txt', 'w') as f:
    for i in range(args.nb_topics):
        f.write('\t'.join(str(x) for x in lda.show_topic(i)) + '\n')
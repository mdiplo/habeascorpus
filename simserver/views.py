# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from gensim import corpora, similarities, models

#Peut-on le faire avec des imports relatifs ?
import sys
import os.path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(os.path.join(root_path, 'scripts'))

import similar_articles

data_path = os.path.join(os.path.join(root_path, 'data'), 'diplo_juillet2')
corpus_name = 'articles_fr'
method = 'tfidf'

corpus_file = os.path.join(data_path, corpus_name + '_' + method + '.mm')
index_file = os.path.join(data_path, corpus_name + '_' + method + '_index')
dico_file = os.path.join(data_path, corpus_name + '_wordids.txt')

try:
    corpus = corpora.mmcorpus.MmCorpus(corpus_file)
except Exception:
    raise IOError('Impossible de charger le fichier %s. Avez-vous bien appliqué le script corpus_to_matrix.py ?' % (corpus_file))
            
try:
    index = similarities.docsim.Similarity.load(index_file)
    print index_file
except Exception:
    raise IOError("""Impossible de charger le fichier %s. Avez-vous bien appliqué le script %s avec l'option --saveindex ?""" % (method, index_file))

try:
    id2word = corpora.dictionary.Dictionary.load_from_text(dico_file)
except Exception:
    raise IOError("Impossible de charger le fichier %s" % (dico_file))
    
if method == 'tfidf':
    model_file = os.path.join(data_path, corpus_name + '_tfidf_model')
    model = models.tfidfmodel.TfidfModel.load(model_file)

elif method.startswith('lsi'):
    model_file = os.path.join(data_path, corpus_name + '_' + method + '_model')
    model = models.lsimodel.LsiModel.load(model_file)

elif method.startswith('lda'):
    model_file = os.path.join(data_path, corpus_name + '_' + method + '_model')
    model = models.ldamodel.LdaModel.load(model_file)

@csrf_exempt
def diploisation(request):
    return HttpResponse(similar_articles.find_similar_articles('articles_fr', 'tfidf', content=request.POST['texte'], data_dir=data_path, index=index, id2word=id2word, corpus=corpus, model=model))

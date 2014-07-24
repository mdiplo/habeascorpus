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
import utils
from habeascorpus import settings

tsv_file = os.path.join(settings.DATA_DIR, settings.CORPUS_NAME + '.tsv')
corpus_file = os.path.join(settings.DATA_DIR, settings.CORPUS_NAME + '_' + settings.METHOD + '.mm')
index_file = os.path.join(settings.DATA_DIR, settings.CORPUS_NAME + '_' + settings.METHOD + '_index')
dico_file = os.path.join(settings.DATA_DIR, settings.CORPUS_NAME + '_wordids.txt')

try:
    corpus = corpora.mmcorpus.MmCorpus(corpus_file)
except Exception:
    raise IOError('Impossible de charger le fichier %s. Avez-vous bien appliqué le script corpus_to_matrix.py ?' % (corpus_file))
            
try:
    index = similarities.docsim.Similarity.load(index_file)
    print index_file
except Exception:
    raise IOError("""Impossible de charger le fichier %s. Avez-vous bien appliqué le script %s avec l'option --saveindex ?""" % (settings.METHOD, index_file))

try:
    id2word = corpora.dictionary.Dictionary.load_from_text(dico_file)
except Exception:
    raise IOError("Impossible de charger le fichier %s" % (dico_file))
    
if settings.METHOD == 'tfidf':
    model_file = os.path.join(settings.DATA_DIR, settings.CORPUS_NAME + '_tfidf_model')
    model = models.tfidfmodel.TfidfModel.load(model_file)

elif settings.METHOD.startswith('lsi'):
    model_file = os.path.join(settings.DATA_DIR, settings.CORPUS_NAME + '_' + settings.METHOD + '_model')
    model = models.lsimodel.LsiModel.load(model_file)

elif settings.METHOD.startswith('lda'):
    model_file = os.path.join(settings.DATA_DIR, settings.CORPUS_NAME + '_' + settings.METHOD + '_model')
    model = models.ldamodel.LdaModel.load(model_file)
    
# Construction d'un tableau contenant pour chaque article son titre, l'auteur, les mots-clefs
metadonnees = {}
with open(tsv_file) as f:
    for l in f:
        doc = utils.Document(l)
        metadonnees[doc.id] = {'titre' : doc.title, 'auteurs': doc.authors, 'date': doc.date}

@csrf_exempt
def diploisation(request):
    
    #nb d'articles proches voulu
    if request.POST.has_key('nb_articles'):
        if int(request.POST['nb_articles']) < 0:
            raise ValueError("Le nombre d'articles proches doit être > 0")
        nb_articles = min(int(request.POST['nb_articles']), settings.MAX_ARTICLES)
    else:
        nb_articles = 5
        
    neighbours = similar_articles.find_similar_articles(settings.CORPUS_NAME, settings.METHOD, n=nb_articles, content=request.POST['texte'], data_dir=settings.DATA_DIR, index=index, id2word=id2word, corpus=corpus, model=model)
    
    result = []
    for article in neighbours:
        result.append(dict(metadonnees[str(article['id'])].items() + article.items()))
    return HttpResponse(json.dumps(result))

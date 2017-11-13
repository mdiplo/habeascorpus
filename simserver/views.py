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
corpus_file = os.path.join(settings.MODELS_DIR, settings.CORPUS_NAME + '_' + settings.METHOD + '.mm')
index_file = os.path.join(settings.MODELS_DIR, settings.CORPUS_NAME + '_' + settings.METHOD + '_index')
dico_file = os.path.join(settings.MODELS_DIR, settings.CORPUS_NAME + '_wordids.txt')


print('settings.CORPUS_NAME', settings.CORPUS_NAME)

try:
    corpus = corpora.mmcorpus.MmCorpus(corpus_file)
except Exception:
    raise IOError('Impossible de charger le fichier %s. Avez-vous bien appliqué le script corpus_to_matrix.py ?' % (corpus_file))
            
try:
    index = similarities.docsim.Similarity.load(index_file)
    print (index_file)
except Exception:
    raise IOError("""Impossible de charger le fichier %s. Avez-vous bien appliqué le script %s avec l'option --saveindex ?""" % (settings.METHOD, index_file))

try:
    id2word = corpora.dictionary.Dictionary.load_from_text(dico_file)
except Exception:
    raise IOError("Impossible de charger le fichier %s" % (dico_file))

# Construction d'un tableau contenant pour chaque article son titre, l'auteur, les mots-clefs
metadonnees = {}
with open(tsv_file) as f:
    for l in f:
        doc = utils.Document(l)
        metadonnees[doc.id] = {'titre' : doc.title, 'auteurs': doc.authors, 'date': doc.date, 'mots': list(doc.keywords), 'url_site': doc.url_site }

@csrf_exempt
def diploisation(request):

    texte = ''
    if 'texte' in request.GET:
        texte = request.GET['texte']
    elif 'texte' in request.POST:
        texte = request.POST['texte']

    # rien poste: home page
    if texte == '':
        return HttpResponse(homepage())

    #nb d'articles proches voulu
    nb_articles = 5
    if 'nb_articles' in request.POST:
        nb_articles = request.POST['nb_articles']
    if 'nb_articles' in request.GET:
        nb_articles = request.GET['nb_articles']
    nb_articles = max(0, min(int(nb_articles), settings.MAX_ARTICLES))
    
    # choix de la méthode parmi celles définies dans habeascorpus.settings
    method = settings.METHOD
    if 'method' in request.GET and request.GET['method'] in settings.METHODS:
        method = settings.METHODS[request.GET['method']]
    if 'method' in request.POST and request.POST['method'] in settings.METHODS:
        method = settings.METHODS[request.POST['method']]
    if method == 'tfidf':
        model_file = os.path.join(settings.MODELS_DIR, settings.CORPUS_NAME + '_tfidf_model')
        model = models.tfidfmodel.TfidfModel.load(model_file)
    elif method.startswith('lsi'):
        model_file = os.path.join(settings.MODELS_DIR, settings.CORPUS_NAME + '_' + method + '_model')
        model = models.lsimodel.LsiModel.load(model_file)
    elif method.startswith('lda'):
        model_file = os.path.join(settings.MODELS_DIR, settings.CORPUS_NAME + '_' + method + '_model')
        model = models.ldamodel.LdaModel.load(model_file)
    
    neighbours = similar_articles.find_similar_articles(settings.CORPUS_NAME, method, n=nb_articles, content=texte, data_dir=settings.MODELS_DIR, index=index, id2word=id2word, corpus=corpus, model=model)

    result = { 'method': method, 'articles': [] }
    for article in neighbours:
        meta = metadonnees[str(article['id'])]
        meta['id'] = str(article['id'])
        meta['score'] = 0 + article['score'] # converts np to float
        result['articles'].append(meta)
    print ('post:', texte)
    print ('result:', result)
    return HttpResponse(json.dumps(result), content_type="application/json")


def homepage():
    return u'Bookmarklet: <a href="javascript:var%20titre=document.title;var%20txt=\'\';if(window.getSelection){txt=window.getSelection();}else%20if(document.getSelection){txt=document.getSelection();}else%20if(document.selection){txt=document.selection.createRange().text;}var%20url=document.location;void(btw=window.open(\'http://archives.mondediplo.com?page=diploiser#titre=\'+(encodeURIComponent(titre))+encodeURI(\'\\r\')+escape(url)+encodeURI(\'\\r\\r\')+\'&texte=\'+(encodeURIComponent(txt))))">+diploiser</a>'




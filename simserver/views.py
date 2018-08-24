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

tsv_file={}
corpus_file={}
index_file={}
dico_file={}
corpus={}
index={}
metadonnees={}
id2word={}

for lang in settings.LANGS:
    tsv_file[lang] = os.path.join(settings.DATA_DIR, settings.CORPUS_NAME + '-' + lang + '.tsv')
    corpus_file[lang] = os.path.join(settings.MODELS_DIR, settings.CORPUS_NAME + '-' + lang + '_' + settings.METHOD + '.mm')
    index_file[lang] = os.path.join(settings.MODELS_DIR, settings.CORPUS_NAME + '-' + lang + '_' + settings.METHOD + '_index')
    dico_file[lang] = os.path.join(settings.MODELS_DIR, settings.CORPUS_NAME + '-' + lang + '_wordids.txt')

    print('settings.CORPUS_NAME', settings.CORPUS_NAME)

    try:
        corpus[lang] = corpora.mmcorpus.MmCorpus(corpus_file[lang])
    except Exception:
        raise IOError('Impossible de charger le fichier %s. Avez-vous bien appliqué le script corpus_to_matrix.py ?' % (corpus_file[lang]))

    try:
        index[lang] = similarities.docsim.Similarity.load(index_file[lang])
        print (index_file[lang])
    except Exception:
        raise IOError("""Impossible de charger le fichier %s. Avez-vous bien appliqué le script %s avec l'option --saveindex ?""" % (settings.METHOD, index_file))

    try:
        id2word[lang] = corpora.dictionary.Dictionary.load_from_text(dico_file[lang])
    except Exception:
        raise IOError("Impossible de charger le fichier %s" % (dico_file[lang]))

    # Construction d'un tableau contenant pour chaque article son titre, l'auteur, les mots-clefs
    metadonnees[lang] = {}
    with open(tsv_file[lang]) as f:
        for l in f:
            doc = utils.Document(l)
            metadonnees[lang][doc.id] = {'titre' : doc.title, 'auteurs': doc.authors, 'date': doc.date, 'mots': list(doc.keywords), 'url_site': doc.url_site }


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

    # choix de la langue
    lang = '?'
    if 'lang' in request.POST:
        lang = request.POST['lang']
    if 'lang' in request.GET:
        lang = request.GET['lang']
    if not lang in settings.LANGS:
        lang = 'fr'

    # choix de la méthode parmi celles définies dans habeascorpus.settings
    method = settings.METHOD
    if 'method' in request.GET and request.GET['method'] in settings.METHODS:
        method = settings.METHODS[request.GET['method']]
    if 'method' in request.POST and request.POST['method'] in settings.METHODS:
        method = settings.METHODS[request.POST['method']]
    if method == 'tfidf':
        model_file = os.path.join(settings.MODELS_DIR, settings.CORPUS_NAME + '-' + lang +'_tfidf_model')
        model = models.tfidfmodel.TfidfModel.load(model_file)
    elif method.startswith('lsi'):
        model_file = os.path.join(settings.MODELS_DIR, settings.CORPUS_NAME + '-' + lang + '_' + method + '_model')
        model = models.lsimodel.LsiModel.load(model_file)
    elif method.startswith('lda'):
        model_file = os.path.join(settings.MODELS_DIR, settings.CORPUS_NAME + '-' + lang + '_' + method + '_model')
        model = models.ldamodel.LdaModel.load(model_file)
    
    neighbours = similar_articles.find_similar_articles(settings.CORPUS_NAME + '-' + lang, method, n=nb_articles, content=texte, data_dir=settings.MODELS_DIR, index=index[lang], id2word=id2word[lang], corpus=corpus[lang], model=model)

    result = { 'method': method, 'articles': [] }
    for article in neighbours:
        meta = metadonnees[lang][str(article['id'])]
        meta['id'] = str(article['id'])
        meta['score'] = 0 + article['score'] # converts np to float
        result['articles'].append(meta)
    print ('post:', texte)
    print ('result:', result)
    return HttpResponse(json.dumps(result), content_type="application/json")


def homepage():
    return u'Bookmarklet: <a href="javascript:var%20titre=document.title;var%20txt%20=%20\'\';%20if%20(window.getSelection)%20{txt=window.getSelection();}%20else%20if%20(document.getSelection){txt%20=%20document.getSelection();}%20else%20if%20(document.selection){txt%20=%20document.selection.createRange().text;}%20%20var%20url=document.location;%20void%20(btw=window.open%20(\'https://archives.mondediplo.com?page=diploiser#titre=\'+(encodeURIComponent(titre))+\'&url=\'+(encodeURIComponent(url))+encodeURI(\'\r\r\')+\'&texte=\'+(encodeURIComponent(txt))))">+diploiser</a>'




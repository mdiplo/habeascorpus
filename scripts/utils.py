# -*- coding: utf-8 -*-

"""

Des fonctions régulièrement utilisées dans les autres fichiers

"""

import os, sys
#import nltk
import re

def textimport(text):
    if sys.version_info[0] == 2:
        return unicode(text, 'utf8')
    return str(text)

class Document:

    """Une classe qui représente un document """

    def __init__(self, raw_document):
        id, title, chapo, text, lang, authors, keywords, date, url_site = raw_document.rstrip('\n').split('\t')

        self.id = id
        self.title = title
        self.chapo = textimport(chapo)
        text = textimport(text)
        text = re.sub('\\\\n', '', text)
        text = re.sub('\\n', '', text)
        self.text = text 
        self.lang = lang
        self.authors = authors.split(', ')
        self.keywords = set(keywords.split(', '))
        self.date = date
        self.url_site = url_site

    def __str__(self):
        id = self.id
        title = self.title
        chapo = self.chapo.encode('utf8')
        text = self.text.encode('utf8')
        lang = self.lang
        authors = ', '.join(self.authors)
        keywords = ', '.join(self.keywords)
        date = self.date
        url_site = self.url_site

        return '\t'.join([id, title, chapo, text, lang, authors, keywords, date, url_site]) + '\n'

    def get_tokens(self, stopwords):
    
        """ tokenize le document """
        
        text_tokens = [t.lower() for t in re.split(r'\W+', self.chapo + self.text, 0, re.UNICODE)[1:-1] if t.lower() not in stopwords]
        return text_tokens


def tokenize(texte, stopwords=set([]), stem=False):
    """
    Renvoie un texte sous forme de liste de mots, en retirant les mots trop
    communs (ex: le, la, est,...).
    Si stem=True, les mots sont stemmatisés.

    :Parameters:
    -`stopwords` : ensemble de stopwords à ignorer

    """

    tokens = [t.lower() for t in re.split(r'\W+', texte, 0, re.UNICODE) if t.lower() not in stopwords]
    
    if stem:
        stemmer = nltk.stem.snowball.FrenchStemmer()
        tokens = map(stemmer.stem, tokens)

    return tokens


def split_path(file_path):
    """
    Renvoie sous la forme d'un dictionnaire le nom du fichier sans l'extension,
    le nom avec l'extension, et le chemin absolu.
    >>> split_path('/home/bob/article.tsv')
    {'name' : 'article', 'file_name' : 'article.tsv', 'path' : '/gome/bob/article.tsv'}
    """

    file_name = os.path.split(file_path)[1]
    name = os.path.splitext(file_name)[0]

    return {'name': name, 'file_name': file_name, 'path': file_path}


def get_article_by_id(id, docid_file):
    """Renvoie l'index dans le corpus de l'article dont l'id est id"""

    with open(docid_file, 'r') as f:
        for i, line in enumerate(f):
            id_article, titre = line.split('\t')
            if id == int(id_article):
                return i


def get_article_by_corpus_number(n, docid_file):
    """Renvoie l'id du document dont l'index dans le corpus est n"""
    with open(docid_file, 'r') as f:
        for i, line in enumerate(f):
            id_article, titre = line.split('\t')
            if i == n:
                return int(id_article)
                
def get_article_title_by_id(id, docid_file):
    """Renvoie le titre dans le corpus de l'article dont l'id est id"""

    with open(docid_file, 'r') as f:
        for i, line in enumerate(f):
            id_article, titre = line.split('\t')
            if id == int(id_article):
                return titre

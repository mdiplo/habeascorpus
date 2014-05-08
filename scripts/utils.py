# -*- coding: utf-8 -*-
import os
import nltk
import re


class Document:

    def __init__(self, raw_document):
        id, title, chapo, text, lang, authors, keywords, date = raw_document.rstrip('\n').split('\t')

        self.id = id
        self.title = title
        self.chapo = chapo
        self.text = unicode(text, 'utf8')
        self.lang = lang
        self.authors = authors.split(', ')
        self.keywords = set(keywords.split(', '))
        self.date = date

    def __str__(self):
        id = self.id
        title = self.title
        chapo = self.chapo
        text = self.text.encode('utf8')
        lang = self.lang
        authors = ', '.join(self.authors)
        keywords = ', '.join(self.keywords)
        date = self.date

        return '\t'.join([id, title, chapo, text, lang, authors, keywords, date]) + '\n'

    def get_text_tokens(self):
        text_tokens = [t.lower() for t in re.split(r'\W+', self.text, 0, re.UNICODE)[1:-1]]
        return text_tokens

    def remove_text(self, s):
        self.text = re.sub(s, '', self.text)


def tokenize(texte, stopwords=None, stem=False):
    """
    Renvoie un texte sous forme de liste de mots, en retirant les mots trop
    communs (ex: le, la, est,...).
    Si stem=True, les mots sont stemmatisés.

    :Parameters:
    -`stopwords` : ensemble de stopwords à ignorer

    """

    tokens_2d = [nltk.word_tokenize(sent) for sent in nltk.sent_tokenize(texte)]
    tokens = [x.lower() for sublist in tokens_2d for x in sublist
              if x.isalpha() and x.lower() not in stopwords]
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
            if id == int(line):
                return i


def get_article_by_corpus_number(n, docid_file):
    with open(docid_file, 'r') as f:
        for i, line in enumerate(f):
            if i == n:
                return int(line)

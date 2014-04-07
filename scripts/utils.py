# -*- coding: utf-8 -*-
import os
import nltk


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


def get_article(n, tsv_file):
    """Renvoie l'article dont le numéro dans le corpus est n"""

    with open(tsv_file, 'r') as f:
        f.readline()  # On passe la première ligne qui contient le nom des colonnes
        for i, line in enumerate(f):
            if i == n:
                (_, titre, _, texte, _, auteur, _, date) = line.split('\t')
                return {'titre': titre, 'texte':   texte, 'date': date, 'auteur': auteur}

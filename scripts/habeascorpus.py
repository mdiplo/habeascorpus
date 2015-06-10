# -*- coding: utf-8 -*-
import utils
import gzip
from nltk.corpus import stopwords
from gensim import corpora


class HabeasCorpus(corpora.TextCorpus):

    """
    TextCorpus est une classe abstraite, pour l'utiliser il faut hériter
    et redéfinir get_texts(), qui indique la manière
    de récupérer un fichier sous la forme de tokens
    """

    def __init__(self, corpus_file, stopwords=None):
        """
        :Parameters:
            -`stop_words` : liste de stopwords à ignorer

        """

        self.stopwords = set(stopwords)
        super(HabeasCorpus, self).__init__(corpus_file)

    def get_texts(self):
        with file_read(self.input) as f:
            f.readline()  # La première ligne qui contient les noms des colonnes
            for i, raw_line in enumerate(f):
                try:
                    document = utils.Document(raw_line)
                except Exception:
                    raise ValueError("La ligne n°%d n'est pas au bon format" % (i+1))
                yield document.get_tokens(self.stopwords)


def file_read(f):
    if f.endswith('.gz'):
        return gzip.open(f, 'r')
    else:
        return open(f, 'r')

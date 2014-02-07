# -*- coding: utf-8 -*-
import nltk
import utils
from gensim import corpora

class HabeasCorpus(corpora.TextCorpus):
    """TextCorpus est une classe abstraite, pour l'utiliser il faut hériter et redéfinir get_texts(), qui indique la manière 
    de récupérer un fichier sous la forme de tokens"""
    
    def get_texts(self):
        with open(self.input, 'r') as f:
            f.readline() #La première ligne qui contient les noms des colonnes
            for raw_line in f:
                (id_article, titre, chapo, texte, langue, auteur, mots, date) = raw_line.split('\t')             
                yield utils.tokenize(texte)
                

    



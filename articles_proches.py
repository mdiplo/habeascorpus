# -*- coding: utf-8 -*-
import logging
import sys
import utils
from gensim import corpora, similarities
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


"""Renvoie les num_articles les plus proches de l'article n du corpus"""
n = int(sys.argv[1])
print n
num_articles = int(sys.argv[2])

corpus_lda = corpora.mmcorpus.MmCorpus('articles_fr_lda.mm')
index = similarities.MatrixSimilarity.load('articles_fr_similarityindex')
article = utils.get_article(n, 'articles_fr.tsv')
vec_lda = corpus_lda[n]

index.num_best = num_articles
sims = index[vec_lda]

print "\nLes %d articles les plus proches de l'article «%s» sont :\n" % (num_articles, utils.get_article(n, 'articles_fr.tsv')['titre'])
for i, article in enumerate(sims):
    titre = utils.get_article(article[0], 'articles_fr.tsv')['titre']
    date = utils.get_article(article[0], 'articles_fr.tsv')['date']
    auteur = utils.get_article(article[0], 'articles_fr.tsv')['auteur']
    print "%d. %s %s %s\n" % (article[0], titre, date, auteur)


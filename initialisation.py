# -*- coding: utf-8 -*-
import re
import logging  
import habeascorpus
from gensim import corpora, models, similarities
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

#On extraie les articles et reportages français


## remplacer les True/False par test d'existence des fichiers
## (encore mieux : faire un makefile / gruntfile)

if (False):
    with open('all.tsv', 'r') as f, open('articles_fr.tsv', 'w') as out, open('articles_fr_num.txt', 'w') as num_articles:
        out.write(f.readline())
        nb_articles = 0
    for raw_line in f:
        (id_article, titre, chapo, texte, langue, auteur, mots, date) = raw_line.split('\t')
        mots = set(re.sub(r'\n','', mots).split(', '))
        if (langue == 'fr' and ('article' in  mots or 'reportage' in mots)):
            nb_articles += 1
            out.write(raw_line)
            num_articles.write('%s\t%s\n' % (nb_articles, titre))

    corpus = habeascorpus.HabeasCorpus('articles_fr.tsv')
    corpus.dictionary.filter_extremes(no_below=3, no_above=0.5)
    corpus.dictionary.save_as_text('articles_fr_wordids.txt')

    corpora.mmcorpus.MmCorpus.serialize('articles_fr_bow.mm', corpus, progress_cnt=1000)

    del corpus


corpus = corpora.mmcorpus.MmCorpus('articles_fr_bow.mm')
id2word = corpora.dictionary.Dictionary.load_from_text('articles_fr_wordids.txt')

#On applique l'algo LDA
if (False):
    lda = models.ldamodel.LdaModel(corpus=corpus, id2word=id2word, num_topics=100, passes=3)

    lda.save('articles_fr.lda')

else:
    lda = models.ldamodel.LdaModel('articles_fr.lda')

if (True):
    corpora.mmcorpus.MmCorpus.serialize('articles_fr_lda.mm', lda[corpus], progress_cnt=1000)


#On affiche les topics :
for i, topic in enumerate(lda.show_topics(topics=100)):
    print "Topic n°%d : %s\n" %(i, topic)
    
del lda
corpus_lda = corpora.mmcorpus.MmCorpus('articles_fr_lda.mm')

#On créé l'index de similarité
index = similarities.MatrixSimilarity(corpus_lda, num_features=100)
index.save('articles_fr_similarityindex')

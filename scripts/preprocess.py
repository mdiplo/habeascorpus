# -*- coding: utf-8 -*-
"""
Applique un prétraitement à un corpus :
    - Met les mots en minuscule

    - Trouve les entités d'un corpus ("New York", "Barrack Obama",
    "Le président de la république") et produit un nouveau corpus
    en remplaçant les occurrences des entités trouvées par une entité
    unique : New York -> New_York

    - Supprime les mots peu fréquents, les signes de ponctuation

"""

import argparse
import nltk
import os
import utils

parser = argparse.ArgumentParser(description="""Détermine les entités d'un corpus""")
parser.add_argument('corpus_file', type=str,
                    help="Fichier .tsv contenant les articles du corpus")
parser.add_argument('--stopwords', type=str, help='Un fichier contenant un stopword par ligne')
args = parser.parse_args()
corpus_file_name = os.path.basename(args.corpus_file)
corpus_name = os.path.splitext(corpus_file_name)[0]

if args.stopwords:
    with open(args.stopwords) as f:
        stopwords = [line.rstrip() for line in f]
else:
    stopwords = []

stopwords.extend(nltk.corpus.stopwords.words('french'))
stopwords = set([unicode(x, 'utf8') for x in stopwords])

with open(args.corpus_file) as f:
    tokens = []

    for i, raw_document in enumerate(f):
        if i > 3000:
            # on cherche les bigrammes sur 3000 documents
            break

        print "Lecture document %d" % (i)
        doc = utils.Document(raw_document)
        doc.remove_text('\\\\n')
        doc.remove_text('\\r')
        text_tokens = [t for t in doc.get_text_tokens() if t not in stopwords]
        tokens.extend(text_tokens)

    bigram_measures = nltk.collocations.BigramAssocMeasures()
    finder = nltk.collocations.BigramCollocationFinder.from_words(tokens)

    finder.apply_freq_filter(5)  # supprime les bigrammes qui apparaissent moins de 5 fois dans le corpus

    bigrams = set(finder.above_score(bigram_measures.pmi, 5))

    print "Bigrammes trouvés"

    # on se replace au début du fichier
    f.seek(0)

    print "Écriture du nouveau corpus %s" % (corpus_name + 'preprocessed.tsv')
    with open(corpus_name + '_preprocessed.tsv', 'w') as o:
        o.write(f.readline())  # headers
        for i, raw_document in enumerate(f):
            print "Écriture document %d" % (i)
            doc = utils.Document(raw_document)
            doc.remove_text('\\\\n')
            doc.remove_text('\\r')
            text_tokens = [t for t in doc.get_text_tokens() if t not in stopwords]
            doc.text = ""

            for i in xrange(len(text_tokens) - 1):
                doc.text += text_tokens[i]
                if (text_tokens[i], text_tokens[i+1]) in bigrams:
                    doc.text += '_'
                else:
                    doc.text += ' '

            doc.text += text_tokens[len(text_tokens) - 1]

            o.write(str(doc))

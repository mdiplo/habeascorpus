# -*- coding: utf-8 -*-

import re
import argparse

import utils

# Les arguments à fournir en ligne de commande
parser = argparse.ArgumentParser(description="""Génère le graph des articles""")
parser.add_argument('corpus', type=str, help="Le nom du corpus (sans l'extension .tsv')")
parser.add_argument('-v', '--verbose', action='store_true',
                    help="Afficher les messages d'information")
args = parser.parse_args()

corpus_file = args.corpus + '.tsv'

with open(corpus_file) as f:
    o = open(args.corpus + '_graph.adj', 'w')
    
    f.readline()
    for i, raw_line in enumerate(f):
        doc = utils.Document(raw_line)
        
        renvois = re.findall("\[([^][]*?([[]\w*[]][^][]*)*)->(>?)([^]]*)\]", doc.text)
        
        for ref in renvois:
            if re.match("(?:art)?(\d+)", ref[3]):
                o.write(doc.id + ' ' + re.match("(?:art)?(\d+)", ref[3]).group(1) + '\n')
                
            if re.match("http://(www\.)?monde-diplomatique\.fr/\d{4}/\d{2}/\w*/(\d+)", ref[3]):
                o.write(doc.id + ' ' + re.match("http://(www\.)?monde-diplomatique\.fr/\d{4}/\d{2}/\w*/(\d+)", ref[3]).group(2  ) + '\n')
                 
        if args.verbose:
            print "Article n°%d traité" % (i)
                
    o.close()

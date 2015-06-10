# -*- coding: utf-8 -*-

import argparse

import utils
import re

# Les arguments à fournir en ligne de commande
parser = argparse.ArgumentParser(description="""Trouve les ids des articles à partir du fichier MDV""")
parser.add_argument('corpus', type=str, help="Le nom du corpus (sans l'extension .tsv')")
parser.add_argument('articles_mdv', type=str, help='Le fichier MDV')
parser.add_argument('-v', '--verbose', action='store_true',
                    help="Afficher les messages d'information")
args = parser.parse_args()

corpus_file = args.corpus + '.tsv'


with open(corpus_file) as f:
    with open(args.articles_mdv) as o:
    
        output_file = open('avec_id_' + args.articles_mdv, 'w')
        o.readline()
        articles_mdv = [l for i, l in enumerate(o.readlines()) if i % 2 == 1]
        
        for i, article in enumerate(articles_mdv):
            
            if args.verbose:
                print "Traitement de l'article MDV n° %d" % (i)
                
            res = re.match(r"(.*)«(.*)»(.*)", article)
            f.seek(0)
            f.readline()
            trouve = False
            for raw_line in f:
                doc = utils.Document(raw_line)
                if doc.title == res.group(2).rstrip(' ').lstrip(' '):
                    output_file.write(res.group(1) + "«[" + res.group(2) + '->' + doc.id + ']»' + res.group(3) + '\n\n')
                    trouve = True
                    break
                
            # article non retrouvé, on recopie sans l'id
            if not trouve:
                output_file.write(article+'\n')
            
            
output_file.close()

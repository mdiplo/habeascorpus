# habeascorpus

analyse un corpus de textes avec gensim, et fait des trucs avec

## Préparation des données
le corpus se présente sous la forme d'un grand fichier TSV (un article par ligne)

Pour SPIP on peut exporter sa base comme suit :

```
echo "SELECT a.id_article,a.titre, a.chapo,a.texte,a.lang, GROUP_CONCAT(DISTINCT u.nom SEPARATOR ', ') AS auteurs, GROUP_CONCAT(DISTINCT m.titre SEPARATOR ', ') AS mots, SUBSTRING(a.date_redac,1,7) AS date FROM spip_articles a LEFT JOIN spip_auteurs_articles au ON a.id_article=au.id_article LEFT JOIN spip_auteurs u ON au.id_auteur=u.id_auteur LEFT JOIN spip_mots_articles am ON a.id_article=am.id_article LEFT JOIN spip_mots m ON am.id_mot=m.id_mot WHERE a.statut IN ('publie') GROUP BY a.id_article;" | mysql $BASE -B > $BASE.tsv
```

(ici avec un test sur le statut 'publié') ; ensuite, on peut regarder le nombre d'articles écrits par Untel (ou parlant de "truc"), avec le nombre de mots et de signes correspondants.

voir aussi http://seenthis.net/messages/224616

Une fois le fichier corpus.tsv obtenu, on le place dans le dossier `/habeascorpus/data`. On calcule la représentation bag-of-words du corpus en lançant depuis le dosier `/habeascorpus/data` :

```
python ../corpus_to_matrix.py corpus.tsv -v
```

On obient ainsi dans le dossier data le fichier `corpus_wordids.txt` qui associe un id à chaque mot du corpus, et le fichier `corpus_bow.mm`, qui indique pour chaque document les mots qu'il contient.

## Calcul des topics

On peut ensuite appliquer l'algorithme LDA qui détermine les topics du corpus (ici on demande 100 topics):

```
python ../lda.py 100 corpus_bow.mm corpus_wordids.txt -v
```

Cette commande produit le fichier `corpus_lda.mm`, qui indique pour chaque document les topics qui lui sont reliés. Elle produit également le fichier `corpus_topics.txt`, qui liste les topics du corpus.

## Explorateur de topics

### Installation
`pip install SQLAlchemy`
`pip install Django`

### Utilisation
On peut maintenant explorer le corpus dans un navigateur, en générant au préalable une base de données contenant les informations nécessaires :

```
cd habeascorpus/browser
python generate_database.py ../data
python server.py
```

Puis on charge la page `localhost:9000` dans un navigateur web.



habeascorpus
============

analyse un corpus de textes avec gensim, et fait des trucs avec


le corpus se présente sous la forme d'un grand fichier #TSV (un article par ligne)

Pour SPIP on peut exporter sa base comme suit :

```
echo "SELECT a.id_article,a.titre, a.chapo,a.texte,a.lang, GROUP_CONCAT(DISTINCT u.nom SEPARATOR ', ') AS auteurs, GROUP_CONCAT(DISTINCT m.titre SEPARATOR ', ') AS mots, SUBSTRING(a.date_redac,1,7) AS date FROM spip_articles a LEFT JOIN spip_auteurs_articles au ON a.id_article=au.id_article LEFT JOIN spip_auteurs u ON au.id_auteur=u.id_auteur LEFT JOIN spip_mots_articles am ON a.id_article=am.id_article LEFT JOIN spip_mots m ON am.id_mot=m.id_mot WHERE a.statut IN ('publie') GROUP BY a.id_article;" | mysql $BASE -B > $BASE.tsv
```

(ici avec un test sur le statut 'publié') ; ensuite, on peut regarder le nombre d'articles écrits par Untel (ou parlant de "truc"), avec le nombre de mots et de signes correspondants.

voir aussi http://seenthis.net/messages/224616


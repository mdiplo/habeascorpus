# -*- coding: utf-8 -*-
import nltk
from gensim import corpora, models, similarities

def tokenize(texte):
    """Renvoie un texte sous forme de liste de mots, en retirant les mots trop communs (ex: le, la, est,...)"""
    tokens_2d = [nltk.word_tokenize(sent) for sent in nltk.sent_tokenize(texte)]
    tokens = [x.lower() for sublist in tokens_2d for x in sublist if x.isalpha() and x not in set(nltk.corpus.stopwords.words('french'))]   
    return tokens
    
def get_article(n, tsv_file):
    """Renvoie l'article dont le numéro dans le corpus est n"""
    
    with open(tsv_file, 'r') as f:
        f.readline() #On passe la première ligne qui contient le nom des colonnes
        for i, line in enumerate(f):
            if i == n:
                (_, titre, _, texte, _, auteur, _, date) = line.split('\t')
                return {'titre': titre, 'texte':   texte, 'date': date, 'auteur': auteur}
         
        
def get_nearest_article(n, corpus_path, index_path, tsv_file, num_articles):
    """Renvoie les num_articles les plus proches de l'article n du corpus"""
    corpus_lda = corpora.mmcorpus.MmCorpus(corpus_path)
    index = similarities.MatrixSimilarity.load(index_path)
    article = get_article(n, tsv_file)
    vec_lda = corpus_lda[n]
    
    sims = index[vec_lda]
    sims = sorted(enumerate(sims), key=lambda item: -item[1])
    
    result = []
    for article in sims[:num_articles]:
        result.append(get_article(article[0], tsv_file)['titre'])
        
    return result
    
def query(query, dico_path, index_path, model_path, tsv_file, num_articles):
    """Moteur de recherche. Ne fonctionne pas pour l'instant"""
    dico = corpora.dictionary.Dictionary.load_from_text(dico_path)
    index = similarities.MatrixSimilarity.load(index_path)
    lda_model = models.ldamodel.LdaModel.load('Article non trouvé')
    vec_lda = lda_model[dico.doc2bow(tokenize(query))]
    
    print vec_lda 
    
    sims = index[vec_lda]
    sims = sorted(enumerate(sims), key=lambda item: -item[1])
    
    result = []
    for article in sims[:num_articles]:
        result.append(get_article(article[0], tsv_file)['titre'])
        
    return result
    
    
    

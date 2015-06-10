from django.db import models
from gensim import corpora, similarities, models

#Peut-on le faire avec des imports relatifs ?
import sys
import os.path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(os.path.join(root_path, 'scripts'))

data_path = os.path.join(os.path.join(root_path, 'data'), 'diplo_juillet2')

index_file = os.path.join(data_dir, corpus_name + '_' + method + '_index')
index = similarities.docsim.Similarity.load(index_file)

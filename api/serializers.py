from django.forms import widgets
from rest_framework import serializers
from browser.models import Document, Topic, DocumentTopic

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ('id', 'related_words', 'weight_in_corpus')

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('id', 'titre', 'chapo', 'langue', 'auteur', 'mots', 'date')
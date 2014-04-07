# -*- coding: utf-8 -*-

"""
Les serializers permettent de convertir des types de données complexes
(modèles, requètes SQL,...) en types Python natifs pour ensuite les
renvoyer en JSON, XML, etc. Les serializers permettent aussi de
déserializer.

"""

from rest_framework import serializers
from rest_framework import pagination
from api.models import Document, Topic


class TopicSerializer(serializers.ModelSerializer):
    # Lorsque on sérialize un topic, on veut récupérer les mots liés au
    # topic avec la méthode get_related_words
    related_words = serializers.Field(source='get_related_words')

    class Meta:
        model = Topic

        # Les champs à sérializer
        fields = ('id', 'related_words', 'weight_in_corpus')


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document

        # Les champs à sérializer
        fields = ('id', 'titre', 'chapo', 'langue', 'auteur', 'mots', 'date')


class DocumentPaginationSerializer(pagination.BasePaginationSerializer):
    """
    Permet de paginer les documents : plutôt que de renvoyer la liste des
    50 000 documents quand on veut y accéder, on renvoie les N premiers
    et un lien vers la liste des N suivants.

    """

    page = serializers.Field(source='paginator.page')

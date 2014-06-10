# -*- coding: utf-8 -*-
from api.models import Topic, Document
from api.serializers import TopicSerializer, DocumentSerializer
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status

"""
Dans le patron Modèle-Vue-Template, la Vue récupère les données et génère
un rendu (JSON, XML, ...)
DjangoREST fournit des classes abstraites de Vue qui permettent de simplifier
le code. 

"""

class TopicViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer


class TopicRelatedDocuments(generics.ListAPIView):
    """Renvoie les documents liés à un article classés par poids décroissant"""

    serializer_class = DocumentSerializer
    paginate_by = 10

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Topic.objects.\
                get(pk=pk).\
                documents.\
                order_by('-documenttopic__weight_in_document').\
                all()


@api_view(['GET'])
def topic_history(request, pk):
    """
    Renvoie l'historique du topic dont la Primary Key est pk.

    """

    try:
        topic = Topic.objects.get(pk=pk)
    except Topic.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    return Response(topic.get_history())


class DocumentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    paginate_by = 10


class DocumentNeighbours(generics.ListAPIView):
    """Renvoie les documents similaires à un document donné"""

    serializer_class = DocumentSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Topic.objects.\
                get(pk=pk).\
                documents.\
                order_by('-documenttopic__weight_in_document').\
                all()



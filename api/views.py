# -*- coding: utf-8 -*-
import json
from api.models import Topic, Document
from api.serializers import TopicSerializer, DocumentSerializer, DocumentPaginationSerializer
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status

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
    Renvoie l'historique d'un Topic : pour chaque année, le poids du topic dans
    le corpus et les 3 articles les  plus représentatifs du Topic à cette date.

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

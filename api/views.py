# -*- coding: utf-8 -*-
from api.models import Topic, Document
from api.serializers import TopicSerializer, DocumentSerializer, DocumentPaginationSerializer
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics

class TopicViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

class TopicRelatedDocuments(generics.ListAPIView):
    """Renvoie les documents liés à un article classés par poids décroissant"""

    serializer_class = DocumentSerializer
    paginate_by = 10

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Topic.objects.get(pk=pk).documents.order_by('-documenttopic__weight_in_document').all()


class DocumentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    paginate_by = 10

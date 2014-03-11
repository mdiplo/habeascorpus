from browser.models import Topic, Document
from browser.serializers import TopicSerializer, DocumentSerializer
from rest_framework import generics

class TopicList(generics.ListCreateAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

class DocumentList(generics.ListCreateAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
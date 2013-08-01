from rest_framework import generics

from farm.models import Node
from farm.serializers import NodeSerializer

class NodeList(generics.ListCreateAPIView):
    queryset = Node.objects.all()
    serializer_class = NodeSerializer

class NodeDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NodeSerializer

    def get_queryset(self):
        queryset = Node.objects.all()
        if "slug" in self.kwargs:
            queryset = queryset.filter(slug=self.kwargs['slug'])
        if "pk" in self.kwargs:
            queryset = queryset.filter(id=self.kwargs['pk'])
        return queryset

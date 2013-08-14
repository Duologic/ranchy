from rest_framework import generics, viewsets

from farm.models import Node
from farm.serializers import NodeSerializer


class NodeViewSet(viewsets.ModelViewSet):
    serializer_class = NodeSerializer
    queryset = Node.objects.all()


class NodeBySlug(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NodeSerializer

    def get_queryset(self):
        queryset = None 
        if "slug" in self.kwargs:
            queryset = Node.objects.filter(slug=self.kwargs['slug'])
        return queryset

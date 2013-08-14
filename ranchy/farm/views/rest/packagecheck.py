from rest_framework import generics, viewsets

from farm.models import PackageCheck
from farm.serializers import PackageCheckSerializer


class PackageCheckViewSet(viewsets.ModelViewSet):
    serializer_class = PackageCheckSerializer
    queryset = PackageCheck.objects.all()


class PackageCheckByNode(generics.ListCreateAPIView):
    serializer_class = PackageCheckSerializer

    def get_queryset(self):
        queryset = PackageCheck.objects.all()
        if "nodeslug" in self.kwargs:
            queryset = queryset.filter(node__slug=self.kwargs['nodeslug'])
        return queryset

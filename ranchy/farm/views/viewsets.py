from rest_framework import viewsets, status
from rest_framework.response import Response

from farm.models import (Owner, Location, Node, Package, PackageCheck)
from farm.serializers import (OwnerSerializer, LocationSerializer,
                              NodeSerializer, PackageSerializer, PackageCheckSerializer)


class BulkModelViewSet(viewsets.ModelViewSet):

    def create(self, request, *args, **kwargs):
        data = request.DATA
        serializer = self.get_serializer(data=data, many=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        data = request.DATA
        queryset = self.queryset
        serializer = self.get_serializer(queryset, data=data, many=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OwnerViewSet(BulkModelViewSet):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer


class LocationViewSet(BulkModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class NodeViewSet(BulkModelViewSet):
    serializer_class = NodeSerializer
    queryset = Node.objects.all()
    lookup_field = 'slug'


class PackageCheckViewSet(BulkModelViewSet):
    serializer_class = PackageCheckSerializer
    queryset = PackageCheck.objects.all()

    def get_queryset(self):
        if "nodeslug" in self.kwargs:
            return self.queryset.filter(node__slug=self.kwargs['nodeslug'])
        return self.queryset


class PackageViewSet(BulkModelViewSet):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        if "nodeslug" in self.kwargs:
            return self.queryset.filter(packagecheck__node__slug=self.kwargs['nodeslug'])
        return self.queryset

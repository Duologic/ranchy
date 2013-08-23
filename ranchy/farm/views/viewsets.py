from rest_framework import viewsets, status
from rest_framework.response import Response

from farm.models import (Owner, Location, Node, Package, PackageCheck)
from farm.serializers import (OwnerSerializer, LocationSerializer,
                              NodeSerializer, PackageSerializer,
                              PackageCheckSerializer)


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
    lookup_field = 'slug'


class LocationViewSet(BulkModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    lookup_field = 'slug'


class NodeViewSet(BulkModelViewSet):
    serializer_class = NodeSerializer
    queryset = Node.objects.all()
    lookup_field = 'slug'


class PackageCheckViewSet(BulkModelViewSet):
    serializer_class = PackageCheckSerializer
    queryset = PackageCheck.objects.all()

    def get_queryset(self):
        package = self.request.QUERY_PARAMS.get('package', None)
        if package is not None:
            self.queryset = self.queryset.filter(package__slug=package)
        nodeslug = self.request.QUERY_PARAMS.get('nodeslug', None)
        if nodeslug is not None:
            self.queryset = self.queryset.filter(node__slug=nodeslug)
        return self.queryset


class PackageViewSet(BulkModelViewSet):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        packagetype = self.request.QUERY_PARAMS.get('packagetype', None)
        if packagetype is not None:
            self.queryset = self.queryset.filter(packagetype=packagetype)
        nodeslug = self.request.QUERY_PARAMS.get('nodeslug', None)
        if nodeslug is not None:
            self.queryset = self.queryset.filter(packagecheck__node__slug=nodeslug)
        return self.queryset

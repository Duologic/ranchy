from rest_framework import viewsets, status
from rest_framework.response import Response

from farm.models import Owner, Location, GroupType, Group, Node, PackageType, Package, PackageCheck
from farm.serializers import OwnerSerializer, LocationSerializer, GroupTypeSerializer, GroupSerializer, NodeSerializer, PackageTypeSerializer, PackageSerializer, PackageCheckSerializer


class BulkModelViewSet(viewsets.ModelViewSet):
    
    
    def create(self, request, *args, **kwargs):
        data = request.DATA
        serializer = GroupTypeSerializer(data=data, many=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, *args, **kwargs):
        data = request.DATA
        queryset = GroupType.objects.all()
        serializer = GroupTypeSerializer(queryset, data=data, many=True)

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


class GroupTypeViewSet(BulkModelViewSet):
    queryset = GroupType.objects.all()
    serializer_class = GroupTypeSerializer


class GroupViewSet(BulkModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class NodeViewSet(BulkModelViewSet):
    serializer_class = NodeSerializer
    queryset = Node.objects.all()
    lookup_field = 'slug'


class PackageTypeViewSet(BulkModelViewSet):
    queryset = PackageType.objects.all()
    serializer_class = PackageTypeSerializer


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

from rest_framework import viewsets

from farm.models import Owner, Location, GroupType, Group, Node, PackageType, Package, PackageCheck
from farm.serializers import OwnerSerializer, LocationSerializer, GroupTypeSerializer, GroupSerializer, NodeSerializer, PackageTypeSerializer, PackageSerializer, PackageCheckSerializer


class OwnerViewSet(viewsets.ModelViewSet):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class GroupTypeViewSet(viewsets.ModelViewSet):
    queryset = GroupType.objects.all()
    serializer_class = GroupTypeSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class NodeViewSet(viewsets.ModelViewSet):
    serializer_class = NodeSerializer
    queryset = Node.objects.all()
    lookup_field = 'slug'


class PackageTypeViewSet(viewsets.ModelViewSet):
    queryset = PackageType.objects.all()
    serializer_class = PackageTypeSerializer


class PackageCheckViewSet(viewsets.ModelViewSet):
    serializer_class = PackageCheckSerializer
    queryset = PackageCheck.objects.all()

    def get_queryset(self):
        if "nodeslug" in self.kwargs:
            return self.queryset.filter(node__slug=self.kwargs['nodeslug'])
        return self.queryset


class PackageViewSet(viewsets.ModelViewSet):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        if "nodeslug" in self.kwargs:
            return self.queryset.filter(packagecheck__node__slug=self.kwargs['nodeslug'])
        return self.queryset

from rest_framework import viewsets

from farm.models import Owner, Location, GroupType, Group, PackageType
from farm.serializers import OwnerSerializer, LocationSerializer, GroupTypeSerializer, GroupSerializer, PackageTypeSerializer


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


class PackageTypeViewSet(viewsets.ModelViewSet):
    queryset = PackageType.objects.all()
    serializer_class = PackageTypeSerializer

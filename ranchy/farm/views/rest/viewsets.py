from rest_framework import viewsets, status
from rest_framework.response import Response

from farm.models import Owner, Location, GroupType, Group, Node, PackageType, Package, PackageCheck
from farm.serializers import OwnerSerializer, LocationSerializer, GroupTypeSerializer, GroupSerializer, NodeSerializer, PackageTypeSerializer, PackageSerializer, PackageCheckSerializer


class BulkModelViewSet(viewsets.ModelViewSet):
    
    
    def create(self, request, *args, **kwargs):
        import pdb; pdb.set_trace()
        data = request.DATA #JSONParser().parse(request)
        serializer = GroupTypeSerializer(data=data, many=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, *args, **kwargs):
        import pdb; pdb.set_trace()
        data = request.DATA #JSONParser().parse(request)
        queryset = GroupType.objects.all()
        serializer = GroupTypeSerializer(queryset, data=data, many=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OwnerViewSet(viewsets.ModelViewSet):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class GroupTypeViewSet(BulkModelViewSet):
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

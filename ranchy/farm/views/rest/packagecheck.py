from rest_framework import generics

from farm.models import PackageCheck
from farm.serializers import PackageCheckSerializer

class PackageCheckList(generics.ListCreateAPIView):
    serializer_class = PackageCheckSerializer

    def get_queryset(self):
        queryset = PackageCheck.objects.all()
        if "nodeslug" in self.kwargs:
            queryset = queryset.filter(node__slug=self.kwargs['nodeslug'])
        if "packageid" in self.kwargs:
            queryset = queryset.filter(package=self.kwargs['packageid'])
        return queryset

class PackageCheckDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PackageCheckSerializer

    def get_queryset(self):
        queryset = PackageCheck.objects.all()
        if "pk" in self.kwargs:
            queryset = queryset.filter(id=self.kwargs['pk'])
        return queryset

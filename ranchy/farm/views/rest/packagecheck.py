from rest_framework import generics
from django.http import HttpResponse

from farm.models import PackageCheck
from farm.serializers import PackageCheckSerializer


class PackageCheckList(generics.ListCreateAPIView):
    serializer_class = PackageCheckSerializer

    def get_queryset(self):
        queryset = PackageCheck.objects.all()
        filtered = False
        if "nodeslug" in self.kwargs:
            queryset = queryset.filter(node__slug=self.kwargs['nodeslug'])
            filtered = True
        if "packageid" in self.kwargs:
            queryset = queryset.filter(package=self.kwargs['packageid'])
            filtered = True
        if not filtered:
            content = {'queryset','query too long'}
            return HttpResponse(content, status=501)

        return queryset


class PackageCheckDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PackageCheckSerializer

    def get_queryset(self):
        queryset = PackageCheck.objects.all()
        if "pk" in self.kwargs:
            queryset = queryset.filter(id=self.kwargs['pk'])
        return queryset

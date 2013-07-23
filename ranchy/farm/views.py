from django.shortcuts import render
from django.http import Http404
from farm.models import Package,PackageCheck,Node,Group,PackageType,Location,Owner,PackageCheck
from farm.serializers import NodeSerializer, OwnerSerializer,PackageSerializer, PackageCheckSerializer

from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

def matrix(request, typeslug, nodeslug=''):
    context = ''

    try:
        packagetype = PackageType.objects.get(slug=typeslug)
        if nodeslug:
            nodeslugs = nodeslug.split(";")
            node_list = Node.objects.filter(slug__in=nodeslugs).filter(group=packagetype.group).all()
        else:
            node_list = Node.objects.filter(group=packagetype.group).all()
    except PackageType.DoesNotExist:
        node_list = None
        pass

    try:
        packagecheck_list = PackageCheck.objects.filter(node__in=node_list).all().prefetch_related('node').prefetch_related('package').order_by('package__name')
        prev = "" 
        dicti = {} 
        for packagecheck in packagecheck_list:
            if prev != packagecheck.package.name:
                prev = packagecheck.package.name
                dicti[prev] = {}
                for n in node_list:
                    dicti[prev][n.name] = None
            dicti[prev][packagecheck.node.name] = packagecheck

        context = {
            'dicti': sorted(dicti.iteritems(), key= lambda (k, v) :  (k, v)),
            }
    except:
        context = { 'dicti': None, }
        pass

    return render(request, 'matrix.html', context)

def nodeoverview(request):
    firewall_list = Node.objects.filter(group__name="Firewall").all().prefetch_related('owner').prefetch_related('location').select_related()
    for firewall in firewall_list:
        children = firewall.parents.all().order_by("name").select_related()
        for child in children:
            pass
            

    return "b";
#    context = {
#            }
#    return render(request, 'nodeoverview.html', context)

class NodeList(generics.ListCreateAPIView):
    queryset = Node.objects.all()
    serializer_class = NodeSerializer

class NodeDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NodeSerializer

    def get_queryset(self):
        queryset = Node.objects.all()
        if "slug" in self.kwargs:
            queryset = queryset.filter(slug=self.kwargs['slug'])
        if "pk" in self.kwargs:
            queryset = queryset.filter(id=self.kwargs['pk'])
        return queryset

class OwnerList(generics.ListCreateAPIView):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer

class OwnerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer

class PackageList(generics.ListCreateAPIView):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer

class PackageDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PackageSerializer

    def get_queryset(self):
        queryset = Package.objects.all()
        if "slug" in self.kwargs:
            queryset = queryset.filter(slug=self.kwargs['slug'])
        if "pk" in self.kwargs:
            queryset = queryset.filter(id=self.kwargs['pk'])
        return queryset

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

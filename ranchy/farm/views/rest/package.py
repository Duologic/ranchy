from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from rest_framework import generics, status
from rest_framework.views import APIView

from farm.models import Package
from farm.serializers import PackageSerializer
from farm.views.rest.general import JSONResponse
from rest_framework.parsers import JSONParser


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


class PackageBulk(APIView):

    def put(self, request):
        data = JSONParser().parse(request)
        queryset = Package.objects.all()
        serializer = PackageSerializer(queryset, data=data, many=True)

        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        else:
            return JSONResponse(serializer.errors, status=400)

    def post(self, request):
        data = JSONParser().parse(request)
        serializer = PackageSerializer(data=data, many=True)

        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        else:
            return JSONResponse(serializer.errors, status=400)

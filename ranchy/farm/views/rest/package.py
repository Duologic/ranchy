from rest_framework.views import APIView
from rest_framework.parsers import JSONParser

from farm.models import Package
from farm.serializers import PackageSerializer
from farm.views.rest.general import JSONResponse


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

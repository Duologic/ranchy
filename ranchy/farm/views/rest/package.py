from django.views.decorators.csrf import csrf_exempt

from rest_framework import generics, status

from farm.models import Package
from farm.serializers import PackageSerializer
from farm.views.rest.general import JSONResponse

@csrf_exempt
def package_bulk(request):
    if request.method == 'GET':
        return "yes"

    if request.method =='POST':
        data = JSONParser().parse(request)
        queryset = Package.objects.all()
        serializer = PackageSerializer(queryset, data=data, many=True)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        else:
            return JSONResponse(serializer.errors, status=400)

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

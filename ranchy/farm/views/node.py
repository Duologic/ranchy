from django.shortcuts import render
from django.http import Http404, HttpResponse
from farm.models import Node


def overview(request):
    firewall_list = Node.objects.filter(group__name="Firewall").prefetch_related('owner').prefetch_related('location').select_related()
    for firewall in firewall_list:
        children = firewall.parents.all().order_by("name").select_related()
        for child in children:
            pass

    return HttpResponse("b")
#    context = {
#            }
#    return render(request, 'nodeoverview.html', context)

from django.shortcuts import render
from farm.models import Node, Package, PackageCheck


def index(request, typeslug, nodeslug=''):
    context = ''

    try:
        packagetype = PackageType.objects.get(slug=typeslug)
        if nodeslug:
            nodeslugs = nodeslug.split(";")
            node_list = Node.objects.filter(
                slug__in=nodeslugs).filter(group=packagetype.group).all()
        else:
            node_list = Node.objects.filter(group=packagetype.group).all()
    except PackageType.DoesNotExist:
        node_list = None
        pass

    try:
        packagecheck_list = PackageCheck.objects.filter(node__in=node_list).prefetch_related('node').prefetch_related('package').order_by('package__name')
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
            'dicti': sorted(dicti.iteritems(), key=lambda (k, v):  (k, v)),
        }
    except:
        context = {'dicti': None, }
        pass

    return render(request, 'matrix.html', context)

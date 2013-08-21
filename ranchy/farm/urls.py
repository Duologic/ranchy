from django.conf.urls import patterns, url, include
from farm.views import matrix, servergram, viewsets

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'owner', viewsets.OwnerViewSet)
router.register(r'location', viewsets.LocationViewSet)
router.register(r'node', viewsets.NodeViewSet)
router.register(r'package', viewsets.PackageViewSet)
router.register(r'package/bynode/(?P<nodeslug>.+)', viewsets.PackageViewSet)
router.register(r'packagecheck', viewsets.PackageCheckViewSet)
router.register(r'packagecheck/bynode/(?P<nodeslug>.+)', viewsets.PackageCheckViewSet)

urlpatterns = patterns('',
                       url(r'^matrix/(?P<typeslug>[^/]+)/$',
                           matrix.index, name='matrixindex'),
                       url(r'^matrix/(?P<typeslug>[^/]+)/(?P<nodeslug>[^/]+)/$',
                           matrix.index, name='matrixindex'),
                       url(r'^nodes/$', servergram.overview, name='nodeoverview'),

                       url(r'^api/', include(router.urls)),
                       )

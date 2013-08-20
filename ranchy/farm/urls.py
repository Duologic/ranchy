from django.conf.urls import patterns, url, include
from farm.views import  matrix, servergram
from farm.views.rest import viewsets, package

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'owner', viewsets.OwnerViewSet)
router.register(r'location', viewsets.LocationViewSet)
router.register(r'grouptype', viewsets.GroupTypeViewSet)
router.register(r'group', viewsets.GroupViewSet)
router.register(r'node', viewsets.NodeViewSet)
router.register(r'packagetype', viewsets.PackageTypeViewSet)
router.register(r'package', viewsets.PackageViewSet)
router.register(r'package/bynode/(?P<nodeslug>.+)', viewsets.PackageViewSet)
router.register(r'packagecheck', viewsets.PackageCheckViewSet)
router.register(r'packagecheck/bynode/(?P<nodeslug>.+)', viewsets.PackageCheckViewSet)

urlpatterns = patterns('',
                       # HTML views
                       url(r'^matrix/(?P<typeslug>[^/]+)/$',
                           matrix.index, name='matrixindex'),
                       url(r'^matrix/(?P<typeslug>[^/]+)/(?P<nodeslug>[^/]+)/$',
                           matrix.index, name='matrixindex'),
                       url(r'^nodes/$', servergram.overview, name='nodeoverview'),

                       # REST views

                       url(r'^api/package/bulk/$',
                           package.PackageBulk.as_view()),

                       url(r'^api/', include(router.urls)),
                      )

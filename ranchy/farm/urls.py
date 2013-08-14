from django.conf.urls import patterns, url, include
from farm.views import  matrix, servergram
from farm.views.rest import genericviews, node, packagecheck, package

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'owner', genericviews.OwnerViewSet)
router.register(r'location', genericviews.LocationViewSet)
router.register(r'grouptype', genericviews.GroupTypeViewSet)
router.register(r'group', genericviews.GroupViewSet)
router.register(r'node', node.NodeViewSet)
router.register(r'packagetype', genericviews.PackageTypeViewSet)
router.register(r'package', genericviews.PackageTypeViewSet)
router.register(r'packagecheck', genericviews.PackageTypeViewSet)

urlpatterns = patterns('',
                       # HTML views
                       url(r'^matrix/(?P<typeslug>[^/]+)/$',
                           matrix.index, name='matrixindex'),
                       url(r'^matrix/(?P<typeslug>[^/]+)/(?P<nodeslug>[^/]+)/$',
                           matrix.index, name='matrixindex'),
                       url(r'^nodes/$', servergram.overview, name='nodeoverview'),

                       # REST views

                       # node by slug
                       url(r'^api/node/(?P<slug>.+)/$',
                           node.NodeBySlug.as_view()),

                       # custom package calls
                       url(r'^api/package/bulk/$',
                           package.PackageBulk.as_view()),
                       url(r'^api/package/(?P<slug>.+)/$',
                           package.PackageBySlug.as_view()),

                       # packagecheck
                       #url(r'^api/packagecheck/(?P<nodeslug>.+)/(?P<packageid>\d+)/$',
                       #    packagecheck.PackageCheckList.as_view()),
                       url(r'^api/packagecheck/(?P<nodeslug>.+)/$',
                           packagecheck.PackageCheckByNode.as_view(), name='packagecheck-node'),

                       url(r'^api/', include(router.urls)),
                      )

#urlpatterns = format_suffix_patterns(urlpatterns)

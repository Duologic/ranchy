from django.conf.urls import patterns, url, include
from farm.views import rest, matrix, node

from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = patterns('',
# HTML views
        url(r'^matrix/(?P<typeslug>[^/]+)/$', matrix.index, name='matrixindex'),
        url(r'^matrix/(?P<typeslug>[^/]+)/(?P<nodeslug>[^/]+)/$', matrix.index, name='matrixindex'),
        url(r'^nodes/$', node.overview, name='nodeoverview'),

# REST views
        # owner
        url(r'^api/owner/$', rest.owner.OwnerList.as_view()),
        url(r'^api/owner/(?P<pk>\d+)/$', rest.owner.OwnerDetail.as_view()),

        # node
        url(r'^api/node/$', rest.node.NodeList.as_view()),
        url(r'^api/node/(?P<pk>\d+)/$', rest.node.NodeDetail.as_view()),
        url(r'^api/node/(?P<slug>.+)/$', rest.node.NodeDetail.as_view()),

        # package
        ## should become cached! too long to request each time
        url(r'^api/package/$', rest.package.PackageList.as_view()),
        url(r'^api/package/(?P<pk>\d+)/$', rest.package.PackageDetail.as_view()),
        url(r'^api/package/(?P<slug>.+)/$', rest.package.PackageDetail.as_view()),
        ## concept code, will test in near future
        url(r'^api/packagebulk/$', rest.package.package_bulk),

        # packagecheck
        ## too big to request, should only be requested per node or per packageid
        ##url(r'^api/packagecheck/$', rest.packagecheck.PackageCheckList.as_view()),
        url(r'^api/packagecheck/(?P<pk>\d+)/$', rest.packagecheck.PackageCheckDetail.as_view()),
        url(r'^api/packagecheck/(?P<nodeslug>.+)/(?P<packageid>\d+)/$', rest.packagecheck.PackageCheckList.as_view()),
        url(r'^api/packagecheck/(?P<nodeslug>.+)/$', rest.packagecheck.PackageCheckList.as_view()),
)

urlpatterns = format_suffix_patterns(urlpatterns)

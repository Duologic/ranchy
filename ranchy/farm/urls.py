from django.conf.urls import patterns, url
from farm import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = patterns('',
        url(r'^matrix/(?P<typeslug>[^/]+)/$', views.matrix, name='index'),
        url(r'^matrix/(?P<typeslug>[^/]+)/(?P<nodeslug>[^/]+)/$', views.matrix, name='index'),
        url(r'^nodes$', views.nodeoverview, name='nodeoverview'),
        url(r'^api/owner/$', views.OwnerList.as_view()),
        url(r'^api/owner/(?P<pk>\d+)$', views.OwnerDetail.as_view()),
        url(r'^api/node/$', views.NodeList.as_view()),
        url(r'^api/node/(?P<pk>\d+)$', views.NodeDetail.as_view()),
        url(r'^api/node/(?P<slug>.+)$', views.NodeDetail.as_view()),
        url(r'^api/package/$', views.PackageList.as_view()),
        url(r'^api/package/(?P<pk>\d+)$', views.PackageDetail.as_view()),
        url(r'^api/package/(?P<slug>.+)$', views.PackageDetail.as_view()),
        url(r'^api/packagecheck/$', views.PackageCheckList.as_view()),
        url(r'^api/packagecheck/(?P<pk>\d+)$', views.PackageCheckDetail.as_view()),
        url(r'^api/packagecheck/(?P<nodeslug>.+)/(?P<packageid>\d+)$', views.PackageCheckList.as_view()),
        url(r'^api/packagecheck/(?P<nodeslug>.+)$', views.PackageCheckList.as_view()),
)

urlpatterns = format_suffix_patterns(urlpatterns)

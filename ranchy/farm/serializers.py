import urllib
from rest_framework import serializers
from rest_framework.reverse import reverse
from farm.models import Owner, Location, Node, Package, PackageCheck


class HyperlinkedQueryField(serializers.HyperlinkedIdentityField):
    """
    HyperlinkedIdentityField with multiple lookup
    fields and possible query parameters.
    """
    lookup_fields = None
    query_params = None

    def __init__(self, *args, **kwargs):
        self.lookup_fields = kwargs.pop('lookup_fields', None)
        self.query_params = kwargs.pop('query_params', None)
        super(HyperlinkedQueryField, self).__init__(*args, **kwargs)

    def get_url(self, obj, view_name, request, format):
        kwargs = {}

        if self.lookup_fields is not None:
            for k, v in self.lookup_fields.iteritems():
                if '__' in k:
                    (subobj, attr) = k.split('__')
                else:
                    subobj = k
                    attr = ''
                lookup_field = getattr(obj, subobj)
                if hasattr(lookup_field, attr):
                    kwargs[v] = getattr(lookup_field, attr)
                else:
                    kwargs[v] = lookup_field

        url = reverse(view_name, kwargs=kwargs, request=request, format=format)

        if self.query_params is not None:
            query_params = {}
            for k, v in self.query_params.iteritems():
                if hasattr(obj, k):
                    lookup_field = getattr(obj, k)
                else:
                    lookup_field = k
                query_params[v] = lookup_field

            params = urllib.urlencode(query_params)
            return url + '?' + params

        return url


class OwnerSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Owner


class LocationSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Location


class NodeSerializer(serializers.HyperlinkedModelSerializer):

    url_packagecheck = HyperlinkedQueryField(view_name='packagecheck-list',
                                             query_params={'slug': 'nodeslug'})
    url_package = HyperlinkedQueryField(view_name='package-list',
                                        query_params={'slug': 'nodeslug'})

    class Meta:
        model = Node


class PackageSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Package


class PackageCheckSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = PackageCheck

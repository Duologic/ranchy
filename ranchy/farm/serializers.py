from rest_framework import serializers
from rest_framework.reverse import reverse
from farm.models import Owner, Location, GroupType, Group, Node, PackageType, Package, PackageCheck


class HyperlinkedIdentityField(serializers.HyperlinkedIdentityField):
    url_kwargs = ''

    def __init__(self, *args, **kwargs):
        self.url_kwargs = kwargs.pop('url_kwargs', None)
        super(HyperlinkedIdentityField, self).__init__(*args, **kwargs)

    def get_url(self, obj, view_name, request, format):
        kwargs = {}
        for k, v in self.url_kwargs.iteritems():
            lookup_field = getattr(obj, k)
            kwargs[v] = lookup_field
        return reverse(view_name, kwargs=kwargs, request=request, format=format)


class OwnerSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Owner


class LocationSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Location


class GroupTypeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = GroupType


class GroupSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Group


class NodeSerializer(serializers.HyperlinkedModelSerializer):

    packagechecks = HyperlinkedIdentityField(view_name='packagecheck-node',
                                             lookup_field='a',
                                             url_kwargs={'slug':'nodeslug'})
    class Meta:
        model = Node


class PackageTypeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = PackageType


class PackageSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Package


class PackageCheckSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = PackageCheck



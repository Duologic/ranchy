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

        return reverse(view_name, kwargs=kwargs, request=request, format=format)

class OwnerSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Owner


class LocationSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Location


class GroupTypeSerializer(serializers.HyperlinkedModelSerializer):
#    def __init__(self, *args, **kwargs):
#        many = kwargs.pop('many', True)
#        super(GroupTypeSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = GroupType


class GroupSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Group


class NodeSerializer(serializers.HyperlinkedModelSerializer):

    packagecheck = HyperlinkedIdentityField(view_name='packagecheck-list',
                                             url_kwargs={'slug':'nodeslug'})
    package = HyperlinkedIdentityField(view_name='package-list',
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



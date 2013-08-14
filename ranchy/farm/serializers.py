from rest_framework import serializers
from rest_framework.reverse import reverse
from farm.models import Owner, Location, GroupType, Group, Node, PackageType, Package, PackageCheck


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


class HyperlinkedField(serializers.HyperlinkedIdentityField):
    variable_name = ''

    def __init__(self, *args, **kwargs):
        self.variable_name = kwargs.pop('variable_name', None)
        super(HyperlinkedField, self).__init__(*args, **kwargs)

    def get_url(self, obj, view_name, request, format):
        lookup_field = getattr(obj, self.lookup_field)
        kwargs = {self.variable_name: lookup_field}
        return reverse(view_name, kwargs=kwargs, request=request, format=format)


class NodeSerializer(serializers.HyperlinkedModelSerializer):

    packagechecks = HyperlinkedField(view_name='packagecheck-node',
                                           lookup_field='slug',
                                             variable_name='nodeslug')
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



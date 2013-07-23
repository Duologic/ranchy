from django.forms import widgets
from rest_framework import serializers
from farm.models import Owner, Package, PackageCheck, Node

class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = ('id','slug','name', 'identifier', 'location', 'owner')

class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = ('id','slug','name')

class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = ('id','packagetype','slug','name')

class PackageCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageCheck
        fields = ('id','node','package','current','latest', 'hasupdate', 'lastcheck')

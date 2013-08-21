from django.db import models


PACKAGETYPES = ( (1, 'apt'), (2, 'pip') )


class Owner(models.Model):
    slug = models.SlugField()
    name = models.CharField(max_length=200)
    contact = models.CharField(max_length=200, null=True, blank=True)
    mail = models.EmailField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.name


class Location(models.Model):
    slug = models.SlugField()
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(Owner)
    address1 = models.CharField(max_length=200, null=True, blank=True)
    address2 = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    notes = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.name + ' (' + self.city + ')'


class Node(models.Model):
    slug = models.SlugField()
    name = models.CharField(max_length=200)
    identifier = models.CharField(max_length=200)
    uri = models.URLField(max_length=1000, null=True, blank=True)
    location = models.ForeignKey(Location)
    parents = models.ManyToManyField("self", null=True, blank=True)
    owner = models.ForeignKey(Owner)
    notes = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.name + ' (' + str(self.location) + ')'


class Package(models.Model):
    slug = models.SlugField()
    name = models.CharField(max_length=200)
    packagetype = models.IntegerField(choices=PACKAGETYPES)
    notes = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.name


class PackageCheck(models.Model):
    package = models.ForeignKey(Package)
    node = models.ForeignKey(Node)
    current = models.CharField(max_length=200)
    latest = models.CharField(max_length=200)
    hasupdate = models.NullBooleanField()
    lastcheck = models.DateTimeField()
    notes = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = (("package", "node"),)

    def __unicode__(self):
        return self.package.name

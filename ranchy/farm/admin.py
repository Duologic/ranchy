from django.contrib import admin
from farm.models import Owner, Location, Node, Package, PackageCheck


def duplicate_event(modeladmin, request, queryset):
    for object in queryset:
        object.id = None
        object.save()
duplicate_event.short_description = "Duplicate selected record"

admin.site.add_action(duplicate_event)


class OwnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'mail',)

admin.site.register(Owner, OwnerAdmin)


class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'city',)

admin.site.register(Location, LocationAdmin)


class NodeAdmin(admin.ModelAdmin):
    save_as = True
    list_display = ('name', 'location', 'owner')
    list_filter = ('location', 'owner')

admin.site.register(Node, NodeAdmin)


class PackageAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name', 'packagetype')
    search_fields = ('slug', 'name', )

admin.site.register(Package, PackageAdmin)


class PackageCheckAdmin(admin.ModelAdmin):
    list_display = ('package', 'node', 'hasupdate')
    list_filter = ('hasupdate', 'node')
    search_fields = ('package__name', )

admin.site.register(PackageCheck, PackageCheckAdmin)

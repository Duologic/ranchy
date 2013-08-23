# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'PackageCheck.lastcheck'
        db.delete_column(u'farm_packagecheck', 'lastcheck')

        # Adding field 'PackageCheck.uninstalled'
        db.add_column(u'farm_packagecheck', 'uninstalled',
                      self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'PackageCheck.lastcheck'
        raise RuntimeError("Cannot reverse this migration. 'PackageCheck.lastcheck' and its values cannot be restored.")
        # Deleting field 'PackageCheck.uninstalled'
        db.delete_column(u'farm_packagecheck', 'uninstalled')


    models = {
        u'farm.location': {
            'Meta': {'object_name': 'Location'},
            'address1': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'address2': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['farm.Owner']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'farm.node': {
            'Meta': {'object_name': 'Node'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['farm.Location']"}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['farm.Owner']"}),
            'parents': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'parents_rel_+'", 'null': 'True', 'to': u"orm['farm.Node']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'uri': ('django.db.models.fields.URLField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'})
        },
        u'farm.owner': {
            'Meta': {'object_name': 'Owner'},
            'contact': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mail': ('django.db.models.fields.EmailField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'farm.package': {
            'Meta': {'object_name': 'Package'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'packagetype': ('django.db.models.fields.IntegerField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'farm.packagecheck': {
            'Meta': {'unique_together': "(('package', 'node'),)", 'object_name': 'PackageCheck'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'current': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'hasupdate': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latest': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['farm.Node']"}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['farm.Package']"}),
            'uninstalled': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['farm']
# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        pass
#        db.delete_index(u'farm_package', ['packagetype_id'])
        # Deleting model 'Group'

        # Deleting model 'PackageType'

        # Deleting model 'GroupType'

        # Removing M2M table for field group on 'Node'


        # Renaming column for 'Package.packagetype' to match new field type.
#        db.rename_column(u'farm_package', 'packagetype_id', 'packagetype')
        # Changing field 'Package.packagetype'
#        db.alter_column(u'farm_package', 'packagetype', self.gf('django.db.models.fields.IntegerField')())
        # Removing index on 'Package', fields ['packagetype']


    def backwards(self, orm):
        # Adding index on 'Package', fields ['packagetype']
        db.create_index(u'farm_package', ['packagetype_id'])

        # Adding model 'Group'
        db.create_table(u'farm_group', (
            ('grouptype', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['farm.GroupType'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'farm', ['Group'])

        # Adding model 'PackageType'
        db.create_table(u'farm_packagetype', (
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['farm.Group'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'farm', ['PackageType'])

        # Adding model 'GroupType'
        db.create_table(u'farm_grouptype', (
            ('notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'farm', ['GroupType'])

        # Adding M2M table for field group on 'Node'
        m2m_table_name = db.shorten_name(u'farm_node_group')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('node', models.ForeignKey(orm[u'farm.node'], null=False)),
            ('group', models.ForeignKey(orm[u'farm.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['node_id', 'group_id'])


        # Renaming column for 'Package.packagetype' to match new field type.
        db.rename_column(u'farm_package', 'packagetype', 'packagetype_id')
        # Changing field 'Package.packagetype'
        db.alter_column(u'farm_package', 'packagetype_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['farm.PackageType']))

    models = {
        u'farm.location': {
            'Meta': {'object_name': 'Location'},
            'address1': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'address2': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['farm.Owner']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        u'farm.node': {
            'Meta': {'object_name': 'Node'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['farm.Location']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['farm.Owner']"}),
            'parents': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'parents_rel_+'", 'null': 'True', 'to': u"orm['farm.Node']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'uri': ('django.db.models.fields.URLField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'})
        },
        u'farm.owner': {
            'Meta': {'object_name': 'Owner'},
            'contact': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mail': ('django.db.models.fields.EmailField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        u'farm.package': {
            'Meta': {'object_name': 'Package'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'packagetype': ('django.db.models.fields.IntegerField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        u'farm.packagecheck': {
            'Meta': {'unique_together': "(('package', 'node'),)", 'object_name': 'PackageCheck'},
            'current': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'hasupdate': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastcheck': ('django.db.models.fields.DateTimeField', [], {}),
            'latest': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['farm.Node']"}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['farm.Package']"})
        }
    }

    complete_apps = ['farm']

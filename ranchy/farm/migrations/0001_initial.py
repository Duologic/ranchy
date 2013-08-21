# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Owner'
        db.create_table(u'farm_owner', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('contact', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('mail', self.gf('django.db.models.fields.EmailField')(max_length=200, null=True, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'farm', ['Owner'])

        # Adding model 'Location'
        db.create_table(u'farm_location', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['farm.Owner'])),
            ('address1', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('address2', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'farm', ['Location'])

        # Adding model 'Node'
        db.create_table(u'farm_node', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('identifier', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('uri', self.gf('django.db.models.fields.URLField')(max_length=1000, null=True, blank=True)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['farm.Location'])),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['farm.Owner'])),
            ('notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'farm', ['Node'])

        # Adding M2M table for field parents on 'Node'
        m2m_table_name = db.shorten_name(u'farm_node_parents')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_node', models.ForeignKey(orm[u'farm.node'], null=False)),
            ('to_node', models.ForeignKey(orm[u'farm.node'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_node_id', 'to_node_id'])

        # Adding model 'Package'
        db.create_table(u'farm_package', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('packagetype', self.gf('django.db.models.fields.IntegerField')()),
            ('notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'farm', ['Package'])

        # Adding model 'PackageCheck'
        db.create_table(u'farm_packagecheck', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('package', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['farm.Package'])),
            ('node', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['farm.Node'])),
            ('current', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('latest', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('hasupdate', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('lastcheck', self.gf('django.db.models.fields.DateTimeField')()),
            ('notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'farm', ['PackageCheck'])

        # Adding unique constraint on 'PackageCheck', fields ['package', 'node']
        db.create_unique(u'farm_packagecheck', ['package_id', 'node_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'PackageCheck', fields ['package', 'node']
        db.delete_unique(u'farm_packagecheck', ['package_id', 'node_id'])

        # Deleting model 'Owner'
        db.delete_table(u'farm_owner')

        # Deleting model 'Location'
        db.delete_table(u'farm_location')

        # Deleting model 'Node'
        db.delete_table(u'farm_node')

        # Removing M2M table for field parents on 'Node'
        db.delete_table(db.shorten_name(u'farm_node_parents'))

        # Deleting model 'Package'
        db.delete_table(u'farm_package')

        # Deleting model 'PackageCheck'
        db.delete_table(u'farm_packagecheck')


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
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
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
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
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
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'farm.package': {
            'Meta': {'object_name': 'Package'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'packagetype': ('django.db.models.fields.IntegerField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
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
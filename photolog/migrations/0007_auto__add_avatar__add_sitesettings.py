# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Avatar'
        db.create_table(u'photolog_avatar', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('avatar', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('upload_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'photolog', ['Avatar'])

        # Adding model 'SiteSettings'
        db.create_table(u'photolog_sitesettings', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('site_title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('avatar', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['photolog.Avatar'])),
            ('photolog_title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('photolog_intro', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'photolog', ['SiteSettings'])


    def backwards(self, orm):
        # Deleting model 'Avatar'
        db.delete_table(u'photolog_avatar')

        # Deleting model 'SiteSettings'
        db.delete_table(u'photolog_sitesettings')


    models = {
        u'photolog.avatar': {
            'Meta': {'object_name': 'Avatar'},
            'avatar': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'upload_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'photolog.entry': {
            'Meta': {'object_name': 'Entry'},
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'unique': 'True', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'})
        },
        u'photolog.photo': {
            'Meta': {'object_name': 'Photo'},
            'caption': ('django.db.models.fields.TextField', [], {}),
            'duplicate': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'entry': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['photolog.Entry']"}),
            'exif': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'md5_original': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'upload_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'photolog.sitesettings': {
            'Meta': {'object_name': 'SiteSettings'},
            'avatar': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['photolog.Avatar']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photolog_intro': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'photolog_title': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'site_title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        }
    }

    complete_apps = ['photolog']
# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Photo.shooting_time'
        db.add_column(u'photolog_photo', 'shooting_time',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now(), blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Photo.shooting_time'
        db.delete_column(u'photolog_photo', 'shooting_time')


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
            'Meta': {'ordering': "['order', '-shooting_time']", 'object_name': 'Photo'},
            'caption': ('django.db.models.fields.TextField', [], {}),
            'duplicate': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'entry': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['photolog.Entry']"}),
            'exif': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'md5_original': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '50'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'shooting_time': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
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

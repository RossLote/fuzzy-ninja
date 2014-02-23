# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SagePayTransaction'
        db.create_table(u'sagepay_sagepaytransaction', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('vendor_tx_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=40)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('request', self.gf('jsonfield.fields.JSONField')()),
            ('response', self.gf('jsonfield.fields.JSONField')()),
            ('extra_data', self.gf('jsonfield.fields.JSONField')()),
            ('notification_date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('notification_data', self.gf('jsonfield.fields.JSONField')(null=True)),
            ('acknowledgement_data', self.gf('jsonfield.fields.JSONField')(null=True)),
        ))
        db.send_create_signal(u'sagepay', ['SagePayTransaction'])

        # Adding model 'Card'
        db.create_table(u'sagepay_card', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['auth.User'], null=True)),
            ('currency', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('card_holder', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('card_type', self.gf('django.db.models.fields.CharField')(max_length=7)),
            ('first_four_digits', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('last_four_digits', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('expiry_date', self.gf('django.db.models.fields.DateField')()),
            ('start_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('token', self.gf('django.db.models.fields.CharField')(unique=True, max_length=38)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'sagepay', ['Card'])


    def backwards(self, orm):
        # Deleting model 'SagePayTransaction'
        db.delete_table(u'sagepay_sagepaytransaction')

        # Deleting model 'Card'
        db.delete_table(u'sagepay_card')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'sagepay.card': {
            'Meta': {'object_name': 'Card'},
            'card_holder': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'card_type': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'currency': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'expiry_date': ('django.db.models.fields.DateField', [], {}),
            'first_four_digits': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_four_digits': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'token': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '38'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['auth.User']", 'null': 'True'})
        },
        u'sagepay.sagepaytransaction': {
            'Meta': {'object_name': 'SagePayTransaction'},
            'acknowledgement_data': ('jsonfield.fields.JSONField', [], {'null': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'extra_data': ('jsonfield.fields.JSONField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notification_data': ('jsonfield.fields.JSONField', [], {'null': 'True'}),
            'notification_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'request': ('jsonfield.fields.JSONField', [], {}),
            'response': ('jsonfield.fields.JSONField', [], {}),
            'vendor_tx_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'})
        }
    }

    complete_apps = ['sagepay']
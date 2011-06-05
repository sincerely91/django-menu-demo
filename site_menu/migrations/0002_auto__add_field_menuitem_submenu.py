# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'MenuItem.submenu'
        db.add_column('site_menu_menuitem', 'submenu', self.gf('django.db.models.fields.related.OneToOneField')(blank=True, related_name='parent_item', unique=True, null=True, to=orm['site_menu.Menu']), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'MenuItem.submenu'
        db.delete_column('site_menu_menuitem', 'submenu_id')


    models = {
        'site_menu.menu': {
            'Meta': {'ordering': "['slug']", 'object_name': 'Menu'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '40', 'db_index': 'True'})
        },
        'site_menu.menuitem': {
            'Meta': {'ordering': "['menu', 'position']", 'object_name': 'MenuItem'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'menu': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items'", 'to': "orm['site_menu.Menu']"}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'position': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'db_index': 'True'}),
            'submenu': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'parent_item'", 'unique': 'True', 'null': 'True', 'to': "orm['site_menu.Menu']"}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['site_menu']

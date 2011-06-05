#coding: utf-8

from django.contrib import admin

from .models import Menu, MenuItem


class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 3
    fields = [
        'path',
        'relative_url',
        'slug',
        'text',
        'is_enabled',
        'position',
        'submenu',
        ]
    readonly_fields = [
        'relative_url',
        ]
    fk_name = 'menu'

class MenuAdmin(admin.ModelAdmin):
    inlines = [
        MenuItemInline,
    ]


class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_enabled', 'text', 'path', 'slug')
    list_display_links = ('id',)
    list_editable = ('is_enabled', 'text', 'path', 'slug',)
    list_filter = ('menu',)


admin.site.register(Menu, MenuAdmin)
admin.site.register(MenuItem, MenuItemAdmin)

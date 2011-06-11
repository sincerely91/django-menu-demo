#coding: utf-8

from datetime import datetime

from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db.models import (
    Model, ForeignKey, CharField, SlugField,
    SmallIntegerField, BooleanField, OneToOneField,
    )
from django.utils.translation import ugettext_lazy as _

from model_utils.managers import manager_from


class Menu(Model):
    slug = SlugField(_("slug"), max_length=40, unique=True)

    class Meta:
        ordering = ['slug', ]
        verbose_name = _("menu")
        verbose_name_plural = _("menus")

    def __unicode__(self):
        return self.slug


class MenuItemManager(object):
    def active_for_path(self, path):
        ''' Returns menu item that is considered active for given path.
            Active item = item with path of which the given path starts
                or to the path of which the given path equals.
        '''
        # Cut trailing and starting slashes
        if path.startswith('/'):
            path = path[1:]
        if path.endswith('/'):
            path = path[:-1]
        # Split path
        path_parts = path.split('/')

        # I can't express the following with words:
        # We just find items with paths which are in the beginning given path
        # or equal given path.
        path_parts_for_check = []
        if len(path_parts) == 1 and path_parts[0] == '':
            path_parts_for_check = ['/']
        else:
            path_part = ''
            for part in path_parts:
                path_part = '/'.join([path_part, part])
                path_parts_for_check.append(path_part + '/')
        items = self.filter(
            path__in=path_parts_for_check
            )
        if not items.exists():
            items = self.filter(path__in=['/'])
        return items

    def current_for_path(self, path):
        ''' Returns menu item that is most correctly matches given path.
            That is, if our items are
                /teachers/
                /exams/
                /exams/cambridge/
                /exams/cambridge/yle/
            and our path is
                /exams/cambridge/marry/
            then `current_menu_item` is /exams/cambridge/.
            Althogh both /exams/ and /exams/cambridge/ are
            considered as active for the given path, the latter
            has more elements in it and therefore considered more accurate.

        '''
        active_items = self.active_for_path(path)
        item_with_greatest_number_of_parts = None
        for item in active_items:
            if not item_with_greatest_number_of_parts or \
                item.path_part_count > \
                    item_with_greatest_number_of_parts.path_part_count:
                item_with_greatest_number_of_parts = item
        return item_with_greatest_number_of_parts

class MenuItem(Model):
    STRING = object()
    PATTERN = object()
    menu = ForeignKey(Menu, related_name='items')
    submenu = OneToOneField(Menu, related_name='parent_item',
        null=True, blank=True)
    path = CharField(_("path"), max_length=255)
    slug = SlugField(_("slug"), max_length=100)
    text = CharField(_("text"), max_length=100)
    is_enabled = BooleanField(_("enabled"), default=True)
    position = SmallIntegerField(_("position"), null=True)

    objects = manager_from(MenuItemManager, )

    class Meta:
        ordering = ['menu', 'position', ]
        verbose_name = _("menu item")
        verbose_name_plural = _("menu items")

    def __unicode__(self):
        return u"%s (%s) @ %s" % (self.text, self.path, self.menu)

    def clean(self):
        if self.path_type == self.__class__.PATTERN:
            try:
                self.reverse_pattern()
            except:
                raise ValidationError(_(
                    "Cannot reverse pattern."
                    ))

    def get_path_type(self):
        if self.path.startswith('/'):
            return self.__class__.STRING
        return self.__class__.PATTERN
    path_type = property(get_path_type)

    def reverse_pattern(self):
        if self.path_type == self.__class__.STRING:
            return None
        pattern_bits = self.path.split(' ')
        pattern_name = pattern_bits.pop(0)
        return reverse(pattern_name, args=pattern_bits, kwargs={})

    def get_relative_url(self):
        if self.path_type == self.__class__.STRING:
            return self.path
        return self.reverse_pattern()
    relative_url = get_relative_url # =(
    relative_url.short_description = _("relative url")

    def get_path_part_count(self):
        def get_path_without_leading_and_trailing_slashes(path):
            if path.startswith('/'):
                path = path[1:]
            if path.endswith('/'):
                path = path[:-1]
            return path
        path = path_without_leading_and_trailing_slashes(self.path)
        return len(path.split('/'))
    path_part_count = property(get_path_part_count)

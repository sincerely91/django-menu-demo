#coding: utf-8

from django import template
import ttag
from django.template import Node, Variable
from django.utils.translation import ugettext as _

from ..models import Menu, MenuItem


register = template.Library()


class MenuRenderer(ttag.Tag):
    class Meta:
        name = 'render_menu'
        library = register

    slug = ttag.Arg(
        )
    as_var = ttag.Arg(
        #named=True,
        required=False,
        null=True,
        keyword=True,
        )
    context = ttag.KeywordsArg(
        named=True,
        required=False,
        null=True,
        )

    def render(self, context):
        data = self.resolve(context)
        as_var = data.get('as_var', None)
        if as_var: context[as_var] = self.output(data)
        else: return self.output(data)

    def output(self, data):
        context = data.get('context', {})
        slug = data['slug']
        templates = []

        try:
            menu = Menu.objects.get(slug=slug)
        except Menu.DoesNotExist:
            return _("Menu not found")

        templates.append('site_menu/%s_menu.html' % menu.slug)
        templates.append('site_menu/menu.html')

        context['menu'] = menu
        context['items'] = menu.items.all().select_related('submenu')

        template_obj = template.loader.select_template(templates)
        rendered_menu = template_obj.render(template.Context(context))
        return rendered_menu


class MenuItemsNode(Node):
    def __init__(self, menu_slug, context_var):
        self.menu_slug = Variable(menu_slug)
        self.context_var = context_var

    def render(self, context):
        menu_slug = self.menu_slug.resolve(context)

        try:
            menu = Menu.objects.get(slug=menu_slug)
            menu_items = menu.items.all()
        except Menu.DoesNotExist:
            menu_items = []

        context[self.context_var] = menu_items
        return ''

def get_menu_items(parser, token):
    ''' Adds to context all menu items for the given menu slug.

        Could be given an active item's slug as a string argument,
        as well as a list of active items as object of type list.
        ``is_active`` attribute will be set to True on all returned
        items that are active.

        Usage:
            {% get_menu_items "menu_slug" as menu_items %}
            {% get_menu_items "menu_slug" %}

    '''
    try:
        bits = token.split_contents()
    except ValueError:
        raise TemplateSyntaxError("Tag requires one or two arguments")
    if len(bits) not in [2, 4]:
        raise TemplateSyntaxError("Tag requires one or two arguments")
    if len(bits) > 2:
        if bits[-2] != 'as':
            raise TemplateSyntaxError("Incorrect arg format (no 'as'?)")
        context_var = bits[-1]
    else:
        context_var = 'menu_items'
    menu_slug = bits[1]
    return MenuItemsNode(menu_slug, context_var)

register.tag('get_menu_items', get_menu_items)


class ActiveMenuItemsNode(Node):
    def __init__(self, path, menu_slug, context_var):
        self.path = Variable(path)
        if menu_slug:
            self.menu_slug = Variable(menu_slug)
        self.context_var = context_var
 
    def render(self, context):
        menu_ids = Menu.objects.all().values_list('id', flat=True)
        if getattr(self, 'menu_slug', None):
            menu_slug = self.menu_slug.resolve(context)
            menu_ids = Menu.objects.filter(slug=menu_slug).values_list(
                'id', flat=True,
                )
        menu_items = MenuItem.objects.filter(
            menu__id__in=menu_ids,
            )

        active_items = menu_items.active_for_path(
            self.path.resolve(context)
            )
        context[self.context_var] = active_items
        return ''

def get_active_menu_items(parser, token):
    ''' Adds to context all menu items from all menus that are
        active. Active status is calculated from provided argument,
        which generally would be a path to the current page
        (request.path). Its start is compared with the path
        attribute of every menu item.

        Usage:
            {% get_active_menu_items request.path "menu_slug" as active_items %}
            {% get_active_menu_items request.path %}
            {% get_active_menu_items "/online/classifieds/" %}

    '''
    path = menu_slug = None
    try:
        bits = token.split_contents()
    except ValueError:
        raise TemplateSyntaxError("Tag requires from one to three arguments")
    if len(bits) not in [2, 3, 4, 5]:
        raise TemplateSyntaxError("Tag requires from one to three arguments")
    if len(bits) >= 2: path = bits[1]
    if len(bits) in [3, 5]: menu_slug = bits[2]
    if len(bits) in [4, 5]:
        if bits[-2] != 'as':
            raise TemplateSyntaxError("Incorrect arg format (no 'as'?)")
        context_var = bits[-1]
    else:
        context_var = 'active_menu_items'
    return ActiveMenuItemsNode(path, menu_slug, context_var)

register.tag('get_active_menu_items', get_active_menu_items)


class CurrentMenuItemNode(Node):
    def __init__(self, path, menu_slug, context_var):
        self.path = Variable(path)
        if menu_slug:
            self.menu_slug = Variable(menu_slug)
        self.context_var = context_var
 
    def render(self, context):
        menu_ids = Menu.objects.all().values_list('id', flat=True)
        if getattr(self, 'menu_slug', None):
            menu_slug = self.menu_slug.resolve(context)
            menu_ids = Menu.objects.filter(slug=menu_slug).values_list(
                'id', flat=True,
                )
        menu_items = MenuItem.objects.filter(
            menu__id__in=menu_ids,
            )
        try:
            current_item = menu_items.current_for_path(
                self.path.resolve(context)
                )
            context[self.context_var] = current_item
        except:
            raise
            pass

        return ''

def get_current_menu_item(parser, token):
    ''' Usage::

            {% get_current_menu_item request.path "menu_slug" as active_items %}
            {% get_current_menu_item request.path %}
            {% get_current_menu_item "/online/classifieds/" "menu_slug" %}
            {% get_current_menu_item "/online/classifieds/" %}

    '''
    path = menu_slug = None
    try:
        bits = token.split_contents()
    except ValueError:
        raise TemplateSyntaxError("Tag requires from one to three arguments")
    if len(bits) not in [2, 3, 4, 5]:
        raise TemplateSyntaxError("Tag requires from one to three arguments")
    if len(bits) >= 2: path = bits[1]
    if len(bits) in [3, 5]: menu_slug = bits[2]
    if len(bits) in [4, 5]:
        if bits[-2] != 'as':
            raise TemplateSyntaxError("Incorrect arg format (no 'as'?)")
        context_var = bits[-1]
    else:
        context_var = 'current_menu_item'

    return CurrentMenuItemNode(path, menu_slug, context_var)

register.tag('get_current_menu_item', get_current_menu_item)

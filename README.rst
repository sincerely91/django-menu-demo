Minimalistic site menu for Django.

There isn't any tests, use at your own risk. The implementation is pretty simple, though.

Won't work under Django 1.5, tested under Django 1.4.

**Setup:** Install from Git
(``pip install -e git+http://github.com/strogonoff/django-site-menu/#egg=django-site-menu``,
you may want to fork it beforehand and use your version just in case).
Install ``django-ttag``.
Add ``site_menu`` to ``settings.INSTALLED_APPS``.

Create your menu via admin and add ``{% render_menu "menu_slug" %}`` to your template.
(Load ``render_menu`` tag from ``site_menu_tags`` library beforehand.)

Put your template under ``site_menu/menu_slug.html``, and it will be used to output that menu.

Pass additional context to menu template
as simply as ``{% render_menu "menu_slug" context foo="bar" %}``.
(This can be used to highlight active menu items, for example.)

Automatically deducing selected menu items from current URL isn't included out of the box,
but included are utility template tags ``get_active_menu_items`` and ``get_current_menu_item``
that can be helpful. (See ``site_menu.models.MenuItemManager`` for "active" and "current" terms.)

Menus can be nested, just make sure your menu template can handle that.

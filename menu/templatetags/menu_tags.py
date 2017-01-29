from django import template
from django.conf import settings
from django.template import TemplateSyntaxError
from menu.models import Menu, MenuItem

register = template.Library()


def draw_menu(context, menu_name):
    try:
        menu = Menu.objects.get(name=menu_name)
    except Menu.DoesNotExist as e:
        if settings.TEMPLATE_DEBUG:
            raise e
        else:
            return context
    context['menu'] = menu
    return context
register.inclusion_tag('menu/menu.html', takes_context=True)(draw_menu)


def show_menu_item(context, menu_item):
    if not isinstance(menu_item, MenuItem):
        error_message = 'Given argument must be a MenuItem object.'
        raise template.TemplateSyntaxError(error_message)
    context['menu_item'] = menu_item
    return context
register.inclusion_tag('menu/menu_item.html', takes_context=True)(show_menu_item)

from django.contrib import admin

from .models import Menu, MenuItem

class ItemInline(admin.TabularInline):
    model = MenuItem
    extra = 1

class MenuAdmin(admin.ModelAdmin):

    inlines = [ItemInline]

admin.site.register(Menu, MenuAdmin)

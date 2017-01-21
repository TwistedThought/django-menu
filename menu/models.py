from django.db import models
from django.urls import reverse

class MenuItem(models.Model):
    parent = models.ForeignKey('self', verbose_name='parent', null=True, blank=True)
    caption = models.CharField('caption', max_length=50)
    url = models.CharField('URL', max_length=200, blank=True)
    named_url = models.CharField('named URL', max_length=200, blank=True)
    level = models.IntegerField('level', default=0, editable=False)
    rank = models.IntegerField('rank', default=0, editable=False)
    menu = models.ForeignKey('Menu', related_name='contained_items', verbose_name='menu', null=True, blank=True, editable=False)

    def __str__(self):
        return self.caption

    def save(self, *args, **kwargs):

        old_level = self.level
        if self.parent:
            self.level = self.parent.level + 1
        else:
            self.level = 0

        if self.pk:
            new_parent = self.parent
            old_parent = MenuItem.objects.get(pk=self.pk).parent
            if old_parent != new_parent:
                if new_parent:
                    clean_ranks(new_parent.children())
                    self.rank = new_parent.children().count()
                super().save(*args, **kwargs)
                if old_parent:
                    clean_ranks(old_parent.children())
            else:
                super().save(*args, **kwargs)

        else:
            if not self.has_siblings():
                self.rank = 0
            else:
                siblings = self.siblings().order_by('-rank')
                self.rank = siblings[0].rank + 1
            super().save(*args, **kwargs)

        if old_level != self.level:
            for child in self.children():
                child.save()

    def delete(self, using=None):
        old_parent = self.parent
        super().delete()
        if old_parent:
            clean_ranks(old_parent.children())

    def siblings(self):
        if not self.parent:
            return MenuItem.objects.none()
        else:
            if not self.pk:
                return self.parent.children()
            else:
                return self.parent.children().exclude(pk=self.pk)

    def siblings_urls(self):
        urls = []
        for sibling in self.siblings():
            urls.append(sibling.url)
            urls.append(sibling.reverse_named_url())
        return urls

    def has_siblings(self):
        return self.siblings().count() > 0

    def children(self):
        _children = MenuItem.objects.filter(parent=self).order_by('rank',)
        for child in _children:
            child.parent = self
        return _children

    def has_children(self):
        return self.children().count() > 0

    def reverse_named_url(self):
        if self.named_url:
            url = reverse(self.named_url)
        else:
            url = None
        return url


class Menu(models.Model):
    name = models.CharField('name', max_length=50)
    root_item = models.ForeignKey(MenuItem, related_name='is_root_item_of', verbose_name='root item', null=True, blank=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.root_item:
            root_item = MenuItem()
            root_item.caption = 'root'
            if not self.pk:
                super().save(*args, **kwargs)
            root_item.menu = self
            root_item.save()
            self.root_item = root_item
        super().save(*args, **kwargs)

    def delete(self, using=None):
        if self.root_item is not None:
            self.root_item.delete()
        super().delete()

    def __str__(self):
        return self.name

def clean_ranks(menu_items):

    rank = 0
    for menu_item in menu_items:
        menu_item.rank = rank
        menu_item.save()
        rank += 1

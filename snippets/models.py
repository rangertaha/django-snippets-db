# -*- coding:utf-8 -*-
import logging

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver

ICONS = (
    ('fa-linux', 'Linux'),
    ('fa-windows ', 'Windows'),
    ('fa-apple', 'Apple'),

    ('fa-firefox', 'Firefox'),
    ('fa-chrome ', 'Chrome'),
    ('fa-internet-explorer', 'Internet Explorer'),

    ('fa-file', 'Physical File'),
    ('fa-file-o', 'Virtual File'),

    ('fa-folder', 'Folder'),
    ('fa-folder-o', 'Folder White'),

)


class Category(models.Model):
    rank = models.IntegerField(blank=True, null=True, default=0)
    slug = models.SlugField(max_length=32, unique=True, blank=True, null=True)
    name = models.CharField(max_length=32, blank=True, null=True)
    icon = models.CharField(max_length=32, choices=ICONS, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    count = models.IntegerField(default=0)

    # category =

    class Meta:
        ordering = ('rank', )
        verbose_name_plural = "Categories"

    def __unicode__(self):
        return self.name


class Snippet(models.Model):
    order = models.IntegerField(blank=True, null=True, default=0)
    rank = models.IntegerField(blank=True, null=True, default=0)
    slug = models.SlugField(max_length=512, unique=True, blank=True, null=True)
    title = models.CharField(max_length=512, blank=True, null=True, db_index=True)
    usage = models.TextField(blank=True, null=True, unique=True)
    code = models.TextField(blank=True, null=True, unique=True)
    example = models.TextField(blank=True, null=True, unique=True)
    description = models.TextField(blank=True, null=True)

    snippets = models.ManyToManyField('self', blank=True, related_name='parent')
    categories = models.ManyToManyField(Category, blank=True, related_name='snippets')

    # Metadata
    created = models.DateTimeField(_('Created'), auto_now=True, auto_now_add=False)
    updated = models.DateTimeField(_('Updated'), auto_now=False, auto_now_add=True)
    active = models.BooleanField(_('Active'), default=False)

    class Meta:
        ordering = ('rank',)

    def __unicode__(self):
        return self.title


@receiver(pre_save, sender=Snippet)
def pre_snippet(sender, **kwargs):
    snippet = kwargs['instance']
    if not snippet.slug:
        snippet.slug = slugify(snippet.title)


@receiver(pre_save, sender=Category)
def slugify_category_name(sender, **kwargs):
    category = kwargs['instance']
    if not category.slug:
        category.slug = slugify(category.name)

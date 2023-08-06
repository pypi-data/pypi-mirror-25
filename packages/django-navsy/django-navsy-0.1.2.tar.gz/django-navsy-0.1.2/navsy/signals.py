# -*- coding: utf-8 -*-

from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

from navsy import cache
from navsy.models import Page, Pattern, Route


@receiver(post_save, sender=Page, dispatch_uid='post_save_page')
def post_save_page(sender, instance, **kwargs):
    instance.enforce_unique_home()
    instance.create_first_route()
    cache.delete_data()


@receiver(post_delete, sender=Page, dispatch_uid='post_delete_page')
def post_delete_page(sender, instance, **kwargs):
    cache.delete_data()


@receiver(pre_save, sender=Pattern, dispatch_uid='pre_save_pattern')
def pre_save_pattern(sender, instance, **kwargs):
    instance.update_regex_strings()


@receiver(post_save, sender=Pattern, dispatch_uid='post_save_pattern')
def post_save_pattern(sender, instance, **kwargs):
    cache.delete_data()


@receiver(post_delete, sender=Pattern, dispatch_uid='post_delete_pattern')
def post_delete_pattern(sender, instance, **kwargs):
    cache.delete_data()


@receiver(post_save, sender=Route, dispatch_uid='post_save_route')
def post_save_route(sender, instance, **kwargs):
    cache.delete_data()


@receiver(post_delete, sender=Route, dispatch_uid='post_delete_route')
def post_delete_route(sender, instance, **kwargs):
    cache.delete_data()

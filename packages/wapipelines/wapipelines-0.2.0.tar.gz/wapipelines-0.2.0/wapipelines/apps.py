# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class WAPipelinesConfig(AppConfig):
    name = 'wapipelines'
    verbose_name = _('WA Pipelines')

    def create_token(self, sender, instance, created, **kwargs):
        from rest_framework.authtoken.models import Token
        Token.objects.update_or_create(user=instance, defaults={})

    def ready(self):
        from django.db.models.signals import post_save
        from django.contrib.auth.models import User

        post_save.connect(self.create_token, sender=User)

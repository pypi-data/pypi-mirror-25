# -*- coding: utf-8 -*-
# Created by Gustavo Del Negro <gustavodelnegro@gmail.com> on 10/2/16.
from django.core.management import call_command
from django.test import TestCase
from django.conf import settings
from django.core.management.base import CommandError
import os
import requests


class TestManagementCommands(TestCase):

    def test_if_url_is_set(self):
        """
        Test if translation url is set in set
        """
        url = getattr(settings, "TRANSLATION_SERVER_URL", None)
        self.assertIsInstance(url, str)

    def test_get_data_from_url(self):
        """
        Test getting data from url
        """
        call_command('sync_translations')

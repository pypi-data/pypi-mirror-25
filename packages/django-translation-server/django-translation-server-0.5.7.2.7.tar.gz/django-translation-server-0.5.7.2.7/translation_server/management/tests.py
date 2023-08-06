# -*- coding: utf-8 -*-
# Created by Gustavo Del Negro <gustavodelnegro@gmail.com> on 10/2/16.
from django.core.management import call_command
from django.test import TestCase
from django.conf import settings
from django.core.management.base import CommandError
from django.utils.six import StringIO
import os
import sys


class TestManagementCommands(TestCase):

    languages_list = [lang[0] for lang in settings.LANGUAGES]
    app_name = 'translation_server'
    LOCALE_PATH = os.path.dirname(os.path.abspath(__file__)) + "/../locale"

    def test_make_translation(self):
        """
        Test command make_translation
        """
        call_command('make_translation', ",".join(self.languages_list))

    def test_make_translation_migrations(self):
        """
        Test command make_translation
        """
        call_command('make_translation_migrations', self.app_name)

    def test_translate_without_args(self):
        """
        Test command translate without args
        """
        args = []
        opts = {}
        call_command('translate', *args, **opts)

    def test_translate_with_args(self):
        """
        Test command make_translation with args
        """
        args = []
        opts = {}
        call_command('translate', locales_dir=self.LOCALE_PATH)

    def test_upload_csv_with_invalid_file(self):
        """
        Test command upload_csv with invalid file
        """
        out = StringIO()
        sys.sdout = out
        file = os.path.dirname(os.path.abspath(__file__)) + "/../../../assets/TableExpor.csv"
        self.assertRaises(IOError, call_command, 'upload_csv', file)

    def test_upload_csv_with_valid_file(self):
        """
        Test command upload_csv with valid file
        """
        out = StringIO()
        sys.sdout = out
        file = os.path.dirname(os.path.abspath(__file__)) + "/../../../assets/TableExport.csv"
        call_command('upload_csv', file, stdout=out)
        self.assertEqual("", out.getvalue())
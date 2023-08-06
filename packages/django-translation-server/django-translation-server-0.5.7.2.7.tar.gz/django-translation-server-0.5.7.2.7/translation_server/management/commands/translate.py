# -*- coding: utf-8 -*-
# Created by Gustavo Del Negro <gustavodelnegro@gmail.com> on 10/1/16.
from django.core.management import BaseCommand
from django.core.management import call_command
from django.conf import settings


class Command(BaseCommand):
    help = "This command executes all steps for translation"

    app_name = "translation_server"

    def add_arguments(self, parser):
        parser.add_argument(
            '--locales-dir',
            action='store',
            dest='locales_dir',
            default="",
            help="The locales dir to copy the translation files",
        )
        parser.add_argument(
            '--migrate',
            action='store',
            dest='migrate',
            default=False,
            help="If the translation migrations should be made",
        )

    def handle(self, *args, **options):
        languages_list = [lang[0] for lang in settings.LANGUAGES]
        if options['migrate']:
            call_command('make_translation_migrations', self.app_name)
            call_command('migrate', self.app_name)
        call_command('make_translation', ",".join(languages_list), locales_dir=options['locales_dir'])
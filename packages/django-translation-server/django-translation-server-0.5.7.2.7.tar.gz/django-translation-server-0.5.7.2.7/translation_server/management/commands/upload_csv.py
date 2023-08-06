# -*- coding: utf-8 -*-
# Created by Gustavo Del Negro <gustavodelnegro@gmail.com> on 10/1/16.
from django.core.management import BaseCommand
from django.apps import *
from django.core.management import call_command
from django.conf import settings
import re
import os


class Command(BaseCommand):
    help = "This command import a csv to the database"

    app_name = "translation_server"

    csv_file = None

    def __create_record(self, model_name, *args, **kwargs):
        model = apps.get_model('translation_server', model_name)
        try:
            mdl = model.objects.get(tag=kwargs['tag'])
        except model.DoesNotExist:
            mdl = model()
        except Exception as err:
            raise err
        for k, v in kwargs.items():
            if k == "type":
                setattr(mdl, k, apps.get_model("translation_server", "TranslationType").objects.get(tag=v))
            else:
                setattr(mdl, k, v)
        try:
            mdl.save()
        except Exception as err:
            raise err

    def __import_csv(self):
        """
        file format:
        header
        Código WMLB|Código WMHT|WMLB EN|WMLB PT|WMHT EN|WMHT PT|Nome do Campo|Tipo do Campo|Contexto|Local de Uso
        primary_tag|auxiliary_tag|text_en|text_pt_br|auxiliary_text_en|auxiliary_text_pt_br|Nome do Campo|Tipo do Campo|Contexto|Local de Uso
        0|1|2|3|4|5|6|7|8|9
        """
        # valids = re.sub(r"[^A-Za-z]+", '', my_string)
        # if "código" in line, then it's header, ignore it
        # type = re.sub(r"[^A-Za-z]+", '', line[0])
        # auxiliary_type = re.sub(r"[^A-Za-z]+", '', line[1])
        import sys
        import csv

        with open(self.csv_file, 'r') as f:
            has_auxiliary_text = False
            reader = csv.reader(f)
            for row in reader:
                # Translation Type
                if len(row) == 2:
                    translation_type_tag = None
                    auxiliary_translation_type_tag = None
                    has_auxiliary_text = False
                    types_list = row[0].split("e")
                    translation_type_tag = types_list[0].strip()
                    if len(types_list) == 2:
                        auxiliary_translation_type_tag = types_list[1].strip()
                        has_auxiliary_text = True
                    self.__create_record("TranslationType",
                                         **{'tag': translation_type_tag,
                                            'name': translation_type_tag,
                                            'has_auxiliary_text': has_auxiliary_text,
                                            'auxiliary_tag': auxiliary_translation_type_tag,
                                            'name_en': translation_type_tag,
                                            'name_pt_br': translation_type_tag})
                else:
                    if "Código" not in row[0] and len(row) > 1:
                        if len(row) == 5:
                            params_dict = {
                                'type': re.sub(r"[^A-Za-z]+", '', row[0]),
                                'tag': row[0],
                                'text': row[1],
                                'text_en': row[1],
                                'text_pt_br': row[2],
                            }
                        else:
                            params_dict = {
                                'type': re.sub(r"[^A-Za-z]+", '', row[0]),
                                'tag': row[0],
                                'text': row[2],
                                'text_en': row[2],
                                'text_pt_br': row[3],
                            }
                            if has_auxiliary_text:
                                params_dict.update({
                                    'auxiliary_tag': row[1],
                                    'auxiliary_text': row[4],
                                    'auxiliary_text_en': row[4],
                                    'auxiliary_text_pt_br': row[5]
                                })
                        self.__create_record("Translation", **params_dict)

    def add_arguments(self, parser):
        parser.add_argument(
            'file',
            action='store',
            default="",
            help="The input csv file",
        )

    def handle(self, *args, **options):
        if len(options['file']) > 0:
            self.csv_file = options['file']
            try:
                my_file = open(self.csv_file)
            except IOError as error:
                raise error
            else:
                self.__import_csv()

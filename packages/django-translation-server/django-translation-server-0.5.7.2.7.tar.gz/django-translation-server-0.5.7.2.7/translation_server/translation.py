# -*- coding: utf-8 -*-
# Created by Gustavo Del Negro <gustavodelnegro@gmail.com> on 10/1/16.
from modeltranslation.translator import TranslationOptions, translator
from translation_server.models import *


class TranslationModelTranslationOptions(TranslationOptions):
    fields = ('text', 'auxiliary_text')
    required_languages = {'en': ('text', ), 'pt-br': ('text',)}


class TranslationTypeModelTranslationOptions(TranslationOptions):
    fields = ('name',)
    required_languages = ('en', 'pt-br')


class SiteSettingsModelTranslationOptions(TranslationOptions):
    fields = ('value',)
    required_languages = ('en', 'pt-br')

translator.register(Translation, TranslationModelTranslationOptions)
translator.register(TranslationType, TranslationTypeModelTranslationOptions)
# -*- coding: utf-8 -*-
# Created by Gustavo Del Negro <gustavodelnegro@gmail.com> on 10/23/16.
from django.core.management import BaseCommand
from datetime import datetime
from django.core.management import call_command
from django.utils.translation import to_locale
from django.conf import settings
from translation_client.exceptions import InvalidSettingsException
import os
import requests


class Command(BaseCommand):
    help = "This command generates the translation files, based on the response from the 'translation_server'"
    languages_list = None
    locale_path = None
    BASE_DIR = os.path.join(settings.BASE_DIR, 'locale')
    file_map = {}
    url = getattr(settings, "TRANSLATION_SERVER_URL", None)

    def __create_translation_dirs(self):
        if not os.path.exists(self.locale_path):
            os.makedirs(self.locale_path)
        for language in self.languages_list:
            # call_command('makemessages', '-l', language)
            if not os.path.exists(self.locale_path+"/"+to_locale(language)+"/LC_MESSAGES"):
                os.makedirs(self.locale_path+"/"+to_locale(language)+"/LC_MESSAGES")

    def __create_translation_files(self):
        self.__create_translation_dirs()
        for language in self.languages_list:
            self.file_map.update(
                {
                    language: {
                        'dir': self.locale_path + "/" + to_locale(language) + "/LC_MESSAGES/",
                        'file': open(self.locale_path + "/" + to_locale(language) + "/LC_MESSAGES/django.po", "w")
                    }
                }
            )
        header = """
# SOME DESCRIPTIVE TITLE.
# Copyright (C) YEAR THE PACKAGE'S COPYRIGHT HOLDER
# This file is distributed under the same license as the PACKAGE package.
# FIRST AUTHOR <EMAIL@ADDRESS>, YEAR.
#
#, fuzzy
msgid ""
msgstr ""
"Project-Id-Version: PACKAGE VERSION\\n"
"Report-Msgid-Bugs-To: \\n"
"POT-Creation-Date: 2016-05-19 14:44+0000\\n"
"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\\n"
"Last-Translator: FULL NAME <EMAIL@ADDRESS>\\n"
"Language-Team: LANGUAGE <LL@li.org>\\n"
"Language: \\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=UTF-8\\n"
"Content-Transfer-Encoding: 8bit\\n"
"Plural-Forms: nplurals=2; plural=(n > 1);\\n"
"""
        translations = requests.get(self.url).json()
        for language in self.file_map:
            try:
                self.file_map[language]['file'].write(
                    "%s# File generated in: %s \n\n" % (header, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                )
                for translation in translations:
                    text = translation.get("text_"+language.replace("-", "_"), None)
                    self.file_map[language]['file'].write(
                        'msgid "%(tag)s"\nmsgstr "%(text)s"\n\n' % {
                            'tag': translation['tag'],
                            'text': text.replace('"', '\\"') if text else ""
                        }
                    )
                    if translation['auxiliary_tag']:
                        auxiliary_text = translation.get("auxiliary_text_" + language.replace("-", "_"), None)
                        self.file_map[language]['file'].write(
                            'msgid "%(tag)s"\nmsgstr "%(text)s"\n\n' % {
                                'tag': translation['auxiliary_tag'],
                                'text': auxiliary_text.replace('"', '\\"') if auxiliary_text else ""
                            }
                        )
            except Exception as error:
                self.file_map[language]['file'].close()
                raise error
            else:
                self.file_map[language]['file'].close()
        return True

    def add_arguments(self, parser):
        parser.add_argument(
            '--locales-dir',
            action='store',
            dest='locales_dir',
            default="",
            help="The locales dir to store/write the *.po files",
        )

    def handle(self, *args, **options):
        if len(settings.LANGUAGES) == 0:
            raise InvalidSettingsException("You need at least one language on your project settings")
        self.languages_list = [lang[0] for lang in settings.LANGUAGES]
        self.locale_path = options['locales_dir'] if len(options['locales_dir']) > 1 else self.BASE_DIR
        self.__create_translation_files()
        if self.__create_translation_files():
            compile_options = {}
            for lang in self.languages_list:
                compile_options.update({'locale': lang})
            call_command('compilemessages', options=compile_options)

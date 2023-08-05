import io
import os
import re

import xlsxwriter
from django.conf import settings
from django.core.management import BaseCommand


def get_messages(content):
    return zip(re.findall('^msgid \"(.*)\"[^\"]*', content, re.MULTILINE),
               re.findall('^msgstr \"(.*)\"[^\"]*', content, re.MULTILINE))


def export_xlsx(lang, content, format):
    name = 'django_{0}.{1}'.format(lang, format)
    workbook = xlsxwriter.Workbook(name)
    worksheet = workbook.add_worksheet()
    row = 0
    col = 0
    for msgid, msgstr in get_messages(content):
        worksheet.write(row, col, msgid)
        worksheet.write(row, col + 1, msgstr)
        row += 1

    workbook.close()


def export_csv(lang, content, format):
    name = 'django_{0}.{1}'.format(lang, format)
    with open(name, "w", encoding='utf-8') as csv_file:
        for msgid, msgstr in get_messages(content):
            row = "'" + msgid + "','" + msgstr + "'\n"
            csv_file.write(row)
        csv_file.close()


class Command(BaseCommand):
    help = 'Export po files'

    def add_arguments(self, parser):
        parser.add_argument(
            'language', nargs='+',
            help='Language to export',
            type=str
        )
        parser.add_argument(
            '--format',
            type=str,
            dest='format',
            default='xlsx',
            help='Format of file type',
        )

    def handle(self, *args, **options):
        locale_paths = []
        locale = options['language'][0].split(',')
        formats = options['format'].split(',')
        locale_paths.extend(settings.LOCALE_PATHS)
        if os.path.isdir('locale'):
            locale_paths.append(os.path.abspath('locale'))
        default_locale_path = locale_paths[0]
        for lang in locale:
            django_po = os.path.join(default_locale_path, lang, 'LC_MESSAGES', 'django.po')

            with io.open(django_po, 'r', encoding='utf-8') as pofile:
                content = pofile.read()
                for format in formats:
                    format = format.lower()
                    if format in ['xlsx', 'xls']:
                        export_xlsx(lang, content, format)
                    elif format == 'csv':
                        export_csv(lang, content, format)

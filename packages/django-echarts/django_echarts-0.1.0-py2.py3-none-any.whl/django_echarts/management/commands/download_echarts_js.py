# coding=utf8

from __future__ import unicode_literals

import os

from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import six

from django_echarts.utils import DJANGO_ECHARTS_SETTING


class Command(BaseCommand):
    help = 'Download remote javascript to the local.'

    def add_arguments(self, parser):
        parser.add_argument('js_name', type=six.text_type)

        parser.add_argument(
            '--js_host',
            dest='js_host',
            help='The host where the file will be downloaded from.'
        )

    def handle(self, *args, **options):
        js_name = options['js_name']
        remote_host_store = DJANGO_ECHARTS_SETTING.host_store  # TODO Add support for js_host optional argument.
        local_host_store = DJANGO_ECHARTS_SETTING.create_local_host()
        if local_host_store:
            remote_url = remote_host_store.generate_js_link(js_name)
            local_path = local_host_store.generate_js_link(js_name)
            local_path = local_path.replace('/', os.sep)
            local_path = settings.BASE_DIR + local_path
            with six.moves.urllib.request.urlopen(remote_url) as response, open(local_path, 'w+b') as out_file:
                data = response.read()
                out_file.write(data)
        else:
            self.stderr.write('No local host is specified.')

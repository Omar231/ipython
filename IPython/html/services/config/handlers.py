"""Tornado handlers for kernel specifications."""

# Copyright (c) IPython Development Team.
# Distributed under the terms of the Modified BSD License.
import json
import os
import io
from tornado import web

from ...base.handlers import IPythonHandler, json_errors


class ConfigHandler(IPythonHandler):
    SUPPORTED_METHODS = ('GET', 'PUT', 'PATCH')

    def file_name(self, section_name):
        return os.path.join(self.profile_dir, 'nb_%s_config.json' % section_name)

    @web.authenticated
    @json_errors
    def get(self, section_name):
        self.set_header("Content-Type", 'application/json')
        filename = self.file_name(section_name)
        if os.path.isfile(filename):
            with io.open(filename, encoding='utf-8') as f:
                self.finish(f.read())
        else:
            self.finish("{}")

    @web.authenticated
    @json_errors
    def put(self, section_name):
        filename = self.file_name(section_name)
        with open(filename, 'wb') as f:
            f.write(self.request.body)
        self.set_status(204)

    @web.authenticated
    @json_errors
    def patch(self, section_name):
        filename = self.file_name(section_name)
        if os.path.isfile(filename):
            with io.open(filename, encoding='utf-8') as f:
                section = json.load(f)
        else:
            section = {}

        for k, v in self.get_json_body().items():
            if v is None:
                section.pop(k, None)
            else:
                section[k] = v

        with io.open(filename, 'w', encoding='utf-8') as f:
            json.dump(section, f)
        self.set_status(204)


# URL to handler mappings

section_name_regex = r"(?P<section_name>\w+)"

default_handlers = [
    (r"/api/config/%s" % section_name_regex, ConfigHandler),
]

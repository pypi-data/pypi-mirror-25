from __future__ import absolute_import, print_function, unicode_literals

from distutils.spawn import find_executable
import os

import six


PROGRAMMING_LANGUAGE = 'Python'
WORKER_SCRIPT = 'zenaton_slave'


class Config:

    @property
    def app_id(self):
        return os.environ['ZENATON_APP_ID']

    @property
    def app_env(self):
        return os.environ['ZENATON_APP_ENV']

    @property
    def api_token(self):
        return os.environ['ZENATON_API_TOKEN']

    @property
    def concurrent_max(self):
        return os.getenv('ZENATON_CONCURRENT_MAX', 100)

    @property
    def _handle_only(self):
        return os.getenv('ZENATON_HANDLE_ONLY', [])

    @property
    def workflows_name_only(self):
        return []  # FIXME

    @property
    def tasks_name_only(self):
        return []  # FIXME

    @property
    def workflows_name_except(self):
        return []  # FIXME

    @property
    def tasks_name_except(self):
        return []  # FIXME

    @property
    def worker_script(self):
        return find_executable(WORKER_SCRIPT)

    def to_dict(self):
        return {
            'app_id': self.app_id,
            'app_env': self.app_env,
            'api_token': self.api_token,
            'concurrent_max': six.text_type(self.concurrent_max),
            'workflows_name_only': self.workflows_name_only,
            'tasks_name_only': self.tasks_name_only,
            'workflows_name_except': self.workflows_name_except,
            'tasks_name_except': self.tasks_name_except,
            'programming_language': PROGRAMMING_LANGUAGE,
            'worker_script': self.worker_script,
            'autoload_path': None,
        }

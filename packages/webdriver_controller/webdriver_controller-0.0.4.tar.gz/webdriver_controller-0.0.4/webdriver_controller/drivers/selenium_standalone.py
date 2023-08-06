import re
import subprocess
import sys

import requests
import xmltodict

from webdriver_controller import config
from webdriver_controller.utils import tools


class SeleniumStandalone(object):
    @property
    def version(self):
        return self.get_latest_version()

    @property
    def download_url(self):
        filename = self._get_filename()
        version_key = self.version[:(self.version.find('.', -1) - 1)]
        url = '{}{}/{}'.format(
            config.STORAGE_URLS.get('selenium'), version_key, filename)
        return url

    def _get_filename(self) -> str:
        return 'selenium-server-standalone-{}.jar'.format(self.version)

    def get_latest_version(self) -> str:
        resp = requests.get(config.STORAGE_URLS.get('selenium'))
        try:
            resp.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise e
        else:
            doc = xmltodict.parse(resp.content)
            items = doc.get('ListBucketResult').get('Contents')

            for item in reversed(items):
                if 'standalone' in item.get('Key') and 'beta' not in item.get(
                        'Key'):
                    selenium_key = item.get('Key').strip()
                    break

            pattern = re.compile('selenium-server-standalone-(.*).jar')
            version = pattern.match(selenium_key.split('/')[1]).group(1)

            return version

    def start(self) -> None:
        if not tools.is_java_installed():
            print('No Java executable found')
            sys.exit(1)

        selenium_executable = '{}/{}'.format(config.INSTALLATION_FOLDER,
                                             self._get_filename())
        try:
            subprocess.run(['java', '-jar', selenium_executable])
        except KeyboardInterrupt:
            print('\rStop Selenium standalone server')

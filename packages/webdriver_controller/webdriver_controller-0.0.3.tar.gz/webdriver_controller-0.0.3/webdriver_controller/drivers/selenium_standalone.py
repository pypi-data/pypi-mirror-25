import re

import requests
import xmltodict

from webdriver_controller import config


class SeleniumStandalone(object):
    @property
    def version(self):
        return self.get_latest_version()

    @property
    def filename(self):
        # return 'selenium-server-standalone-{}.jar'.format(self.version)
        return self._get_filename()

    @property
    def download_url(self):
        filename = self._get_filename()
        # filename = 'selenium-server-standalone-{}.jar'.format(self.version)
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

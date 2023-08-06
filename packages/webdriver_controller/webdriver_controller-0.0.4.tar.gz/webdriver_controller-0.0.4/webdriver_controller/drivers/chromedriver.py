import subprocess
import sys

import requests

from webdriver_controller import config
from webdriver_controller.utils import tools


class ChromeDriver(object):
    @property
    def version(self):
        return self.get_latest_version()

    @property
    def download_url(self):
        url = '{}{}/{}'.format(
            config.STORAGE_URLS.get('chromedriver'), self.version,
            self._get_filename())
        return url

    def _get_filename(self) -> str:
        return 'chromedriver_{}.zip'.format(tools.get_platform())

    def get_latest_version(self) -> str:
        host = config.STORAGE_URLS.get('chromedriver')
        latest_rel_doc_url = '{}LATEST_RELEASE'.format(host)

        resp = requests.get(latest_rel_doc_url)
        try:
            resp.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise e
        else:
            latest_verison = resp.text.strip()

            return latest_verison

    def unzip_file(self) -> None:
        dest = '{}/{}'.format(config.INSTALLATION_FOLDER, self._get_filename())

        # unzip the driver
        subprocess.run(
            ['unzip', '-oq', dest, '-d', config.INSTALLATION_FOLDER])

    def start(self) -> None:
        if not tools.is_chromedriver_executable_existed():
            print(
                'chromedriver not found in Selenium Webdriver installation folder'
            )
            sys.exit(1)

        try:
            subprocess.run([config.CHROMEDRIVER_EXECUTABLE])
        except KeyboardInterrupt:
            print('\rStop ChromeDriver')

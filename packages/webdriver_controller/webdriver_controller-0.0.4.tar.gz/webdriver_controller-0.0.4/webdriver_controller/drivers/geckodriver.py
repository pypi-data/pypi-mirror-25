import subprocess
import sys
import tarfile

import requests

from webdriver_controller import config
from webdriver_controller.utils import tools


class GeckoDriver(object):
    @property
    def version(self):
        return self.get_latest_version()

    @property
    def download_url(self):
        url = '{}/v{}/{}'.format(
            config.STORAGE_URLS.get('geckodriver'), self.version,
            self._get_filename())
        return url

    def _get_filename(self) -> str:
        host_platform = tools.get_platform()

        if host_platform.startswith('mac'):
            os_arch = 'macos'
        elif host_platform.startswith('linux'):
            os_arch = host_platform

        return 'geckodriver-v{}-{}.tar.gz'.format(self.version, os_arch)

    def get_latest_version(self) -> str:
        # Github v3 API
        tag_api_endpoint = 'https://api.github.com/repos/mozilla/geckodriver/tags'

        resp = requests.get(tag_api_endpoint)
        try:
            resp.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise e
        else:
            resp_json = resp.json()
            latest_verison = resp_json[0].get('name')

            # version in response: v0.19.0
            return latest_verison[1:]

    def unzip_file(self) -> None:
        tar_file = '{}/{}'.format(config.INSTALLATION_FOLDER,
                                  self._get_filename())

        with tarfile.open(tar_file) as fh:
            fh.extractall(config.INSTALLATION_FOLDER)

    def start(self) -> None:
        if not tools.is_geckodriver_executable_existed():
            print(
                'geckodriver not found in Selenium Webdriver installation folder'
            )
            sys.exit(1)

        try:
            subprocess.run([config.GECKODRIVER_EXECUTABLE])
        except KeyboardInterrupt:
            print('\rStop GeckoDriver')

import json
import platform
import os
import shutil
import sys

from webdriver_controller import config


def get_platform() -> str:
    if os.name == 'posix':
        arch = platform.architecture()[0]

        if 'darwin' == sys.platform:
            return 'mac{}'.format(arch[0:2])
        if 'linux' == sys.platform:
            return 'linux{}'.format(arch[0:2])


def is_installation_folder_existed() -> bool:
    return config.INSTALLATION_FOLDER.exists()


def check_installation_folder() -> None:
    if not is_installation_folder_existed():
        config.INSTALLATION_FOLDER.mkdir()


def is_version_file_existed() -> bool:
    return config.VERSION_FILE.exists()


def check_version_file() -> None:
    if is_version_file_existed():
        config.VERSION_FILE.rename(config.OUTDATED_VERSION_FILE)


def remove_outdated_version_file() -> None:
    if config.OUTDATED_VERSION_FILE.exists():
        config.OUTDATED_VERSION_FILE.unlink()


def write_version_file(version_info: dict) -> None:
    with open(config.VERSION_FILE, 'w') as fh:
        json.dump(version_info, fh)


def read_version_file():
    with open(config.VERSION_FILE, 'r') as fh:
        version_info = json.load(fh)
        return version_info


def is_java_installed() -> bool:
    if shutil.which('java') is None:
        return False

    return True


def is_chromedriver_executable_existed() -> bool:
    return config.CHROMEDRIVER_EXECUTABLE.exists()


def is_geckodriver_executable_existed() -> bool:
    return config.GECKODRIVER_EXECUTABLE.exists()

from pathlib import Path

STORAGE_URLS = {
    'selenium': 'https://selenium-release.storage.googleapis.com/',
    'chromedriver': 'https://chromedriver.storage.googleapis.com/'
}

INSTALLATION_FOLDER = Path('{}{}'.format(Path.cwd(), '/drivers'))
VERSION_FILE = Path('{}/{}'.format(INSTALLATION_FOLDER, 'versions'))
OUTDATED_VERSION_FILE = Path(
    '{}/{}.old'.format(INSTALLATION_FOLDER, 'versions'))

CHROMEDRIVER_EXECUTABLE = Path('{}/chromedriver'.format(INSTALLATION_FOLDER))

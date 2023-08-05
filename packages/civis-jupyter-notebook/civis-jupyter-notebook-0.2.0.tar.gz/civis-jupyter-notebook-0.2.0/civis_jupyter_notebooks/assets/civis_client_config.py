import os
import civis
from civis_jupyter_notebooks.platform_persistence import logger as LOGGER
import pip

REQUIREMENTS_PATH = os.path.expanduser(os.path.join('~', 'work', 'requirements.txt'))

if 'CIVIS_API_KEY' in os.environ:
    LOGGER.info('creating civis api client')
    client = civis.APIClient(resources='all')
    LOGGER.info('civis api client created')

if os.path.isfile(REQUIREMENTS_PATH):
    LOGGER.info('installing requirements.txt packages')
    pip.main(['install', '-r', REQUIREMENTS_PATH])
    LOGGER.info('requirements.txt installed')

# clean out the namespace for users
del os
del pip
del LOGGER
del REQUIREMENTS_PATH

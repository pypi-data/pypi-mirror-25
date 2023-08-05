import os
import civis
from civis_jupyter_notebooks import platform_persistence
import pip

logger = platform_persistence.setup_logging()

REQUIREMENTS_PATH = os.path.expanduser(os.path.join('~', 'work', 'requirements.txt'))

if 'CIVIS_API_KEY' in os.environ:
    logger.info('creating civis api client')
    client = civis.APIClient(resources='all')
    logger.info('civis api client created')

if os.path.isfile(REQUIREMENTS_PATH):
    logger.info('install requirements.txt packages')
    pip.main(['install', '-r', REQUIREMENTS_PATH])
    logger.info('requirements.txt installed')

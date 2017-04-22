import os
from jikji.publisher import LocalPublisher

# Root Path of Application
ROOT_PATH = os.path.dirname(__file__)


# Absolute directory path includes Template files
TEMPLATE_ROOT = ROOT_PATH + '/templates'

# Directory that includes Static files (to copied to output)
STATIC_ROOT = ROOT_PATH + '/static'

# Directory that includes View files
VIEW_ROOT = ROOT_PATH + '/views'

# Publisher instance used after generation
PUBLISHER = LocalPublisher(output_root=ROOT_PATH + '/output')
# PUBLISHER = S3Publisher('my-bucket1')


# Scripts that runned on initializing application
INIT_SCRIPTS = (
	ROOT_PATH + '/urls.py',
	ROOT_PATH + '/pages.py',
)

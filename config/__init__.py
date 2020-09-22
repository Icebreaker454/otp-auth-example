import os

from .default import *  # noqa

if os.getenv("TESTING"):
    from .test import *  # noqa

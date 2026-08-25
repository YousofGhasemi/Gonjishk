from .base import *  # noqa: F403

DEBUG = env.bool("DEBUG", default=False)  # noqa: F405
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")  # noqa: F405

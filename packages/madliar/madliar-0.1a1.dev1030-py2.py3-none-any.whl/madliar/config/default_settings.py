"""
madliar default settings. Override these with settings in the
user's custom module.

"""

# --------------------------------------------------------------------------- #
# For CORE
# --------------------------------------------------------------------------- #
DEBUG = True

# Enable the freamwork print log when running.
ENABLE_MADLIAR_LOG = False
MADLIAR_LOG_PATH = "./"

# Enable built-in static respose server. It will ignored when DEBUG=False
STATICS_URL_MAP = {
    "^/statics": "statics",
    "^/static": "static",
}

# To load middleware.
INSTALLED_MIDDLEWARE = (
    "madliar.middleware.BaseMiddleware",
)

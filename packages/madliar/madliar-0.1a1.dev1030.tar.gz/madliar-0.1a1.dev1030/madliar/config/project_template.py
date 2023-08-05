import os
replace_char = "\r\n" if os.name in ("nt", ) else "\n"

# ---------------------------- README.rst ---------------------------------- #
default_read_me_for_user = """
MadLiar

  This is a tiny WSGI web application freamwork. 

""".replace("\n", replace_char)


# ---------------------- application/urls.py ------------------------------- #
default_user_url_map = """

url = {

}
""".replace("\n", replace_char)


# --------------- management/madliar_uwsgi_socket.xml ---------------------- #
default_wsgi_xml = """
<uwsgi>
    <socket>:65501</socket>
    <chdir>%s</chdir>
    <module>management.wsgi</module>
    <processes>1</processes>
    <daemonize>%s_madliar.log</daemonize>
</uwsgi>
""".replace("\n", replace_char)


# --------------------- management/wsgi.py --------------------------------- #
default_wsgi_py = """
\"""
The public interface to WSGI support. It returns a WSGI callable.

\"""

from madliar.core import get_application


application = get_application()
""".replace("\n", replace_char)


# --------------------- management/config.py --------------------------------- #
default_user_config = """
\"""
madliar freamwork settings.

\"""

# --------------------------------------------------------------------------- #
# For CORE
# --------------------------------------------------------------------------- #
DEBUG = True

# Enable the freamwork print log when running.
ENABLE_MADLIAR_LOG = True
MADLIAR_LOG_PATH = "C:\Program Files (x86)\python27\Lib\site-packages\madliar"

# Enable built-in static respose server. It will ignored when DEBUG=False
STATICS_URL_MAP = {
    "^/statics": "statics",
    "^/static": "static",
}

# To load middleware.
INSTALLED_MIDDLEWARE = (
    "madliar.middleware.BaseMiddleware",
)
""".replace("\n", replace_char)

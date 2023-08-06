import os
replace_char = "\r\n" if os.name in ("nt", ) else "\n"

# ---------------------------- README.rst ---------------------------------- #
default_read_me_for_user = """
madliar

  This is a tiny WSGI web application freamwork. For more infomation refers to 
https://github.com/cl-ei/madliar/blob/master/README.rst

  Thanks for checking it out.

""".replace("\n", replace_char)


# ---------------------- application/urls.py ------------------------------- #
default_user_url_map = """
from madliar.http.response import HttpResponse


# The `hello_world` function is just used to show you how to start an application,
# you may need remove it and build your own url map latter.
def hello_world(request):
    return HttpResponse("Hello world !")


url = {
    "/": hello_world,

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
default_user_config = """\"""
madliar freamwork settings.

\"""

# If set True, An internal static files distribution server will be started,
# and more detail info will be provided when error occured.
DEBUG = True

# Enable the debug log output.
ENABLE_SYS_LOG = True
SYS_LOG_PATH = "./"

# Statics files response url. It will ignored when DEBUG=False
STATICS_URL_MAP = {

}

# To load middleware.
INSTALLED_MIDDLEWARE = (

)
""".replace("\n", replace_char)

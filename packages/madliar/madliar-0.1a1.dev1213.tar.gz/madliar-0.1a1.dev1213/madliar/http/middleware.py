"""
Base middleware

"""
from madliar.config import settings
from madliar.http.response import HttpResponse, Http500Response
from madliar.exceptions import NoInstalledApplicationError


class BaseMiddleware(object):
    def __init__(self, get_response):
        # One-time configuration and initialization.
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
        except NoInstalledApplicationError:
            import madliar
            if settings.PROJECT_CWD != madliar.__path__:
                response = HttpResponse(
                    "<center><h3>Error happend!</h3>"
                    "<p>An error happend when madliar load the url map from "
                    "`application.urls` module so that the server cannot work regularly. "
                    "please check it or send an email to author.</p></center>"
                )
            else:
                response = HttpResponse(
                    "<center><h3>It works!</h3><p>You must install at least one app in your project.</p></center>"
                )

        except Exception as e:
            if settings.DEBUG:
                response = HttpResponse(
                    "<center><h3>An error happend !</h3><p>Error: %s</p></center>" % e
                )
            else:
                response = Http500Response()

            if settings.ENABLE_SYS_LOG:
                from madliar.config.log4 import logging
                from madliar.utils import get_traceback

                traceback = get_traceback()
                logging.error("An error caused internal server error: %s, \n%s" % (e, traceback))

        return response

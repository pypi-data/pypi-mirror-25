"""
Base middleware

"""
from madliar.http.response import HttpResponse, Http500Response
from madliar.config import settings
from madliar.exceptions import NoInstalledApplicationError


class BaseMiddleware(object):
    def __init__(self, get_response):
        # One-time configuration and initialization.
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
        except NoInstalledApplicationError:
            if settings.DEBUG:
                response = HttpResponse(
                    "<center><h3>It works!</h3></center>"
                )
            else:
                response = Http500Response()

        except Exception as e:
            if settings.DEBUG:
                response = HttpResponse(
                    "<center><h3>An error happend: %s</h3></center>" % e
                )
            else:
                response = Http500Response()

        return response

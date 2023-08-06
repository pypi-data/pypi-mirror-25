import re
import os
import sys
from importlib import import_module
from wsgiref.simple_server import make_server

from madliar import exceptions as madliar_except
from madliar.http.request import WSGIRequest
from madliar.config import settings
from madliar.http.response import static_files_response, Http404Response
from madliar.utils import cached_property, get_traceback


def dynamic_import_class(dotted_path):
    """
    Import a dotted module path and return the attribute/class designated by the
    last name in the path. Raise ImportError if the import failed.
    """
    try:
        module_path, class_name = dotted_path.rsplit('.', 1)
    except ValueError:
        raise ImportError("%s doesn't look like a module path" % dotted_path)

    dynamic_imported_module = import_module(module_path)

    try:
        return getattr(dynamic_imported_module, class_name)
    except AttributeError:
        raise ImportError(
            """Module "%s" does not define a "%s" attribute/class"""
            % (module_path, class_name)
        )


class BaseHandler(object):
    def __init__(self, *args, **kwargs):
        pass


class WSGIHandler(BaseHandler):
    request_class = WSGIRequest

    def __init__(self, *args, **kwargs):
        super(WSGIHandler, self).__init__(*args, **kwargs)
        self._handler = None

    def __call__(self, environ, start_response):
        request = self.request_class(environ)
        response = self.get_response(request)

        response._handler_class = self.__class__

        status = '%d %s' % (response.status_code, response.reason_phrase)
        start_response(str(status), response.headers.items())

        if getattr(response, 'file_to_stream', None) is not None and environ.get('wsgi.file_wrapper'):
            response = environ['wsgi.file_wrapper'](response.file_to_stream)
        return response

    @cached_property
    def middleware_chain(self):
        get_response_func = self.route_distributing
        for class_path in settings.INSTALLED_MIDDLEWARE[::-1]:
            try:
                cls = dynamic_import_class(class_path)
            except Exception as e:
                err_msg = (
                    "An error happend when load custom middleware: %s, "
                    "the application may not work properly.\n%s"
                    % (e, get_traceback())
                )
                sys.stderr.write(err_msg)
                if settings.ENABLE_SYS_LOG:
                    from madliar.config.log4 import logging
                    logging.critical(err_msg)

                return get_response_func

            if callable(cls):
                get_response_func = cls(get_response_func).__call__
        return get_response_func

    @cached_property
    def url_map(self):
        try:
            application = import_module("application.urls")
        except ImportError:
            raise madliar_except.NoInstalledApplicationError("You must installed a app.")

        try:
            url_map = getattr(application, "url")
        except AttributeError:
            raise madliar_except.ProjectFolderStructureError("Bad poject folder struct.")

        return url_map

    def route_distributing(self, request):
        search_loop = self.url_map.items()
        route_path = request.route_path
        while True:
            try:
                url, sub_url_map = search_loop.pop(0)
            except IndexError:
                break

            if callable(sub_url_map) and url[-1] != "$":
                url += "$"

            m = re.match(url, route_path)
            if m:
                if callable(sub_url_map):
                    return sub_url_map(request, *m.groups())

                route_path = route_path[len(m.group()):] or "/"
                search_loop = sub_url_map.items()

        # Not hit
        if settings.DEBUG:
            request_url = request.path_info
            for static_url, static_path in settings.STATICS_URL_MAP.items():
                m = re.match(static_url, request_url)
                if m:
                    matched_statics_path = request_url[len(m.group()):].lstrip("/")
                    static_file_path = os.path.join(
                        static_path,
                        *os.path.split(matched_statics_path)
                    )
                    return static_files_response(request, static_file_path)

        return Http404Response()

    def get_response(self, request):
        return self.middleware_chain(request)


def get_application():
    return WSGIHandler()


def wsgi_server(host, port):
    """Start a simple server."""
    return make_server(host, port, get_application())

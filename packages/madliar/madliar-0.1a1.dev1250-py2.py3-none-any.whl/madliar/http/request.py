import cgi
import re
from madliar.config import settings
from madliar.utils import cached_property


__all__ = ("WSGIRequest", )

QUERY_STRING_PATTERN = re.compile(r"([^=]+)=(.*)")
QUERY_STRING_SPLIT = re.compile('[&;]')
MULTI_PART_FORM_PTRN = re.compile(r"([ a-zA-Z0-9_-]+)=\"(.*)\"")


class WSGIRequest(object):
    def __init__(self, environ):
        self._encoding = "utf-8"

        script_name = environ.get('SCRIPT_NAME', "")
        path_info = environ.get('PATH_INFO', "/")
        self.path_info = path_info

        self.script_url = environ.get('SCRIPT_URL', " ")
        self.environ = environ
        self.path = '%s/%s' % (script_name.rstrip('/'), path_info.replace('/', '', 1))
        self.__route_path = path_info

        self.META = environ
        self.META['PATH_INFO'] = path_info
        self.META['SCRIPT_NAME'] = script_name
        self.method = environ['REQUEST_METHOD'].upper()

        self.content_type, self.content_params = cgi.parse_header(environ.get('CONTENT_TYPE', ''))

    def _get_scheme(self):
        return self.environ.get('wsgi.url_scheme')

    @property
    def route_path(self):
        return self.__route_path

    @route_path.setter
    def route_path(self, path):
        self.__route_path = path

    @staticmethod
    def parse_query_string(raw_qs):
        pairs = [p for p in QUERY_STRING_SPLIT.split(raw_qs) if p]
        query = dict()
        for pair in pairs:
            m = QUERY_STRING_PATTERN.match(pair)
            if m:
                unquote_value = cgi.urlparse.unquote(m.group(2))
                query[m.group(1)] = unquote_value
        return query

    @cached_property
    def GET(self):
        """The WSGI spec says 'QUERY_STRING' may be absent."""
        raw_query_string = self.environ.get('QUERY_STRING', '')
        query = self.parse_query_string(raw_query_string)
        return query

    def _parse_form_description(self, temp_qs, line):
        qs_pairs = line.strip("\r\n ").split(";")
        description_k, description = map(lambda x: x.strip(" "), qs_pairs[0].split(":"))
        temp_qs[description_k] = description

        for pair in qs_pairs[1:]:
            m = MULTI_PART_FORM_PTRN.match(pair)
            if m:
                k, v = m.groups()
                temp_qs[k.strip("\r\n ")] = v.strip("\r\n ")
        return temp_qs

    def _load_multipart_form_data(self):
        self._post, self._files = {}, {}

        input_handler = self.META["wsgi.input"]
        content_length = min(
            int(self.META.get("CONTENT_LENGTH", 0)),
            settings.MAX_POST_SIZE
        )

        boundary = None
        loaded_content_length = 0
        currsor_position = "boundary"  # "boundary", "description", "content"
        temp_qs = {}

        while True:
            c = input_handler.readline()
            loaded_content_length += len(c)

            if currsor_position == "boundary":
                if boundary is None:
                    if not c:
                        continue

                    m = re.match("(-{2,100}[a-zA-Z0-9]+)\r\n", c)
                    if not m:
                        continue
                    else:
                        boundary = m.group(0)
                if c == boundary:
                    currsor_position = "description"

            elif currsor_position == "description":
                if c == "\r\n":
                    currsor_position = "content"
                else:
                    temp_qs = self._parse_form_description(temp_qs or {}, c)

            elif currsor_position == "content":
                finished_form = bool(c == boundary)
                if finished_form:
                    finished_all = False
                else:
                    finished_all = bool(c[:len(boundary)] == boundary.strip("\r\n") + "--")

                if finished_form or finished_all:
                    name = temp_qs.get("name")
                    f_name = temp_qs.get("filename")
                    if f_name:
                        del temp_qs["name"]
                        if temp_qs["chunk"][-1] == "\r\n":
                            temp_qs["chunk"].pop()
                        if temp_qs["chunk"][-1].endswith("\r\n"):
                            temp_qs["chunk"][-1] = temp_qs["chunk"][-1][:-2]
                        self._files[name] = temp_qs
                    else:
                        self._post[name] = "".join(temp_qs["chunk"])[:-2]

                if finished_form:
                    temp_qs = {}
                    currsor_position = "description"
                elif finished_all:
                    return
                else:
                    if not isinstance(temp_qs.get("chunk"), list):
                        temp_qs["chunk"] = []
                    temp_qs["chunk"].append(c)

            if loaded_content_length >= content_length:
                break

    def _load_post_and_files(self):
        if self.content_type == "multipart/form-data":
            self._load_multipart_form_data()
        else:
            try:
                request_body_size = int(self.environ.get('CONTENT_LENGTH', 0))
            except ValueError:
                request_body_size = 0

            if request_body_size > settings.MAX_POST_SIZE:  # 4MB
                raise ValueError("POST request body too long: %s Bytes." % request_body_size)

            request_body = self.environ['wsgi.input'].read(request_body_size).replace("+", " ")
            post_qs = self.parse_query_string(request_body)
            self._post, self._files = post_qs, {}

    @cached_property
    def POST(self):
        if self.method != "POST":
            return dict()

        if not hasattr(self, '_post'):
            self._load_post_and_files()
        return self._post

    @property
    def FILES(self):
        if not hasattr(self, '_files'):
            self._load_post_and_files()
        return self._files

    @cached_property
    def COOKIES(self):
        raw = [_ for _ in self.environ.get('HTTP_COOKIE', '').split(";") if _]
        cookie = {}
        for col in raw:
            key, val = col.split("=", 1)
            cookie[key.strip()] = val
        return cookie

import cgi
import re
from madliar.config import settings
from madliar.utils import cached_property


__all__ = ("WSGIRequest", )

QUERY_STRING_PATTERN = re.compile(r"([^=]+)=(.*)")
QUERY_STRING_SPLIT = re.compile('[&;]')
MULTI_PART_FORM_PTRN = re.compile(r"([ a-zA-Z0-9_-]+)=\"(.*)\"")
BOUNDARY_START_PTERN = re.compile(r"(-{2,100}[a-zA-Z0-9]+)")


class MultipartDataParser(object):

    def __init__(self, input_handler, content_length):
        self.input_handler = input_handler
        self.content_length = content_length

        self._files, self._post = {}, {}
        self.__loaded = False

    def load_boundary(self, content):
        find_range = content.strip("\r\n ").split("\r\n")
        for line in find_range:
            line = line.strip("\r\n")
            m = BOUNDARY_START_PTERN.match(line)
            if m:
                return m.group(0).strip("\r\n ")
        return None

    def load_description(self, lines):
        temp_qs = {}
        for line in lines:
            line = line.strip("\r\n ")
            if not line:
                continue

            qs_pairs = line.split(";")
            description_k, description = map(lambda x: x.strip(" "), qs_pairs[0].split(":"))
            temp_qs[description_k] = description

            for pair in qs_pairs[1:]:
                m = MULTI_PART_FORM_PTRN.match(pair)
                if m:
                    k, v = m.groups()
                    temp_qs[k.strip("\r\n ")] = v.strip("\r\n ")
        return temp_qs

    def load_all(self):
        self.__loaded = True

        content = self.input_handler.read(self.content_length)
        boundary = self.load_boundary(content[:100])
        if not boundary:
            return

        sections = content.split(boundary)
        for sec in sections:
            s = re.split("\r\n\r\n", sec, 1)
            if len(s) != 2:
                continue

            sec_description, sec_content = s
            temp_qs = self.load_description(sec_description.split("\r\n"))

            name = temp_qs.get("name", "__")
            if temp_qs.get("filename"):
                content_type = temp_qs.get("Content-Type")
                prefix = content_type.split("/")[0].strip("\r\n ")
                if prefix in ("text", ):
                    temp_qs["contents"] = sec_content.replace("\r\n", "\n")[:-1]
                else:
                    temp_qs["contents"] = sec_content[:-2] if sec_content.endswith("\r\n") else sec_content

                self._files[name] = temp_qs
            else:
                self._post[name] = sec_content.replace("\r\n", "\n").rstrip("\n")

    @property
    def files(self):
        if not self.__loaded:
            self.load_all()
        return self._files

    @property
    def post(self):
        if not self.__loaded:
            self.load_all()
        return self._post


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

    def _load_post_and_files(self):
        if self.content_type == "multipart/form-data":
            parser = MultipartDataParser(
                input_handler=self.META["wsgi.input"],
                content_length=min(
                    int(self.META.get("CONTENT_LENGTH", 0)),
                    settings.MAX_POST_SIZE
                )
            )
            self._post, self._files = parser.post, parser.files
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

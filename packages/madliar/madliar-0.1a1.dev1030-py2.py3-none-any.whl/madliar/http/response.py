import re
from wsgiref.headers import Headers

STATICS_FILE_MIME_TYPE = (
    (("png", "jpg", "jpeg", "gif"), "image", None),
    (("js", "woff"), "application", ("javascript", "x-font-woff")),
    (("css", ), "text", None),
    (("mp3", "wav", ), "audio/mpeg", None),
)


class BaseResponse(object):
    def __init__(self, *args, **kwargs):
        self.status_code = kwargs.get("status_code", 200)
        self.reason_phrase = kwargs.get("reason_phrase", "OK")
        self.cookies = []
        self.charset = kwargs.get("charset", "utf-8")
        self._handler_class = None
        self._content = []
        self.__set_default_headers()
        self.headers.add_header(
            "Content-Type",
            kwargs.get("content_type", "text/html; charset=%s" % self.charset)
        )

    def __set_default_headers(self):
        self.headers = Headers([
            ("Server", "MadLiar"),
            ("Access-Control-Allow-Origin", "*"),
            ("X-Frame-Options", "SAMEORIGIN"),
        ])

    @property
    def content(self):
        return b''.join(self._content)

    @content.setter
    def content(self, value):
        # Consume iterators upon assignment to allow repeated iteration.
        if not hasattr(value, '__iter__'):
            value = [value]

        content = b''.join(map(
            lambda x: bytes(x) if isinstance(x, bytes) else bytes(x.encode(self.charset)),
            value
        ))
        self.headers.add_header("Content-length", str(len(content)))
        self._content = [content]

    def __iter__(self):
        return iter(self._content)


class HttpResponse(BaseResponse):
    def __init__(self, *args, **kwargs):
        BaseResponse.__init__(self, *args, **kwargs)
        content = kwargs.get("content", args[0])
        if type(content) == unicode:
            content = content.encode("utf-8")
        if type(content) in (bytes, str):
            self.content = content


class Http404Response(BaseResponse):
    def __init__(self, *args, **kwargs):
        BaseResponse.__init__(self, *args, **kwargs)
        self.content = "<center><h3>404 Not Found!</h3></center>"
        self.status_code = 404
        self.reason_phrase = "Not Found"


class Http410Response(BaseResponse):
    def __init__(self, *args, **kwargs):
        BaseResponse.__init__(self, *args, **kwargs)
        self.content = "<center><h3>410 Gone!</h3></center>"
        self.status_code = 410
        self.reason_phrase = "Gone"


class Http500Response(BaseResponse):
    def __init__(self, *args, **kwargs):
        BaseResponse.__init__(self, *args, **kwargs)
        self.content = "<center><h3>500 Internal Server Error!</h3></center>"
        self.status_code = 500
        self.reason_phrase = "Internal Server Error"


class StreamingHttpResponse(BaseResponse):
    def _set_streaming_content(self, value):
        return self, value


class FileResponse(StreamingHttpResponse):
    """
    A streaming HTTP response class optimized for files.
    """
    block_size = 4096

    def _set_streaming_content(self, value):
        super(FileResponse, self)._set_streaming_content(value)


class HttpResponseRedirectBase(HttpResponse):
    allowed_schemes = ['http', 'https', 'ftp']

    def __init__(self, redirect_to, *args, **kwargs):
        super(HttpResponse, self).__init__()
        self._content_type_for_repr = ""
        self._redirect_to = redirect_to

    url = property(lambda self: self['Location'])

    def __repr__(self):
        return '<%(cls)s status_code=%(status_code)d%(content_type)s, url="%(url)s">' % {
            'cls': self.__class__.__name__,
            'status_code': self.status_code,
            'content_type': self._content_type_for_repr,
            'url': self.url,
        }


def static_files_response(request, static_path):
    static_file_path = static_path + request.route_path
    try:
        with open(static_file_path, "rb") as f:
            content = f.read()
    except IOError:
        return Http404Response()

    try:
        static_file_ext_name = re.match(r".*\.(.*)", static_file_path).groups()[0].lower()
    except AttributeError:
        return Http404Response()

    for static_file_typedef in STATICS_FILE_MIME_TYPE:
        ext_name_group, mime_type, mime_desc = static_file_typedef
        if static_file_ext_name in ext_name_group:
            content_type = "%s/%s" % (
                mime_type,
                mime_desc[ext_name_group.index(static_file_ext_name)] if mime_desc else static_file_ext_name
            )
            break
    else:
        content_type = None

    return HttpResponse(content, content_type=content_type)

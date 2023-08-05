import re
import os
from wsgiref.headers import Headers
from madliar import __version__


STATICS_FILE_MIME_TYPE = (
    ("xml",             "text/xml"),
    ("css",             "text/css"),
    ("html htm shtml",  "text/html"),
    ("txt",             "text/plain"),
    ("mml",             "text/mathml"),
    ("wml",             "text/vnd.wap.wml"),
    ("htc",             "text/x-component"),
    ("jad",             "text/vnd.sun.j2me.app-descriptor"),

    ("png",             "image/png"),
    ("gif",             "image/gif"),
    ("jpeg jpg",        "image/jpeg"),
    ("tif tiff",        "image/tiff"),
    ("webp",            "image/webp"),
    ("jng",             "image/x-jng"),
    ("ico",             "image/x-icon"),
    ("svg svgz",        "image/svg+xml"),
    ("bmp",             "image/x-ms-bmp"),
    ("wbmp",            "image/vnd.wap.wbmp"),

    ("mp4",             "video/mp4"),
    ("ts",              "video/mp2t"),
    ("mpeg mpg",        "video/mpeg"),
    ("3gpp 3gp",        "video/3gpp"),
    ("webm",            "video/webm"),
    ("mng",             "video/x-mng"),
    ("m4v",             "video/x-m4v"),
    ("flv",             "video/x-flv"),
    ("wmv",             "video/x-ms-wmv"),
    ("asx asf",         "video/x-ms-asf"),
    ("avi",             "video/x-msvideo"),
    ("mov",             "video/quicktime"),

    ("ogg",             "audio/ogg"),
    ("mp3",             "audio/mpeg"),
    ("mid midi kar",    "audio/midi"),
    ("m4a",             "audio/x-m4a"),
    ("ra",              "audio/x-realaudio"),

    ("js",              "application/javascript"),
    ("run",             "application/x-makeself"),
    ("xls",             "application/vnd.ms-excel"),
    ("jardiff",         "application/x-java-archive-diff"),
    ("rar",             "application/x-rar-compressed"),
    ("xpi",             "application/x-xpinstall"),
    ("sea",             "application/x-sea"),
    ("hqx",             "application/mac-binhex40"),
    ("sit",             "application/x-stuffit"),
    ("rtf",             "application/rtf"),
    ("kml",             "application/vnd.google-earth.kml+xml"),
    ("xhtml",           "application/xhtml+xml"),
    ("jnlp",            "application/x-java-jnlp-file"),
    ("ppt",             "application/vnd.ms-powerpoint"),
    ("atom",            "application/atom+xml"),
    ("m3u8",            "application/vnd.apple.mpegurl"),
    ("rss",             "application/rss+xml"),
    ("cco",             "application/x-cocoa"),
    ("jar war ear",     "application/java-archive"),
    ("tcl tk",          "application/x-tcl"),
    ("prc pdb",         "application/x-pilot"),
    ("woff",            "application/font-woff"),
    ("zip",             "application/zip"),
    ("doc",             "application/msword"),
    ("eot",             "application/vnd.ms-fontobject"),
    ("kmz",             "application/vnd.google-earth.kmz"),
    ("ps eps ai",       "application/postscript"),
    ("json",            "application/json"),
    ("pdf",             "application/pdf"),
    ("pl pm",           "application/x-perl"),
    ("7z",              "application/x-7z-compressed"),
    ("der pem crt",     "application/x-x509-ca-cert"),
    ("xspf",            "application/xspf+xml"),
    ("swf",             "application/x-shockwave-flash"),
    ("wmlc",            "application/vnd.wap.wmlc"),
    ("rpm",             "application/x-redhat-package-manager"),
    ("xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"),
    ("docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"),
    ("pptx", "application/vnd.openxmlformats-officedocument.presentationml.presentation"),
    ("bin exe dll deb dmg iso img msi msp msm", "application/octet-stream"),
)


class BaseResponse(object):
    def __init__(self, status_code=None, reason_phrase=None, content_type=None, charset=None):
        try:
            if not status_code:
                status_code = 200
                reason_phrase = "OK"

            self.status_code = int(status_code)
            self.reason_phrase = reason_phrase

        except (TypeError, ValueError):
            # TODO: add traceback
            self.status_code = 500
            self.reason_phrase = "Internal Server Error"

        self.cookies = []
        self.charset = charset or "utf-8"
        self._handler_class = None
        self._content = []
        self.__set_default_headers()

        content_type = "text/html" if not content_type else content_type.strip(" \r\n")
        if (
            content_type.split("/", 1)[0] in ("text", "application")
            and "charset" not in content_type.lower()
        ):
            content_type = "%s; charset=%s" % (content_type.rstrip("; \r\n"), self.charset)
        self.headers.add_header("Content-Type", content_type)

    def __set_default_headers(self):
        self.headers = Headers([
            ("Server", "MadLiar/%s" % __version__),
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
    def __init__(self, content, *args, **kwargs):
        super(HttpResponse, self).__init__(*args, **kwargs)
        if type(content) == unicode:
            content = content.encode(self.charset)
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


def static_files_response(request, static_file_path):
    try:
        with open(static_file_path, "rb") as f:
            content = f.read()
    except IOError:
        return Http404Response()

    content_type = "application/octet-stream"
    static_file_ext_name = os.path.splitext(static_file_path)[-1].lower().lstrip(".")
    if static_file_path:
        for file_type, description in STATICS_FILE_MIME_TYPE:
            if static_file_ext_name in file_type:
                content_type = description
                break

    return HttpResponse(content, content_type=content_type)

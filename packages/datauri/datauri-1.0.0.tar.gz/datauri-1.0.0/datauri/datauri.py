import base64
import re
import urllib.parse


# RFC 3986: reserved characters, unreserved characters, and percent.
# See https://tools.ietf.org/html/rfc3986#section-2
RE_DATA_URI = re.compile(
    'data:[{unreserved}{reserved}{percent}]+'
    .format(
        unreserved="A-Za-z0-9-_.~",
        reserved=":/?#\[\]@!$&'()*+,;=",  # only square brackets are escaped
        percent='%'))


class DataURIError(ValueError):
    """
    Exception raised when parsing fails.

    This class subclasses the built-in ``ValueError``.
    """
    pass


class ParsedDataURI:
    """
    Container for parsed data URIs.

    Do not instantiate directly: use ``parse()`` instead.
    """
    def __init__(self, media_type, data, uri):
        self.media_type = media_type
        self.data = data
        self.uri = uri

    def __repr__(self):
        raw = self.data
        if len(raw) > 20:
            raw = raw[:17] + b'...'
        return '<ParsedDataURI media_type={!r} data={!r}>'.format(
            self.media_type, raw)

    def __eq__(self, other):
        return (self.media_type, self.data) == (other.media_type, other.data)

    def __hash__(self):
        return hash((self.media_type, self.data))


def parse(uri):
    """
    Parse a data uri according to RFC2397.

    The generic format is:

      data:[<mediatype>][;base64],<data>

    See https://tools.ietf.org/html/rfc2397 for details.
    """
    if not uri.startswith('data:'):
        raise DataURIError('invalid data uri')
    s = uri[5:]
    if not s or ',' not in s:
        raise DataURIError('invalid data uri')
    media_type, _, raw_data = s.partition(',')
    is_base64_encoded = media_type.endswith(';base64')
    if is_base64_encoded:
        media_type = media_type[:-7]
        missing_padding = '=' * (-len(raw_data) % 4)
        if missing_padding:
            raw_data += missing_padding
        try:
            data = base64.b64decode(raw_data)
        except ValueError as exc:
            raise DataURIError('invalid base64 in data uri') from exc
    else:
        # Note: unquote_to_bytes() does not raise exceptions for invalid
        # or partial escapes, so there is no error handling here.
        data = urllib.parse.unquote_to_bytes(raw_data)
    if not media_type:
        media_type = None
    return ParsedDataURI(media_type, data, uri)


def discover(s):
    """
    Discover data uris in a string.

    This returns a generator that yields data URIs found in the string.
    """
    for match in RE_DATA_URI.finditer(s):
        try:
            yield parse(match.group())
        except DataURIError:
            continue
